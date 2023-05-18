from .models import Folder
from .models import Permission
from .selializer import CreateFolderSerializer, FolderSerializer 
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse # , HttpRequest
from .selializer import *
from rest_framework import status
import itertools

from user_app.models import Users
# from trashbin.models import Trashbin
# from trashbin.serializers import TrashbinSerializer
from django.core.serializers import serialize
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from dropbox.settings import SECRET_KEY
import json



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
    if request.method == 'POST' :
        data = JSONParser().parse(request)

        print("*****data = ")
        print(data)

        input_name = data['folder_name']

        user_token = request.headers.get("Authorization", None)
        payload_data = decode_jwt_token(user_token)

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

            # 원래의 나랑 폴더 이름이 같은 경우 
            # -> 현재와 이름이 같아, 수정 불가능 response
            if current_folder.folder_name == input_name : 
                response = JsonResponse({
                    "ResponseCode":400,
                    "description" : "현재 이름과 같습니다."
                    }, status=400)
                return response
            else : # 원래의 나랑은 다르고,
                # db에서 input 폴더 이름으로 된 폴더 객체가 이미 존재하는 경우
                # -> 중복된 폴더 이름 response

                try :
                    already_exist = Folder.objects.get(folder_name = input_name)
                    print(already_exist.exist())

                    if already_exist.exist() :
                        response = JsonResponse({
                        "ResponseCode" : 400,
                        "description" : "폴더명 중복"
                        }, status=400)
                    return response

                except Folder.DoesNotExist :
                    # 중복X, 현재이름과 같음X -> 이름 수정해서 저장 & 성공 response
                    current_folder.folder_name = input_name
                    # current_folder.updated_at = datetime
                    current_folder.save()
                    response = HttpResponse(status = 200)
                    return response


                # if Folder.objects.get(folder_name = input_name).exist() :
                #     response = JsonResponse({
                #         "ResponseCode":400,
                #         "description" : "폴더명 중복"
                #         }, status=400)
                #     return response

            
def getSharedFolder(folderId):
    return Folder.objects.get(id = folderId)

def getSharedFolders(request):
    if request.method == 'GET':
        try:
            token = request.headers.get('Authorization')
            payload = decode_jwt_token(token) 
            user = Users.objects.get(id = payload["user_id"])
        except AuthenticationFailed:
            # 유효하지 않은 토큰 또는 인증 오류 발생시 처리할 내용
            return JsonResponse({
                    "ResponseCode":401,
                    "description" : "권한이 없습니다."
                    }, status=401)

        # user = Users.objects.get(email = "xxx@naver.com")#token으로 변경해야 함
        pemissionQueryset = Permission.objects.filter(users = user)
        serializer = GetSharedFolderSerializer(pemissionQueryset, many=True)
        folder_data = list(itertools.chain(*[d["folder"] for d in serializer.data]))
        
        return JsonResponse(folder_data, safe = False)
def shareFolder(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        recieverArray = data['reciever']
        if Folder.objects.filter(id=data['folderId']).exists():
            folder = Folder.objects.get(id=data['folderId'])
            try:
                token = request.headers.get('Authorization')
                payload = decode_jwt_token(token) 
                user = Users.objects.get(id=payload["user_id"])
                if user.id != folder.users.id:
                    return JsonResponse({
                        "ResponseCode": 401,
                        "description": "권한이 없습니다."
                    }, status=401)
                if not Permission.objects.filter(users=user, folder=folder).exists():
                    permission_data = {
                        'users': user.id,
                        'folder': folder.id
                    }
                    serializer = SharedFolderSerializer(data=permission_data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return JsonResponse({
                            "ResponseCode": 400,
                            "description": "공유하지 못했습니다.",
                            "errors": serializer.errors
                        }, status=400)
            except AuthenticationFailed:
                return JsonResponse({
                    "ResponseCode": 401,
                    "description": "권한이 없습니다."
                }, status=401)
        else:
            return JsonResponse({
                "ResponseCode": 404,
                "description": "파일을 찾을 수 없습니다."
            }, status=404)
        
        for recieverEmail in recieverArray:
            try:
                reciever = Users.objects.get(email=recieverEmail)
                # permission = Permission(users=reciever, folder=folder)
                # print(permission)
                permission_data = {
                    'users': reciever.id,
                    'folder': folder.id
                }
                serializer = SharedFolderSerializer(data=permission_data)
                if serializer.is_valid():
                    if not Permission.objects.filter(users=reciever, folder=folder).exists():
                        serializer.save()
                else:
                    return JsonResponse({
                        "ResponseCode": 400,
                        "description": "공유하지 못했습니다.",
                        "errors": serializer.errors
                    }, status=400)
            except Users.DoesNotExist:
                return JsonResponse({
                    "ResponseCode": 404,
                    "description": "수신자를 찾을 수 없습니다."
                }, status=404)
        return JsonResponse({"ResponseCode": 201,
                "folder": {
        "id": folder.id,
        "name": folder.folder_name,
        "userId": folder.users.id,
        # 다른 필드들도 필요에 따라 추가할 수 있습니다.
        },
        "receiverEmail": recieverArray
        })

 
    
# def contentInFolder(request):
#     if request.method == 'GET':



# 토큰에서 payload 추출
def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, 'HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
