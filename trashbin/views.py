from http.client import NOT_FOUND
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from files.models import Files
from .models import TrashBin
from datetime import datetime
import boto3
import string
import random


### TrashBin Functions
class FileRemovetoTrashView(APIView):
    # This class for removing file to Trash
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            file.removing()  # This will mark the file as removed
            trash_file = TrashBin(files_id = file_id)
            trash_file.deleting_time
            trash_file.save() # trashbin에 저장
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FileRecoverfromTrashView(APIView):
    # This class for recoviring file from Trash
    permission_classes = [IsAuthenticated]
    def put(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            file.recover()  # This will mark the file as recovered
            TrashBin(files_id = file_id).delete()   # trashbin에서 삭제
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # 복구 기간 30일 추가
    permission_classes = [IsAuthenticated]
    def auto_put(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            trash_file = TrashBin.objects.get(id=file_id)
            trash_file.save()
            diff = trash_file.recovering_time - trash_file.deleting_time
            if diff.days() > 30:
                file.recover()
                TrashBin(files_id = file_id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FilePermanentDeleteView(APIView):
    # This class for completely deleting file from s3 and db
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
        except Files.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the completely_delete method to delete the file
        file.completely_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




