from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from .selializer import *
from rest_framework import status
import itertools

from user_app.models import Users
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

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
        serializer = GetSharedFolderSirializer(pemissionQueryset, many=True)
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
            serializer = SharedFolderSirializer(data=permission.__dict__)
            if serializer.is_valid():
                serializer.save()

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    
# def contentInFolder(request):
#     if request.method == 'GET':



# 토큰에서 payload 추출
def decode_jwt_token(token):
    try:
        print(token)
        payload = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        print(payload['user_id'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')

