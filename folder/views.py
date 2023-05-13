from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from .selializer import *
from user_app.models import Users
# from user_app.views import 
from rest_framework import status
import itertools

def getSharedFolders(request):
    if request.method == 'GET':
        user = Users.objects.get(email = "xxx@naver.com")#token으로 변경해야 함
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
    
# 
