from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .models import Folder
from .models import Permission
from .selializers import FolderSerializer

def folderCreate(request) :
    if request.method == 'POST' :
            data = JSONParser().parse(request)

            print(data)

            serializer = FolderSerializer(data = data)

            print(serializer.is_valid())
            print(serializer.errors)
            print(serializer.validated_data)

            if serializer.is_valid() :
                # if 사용자 권한 유무 검사 :
                    # 유효하면
                    input_folderName = data['folder_name'] 
                    if Folder.objects.filter(folder_name = input_folderName).exists() :
                        response = JsonResponse({
                        "ResponseCode":400,
                        "description" : "폴더명 중복"
                        })
                        return HttpResponse(status=400)
                    
                    else : # 없으면 db 저장
                        serializer.save()
                        savedFolder = Folder.objects.filter(input_folderName)
                        savedId = savedFolder.get('id')
                        response = JsonResponse({
                              "id": savedId,
                              "folder_name": savedFolder.get('folder_name'),
                              "user_id": savedFolder.get('user_id')
                        })

                # else : ---> 권한 없음 (오류 응답)
                    response = JsonResponse({
                    "ResponseCode":401,
                    "description" : "권한이 없습니다."
                    })
                    return HttpResponse(status=401)

                  


def folderDelete(request) :
    return 0

def folderVerifyName(request) :
    return 0

def folderMove(request) :
     return 0
