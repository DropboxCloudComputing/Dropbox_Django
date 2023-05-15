from .models import Folder
from .models import Permission
from .selializer import CreateFolderSerializer
from .selializer import FolderSerializer 
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from .selializer import *
from rest_framework import status
import itertools

from user_app.models import Users
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from dropbox.settings import SECRET_KEY


def folderCreate(request) :
    if request.method == 'POST' :
        data = JSONParser().parse(request)

        print("*****data = ")
        print(data)
        print("*****type of data = ")
        print(type(data))

        user_token = request.headers.get("Authorization", None)
         # 토큰으로부터 데이터 받아와서
        payload_data = decode_jwt_token(user_token)

        print("*****    payload_data = ", payload_data)

        user = Users.objects.get(id= payload_data['user_id'])
        data['user'] = user
        folder = Folder.objects.get(id=data['pfolder'])
        data['pfolder'] = folder

        print("*****    Inserted user_id in data = ")
        print(data)

        serializer = CreateFolderSerializer(data = data)


        print("****    validation : ")
        print(serializer.is_valid())
        print(serializer.errors)
        print(serializer.validated_data)

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
                        savedId = savedFolder.get('id')
                        
                            
                        # 부모 폴더가 없는 경우 (request.pfolder_id = 0)
                        if savedFolder.get('folder_id') == 0 :
                            # 본인의 아이디를 참조하도록 수정 및 저장
                            savedFolder.folder_id = savedId
                            savedFolder.save()

                        response = JsonResponse({
                                "id": savedId,
                                "folder_name": savedFolder.get('folder_name'),
                                "user_id": savedFolder.get('user_id')
                        })
                        return response

                else : # id 조회 불가능
                    response = JsonResponse({
                        "ResponseCode":401,
                    "description" : "권한이 없습니다."
                    }, status=401)
                    return response
                  
def folderDelete(request) :
    return 0

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
