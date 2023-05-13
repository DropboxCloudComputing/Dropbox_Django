from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from .selializer import *
from user_app.models import Users
# from user_app.views import 
import itertools

def getSharedFolders(request):
    if request.method == 'GET':
        user = Users.objects.get(email = "xxx@naver.com")#token으로 변경해야 함
        pemissionQueryset = Permission.objects.filter(users = user)
        serializer = GetSharedFolderSirializer(pemissionQueryset, many=True)
        folder_data = list(itertools.chain(*[d["folder"] for d in serializer.data]))
        #folder_data = list(itertools.chain.from_iterable(serializer.data[0]['folder']))
        # print(folder_data)
        return JsonResponse(folder_data, safe = False)


def shareFolder(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        return JsonResponse(data)
    
#def contentInFolderxs
