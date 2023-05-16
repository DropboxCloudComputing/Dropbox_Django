from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from files.models import Files
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from pytz import timezone
from rest_framework.views import APIView
from files.serializers import FileUploadSerializer


# 파일 리스트 
class FileList(APIView):      
    def get(self, request, format=None):
        files = Files.objects.filter(user_id = self.request.user.id)
        serializer = FileUploadSerializer(files,many = True)
        return Response(serializer.data)