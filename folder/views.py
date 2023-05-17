from .models import Folder
from .models import Permission
from .selializer import CreateFolderSerializer
from .selializer import FolderSerializer 
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse # , HttpRequest
from .selializer import *
from rest_framework import status
import itertools

from user_app.models import Users
# from trashbin.models import Trashbin
# from trashbin.serializers import TrashbinSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from dropbox.settings import SECRET_KEY




def folderCreate(request) :
    if request.method == 'POST' :
        data = JSONParser().parse(request)

        # print("*****data = ")
        # print(data)
        # print("*****type of data = ")
        # print(type(data))

        user_token = request.headers.get("Authorization", None)
         # 토큰으로부터 데이터 받아와서
        payload_data = decode_jwt_token(user_token) #print token, payload type, payload user_id

        # print("*****    payload_data = ", payload_data)

        user = Users.objects.get(id= payload_data['user_id'])
        data['users'] = user.id # user
        folder = Folder.objects.get(id=data['pfolder'])
        data['pfolder'] = folder.id

        # print("*****    Inserted user_id in data = ")
        # print(data)

        serializer = CreateFolderSerializer(data = data)

        # print("****    validation : ")
        # print(serializer.is_valid())
        # print(serializer.errors)
        # print(serializer.validated_data)

        if serializer.is_valid() :
            # print(user_token)
            if user_token == None :
                response = JsonResponse({
                    "ResponseCode":401,
                    "description" : "권한이 없습니다."
                    }, status=401)
                return response
                
            else :
                # 데이터에 대한 id에 대한 유저가 조회 가능하면
                if user :
                    input_folderName = data['folder_name']
                    # 받아온 폴더 이름이 이미 존재하면
                    if Folder.objects.filter(folder_name = input_folderName).exists() :
                        response = JsonResponse({
                            "ResponseCode":400,
                            "description" : "폴더명 중복"
                            }, status=400)
                        return response

                    else : # 폴더 이름이 중복되지 않으면 db에 저장
                        serializer.save()
                        savedFolder = Folder.objects.get(folder_name = input_folderName)
                        savedId = savedFolder.id
                        
                            
                        # 부모 폴더가 없는 경우 (request.pfolder_id = 0)
                        if savedFolder.pfolder == 0 :
                            # 본인의 아이디를 참조하도록 수정 및 저장
                            savedFolder.pfolder = savedId
                            savedFolder.save()

                        response = JsonResponse({
                                "id": savedId,
                                "folder_name": savedFolder.folder_name,
                                "user_id": savedFolder.users.id
                        }, status=200)
                        return response

                else : # id 조회 불가능
                    response = JsonResponse({
                        "ResponseCode":401,
                        "description" : "권한이 없습니다."
                        }, status=401)
                    return response
        else :
            response = JsonResponse({
                "ResponseCode":400,
                "description" : "생성하지 못했습니다(유효하지 않은 값)."
                }, status=400)
            return response



def folderDelete(request) :
    # models.py - removed : 지워지면 1, 존재하면 0
    if request.method == 'POST' :
        user_token = request.headers.get("Authorization", None)
        payload_data = decode_jwt_token(user_token)
        # user = Users.objects.get(id= payload_data['user_id'])
        
        if user_token == None :
                response = JsonResponse({
                    "ResponseCode":401,
                    "description" : "권한이 없습니다."
                    }, status=401)
                return response
        else :
            current_folder_id = request.GET['current_folder_id']
            print(current_folder_id)
            
            current_folder = Folder.objects.get(pk = current_folder_id)

            if current_folder.removed :
                response = JsonResponse({
                    "ResponseCode":403,
                    "description" : "이미 삭제된 폴더입니다."
                    }, status=403)
                return response
            
            else :
                current_folder.removed = 1
                current_folder.save()
                return HttpResponse(status = 200)
                # serializer = TrashbinSerializer(Folder = current_folder)

                # print(serializer.is_valid())
                # print(serializer.errors)
                # print(serializer.validated_data)

                # if serializer.is_valid() :
                #     serializer.save()
                #     if Trashbin.object.get(folder_id = current_folder_id).exist() :
                #         response = HttpResponse(status=200)
                #         return response
                #     else :
                #         response = JsonResponse({
                #             "ResponseCode":400,
                #             "description" : "휴지통으로 이동 실패"
                #             }, status=400)
                #         return response


                # else :
                #     response = JsonResponse({
                #         "ResponseCode":400,
                #         "description" : "휴지통으로 이동 실패(파일이 유효하지 않음)"
                #         }, status=400)
                #     return response

def folderVerifyName(request) :
    return 0

def getSharedFolders(request):
    if request.method == 'GET':
        auth = JWTAuthentication()
        token = request.headers.get('Authorization')
        try:
            #user, t= auth.authenticate(request)
            # print(token)
            payload = decode_jwt_token(request.headers.get('Authorization')) #jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            print(payload)
            user = Users.objects.get(id = payload["user_id"])
            # print(payload)
        except AuthenticationFailed:
            # 유효하지 않은 토큰 또는 인증 오류 발생시 처리할 내용
            return HttpResponse(status=401)

        # user = Users.objects.get(email = "xxx@naver.com")#token으로 변경해야 함
        pemissionQueryset = Permission.objects.filter(users = user)
        serializer = GetSharedFolderSerializer(pemissionQueryset, many=True)
        folder_data = list(itertools.chain(*[d["folder"] for d in serializer.data]))
        
        return JsonResponse(folder_data, safe = False)


def shareFolder(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        recieverArray = data['reciever']
        folder = Folder.objects.get(id=data['folderId'])

        for reciever in recieverArray:
            user = Users.objects.get(email = reciever)
            permission = Permission.objects.create(users=user, folder=folder)
            serializer = SharedFolderSerializer(data=permission.__dict__)
            if serializer.is_valid():
                serializer.save()

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    
# def contentInFolder(request):
#     if request.method == 'GET':



# 토큰에서 payload 추출
def decode_jwt_token(token):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, 'HS256')
        
        print(type(payload))
        print(payload['user_id'])

        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
