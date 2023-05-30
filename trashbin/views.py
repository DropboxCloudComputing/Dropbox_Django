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

# 휴지통 안 모든 객체 정보 출력
class TrashBinListAPI(APIView):
    # This class for printing all objects in trashbin.
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            trash_list = TrashBin.objects.all()
            for obj in trash_list:
                print(obj.files_name, obj.files_id, obj.folder_id, sep = '\t', end = '\n')
            return Response(status=status.HTTP_200_OK)
        
        except TrashBin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            

# 휴지통 한번에 비움
class TrashBinClearAPI(APIView):
    # This class for clearing trashbin.
    permission_classes = [IsAuthenticated]
    def delete(self, request, format=None):
        try:
            trash_all = TrashBin.objects.all()
            # DB, S3에서 삭제
            trash_all.completely_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except TrashBin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 파일 삭제 API (파일을 휴지통에 넣음)
class FileRemoveAPI(APIView):
    # This class for removing file to Trash.
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, file_name, fd_id, user_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            file.removing()  # This will mark the file as removed

            # TrashBin에 해당 파일 저장
            trash_file = TrashBin(files_id = file_id, files_name = file_name, folder_id = fd_id, users_id = user_id)
            trash_file.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 파일 복구
class FileRecoverAPI(APIView):
    # This class for recoviring file from Trash
    permission_classes = [IsAuthenticated]
    def put(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            trash_file = TrashBin.objects.get(files_id=file_id)
            
            # 복구 시점과 삭제 시점의 차이가 30일 이하면 파일 복구, 휴지통에서 해당 파일 없애기.
            diff = trash_file.restored_at - trash_file.deleted_at
            if diff.days() <= 30:
                file.recover()  # This will mark the file as recovered

                # trashbin에서 해당 파일 삭제
                trash_file.delete()       
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            # 30일 초과면 복구 불가
            else:
                # 휴지통에서 삭제
                # 파일 영구 삭제 -> response ?
                trash_file.delete()
                return Response({"detail": "File cannot be restored."}, status=status.HTTP_404_NOT_FOUND)
            
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
   
# 즉시 영구 삭제
class FilePermanentlyDeleteAPI(APIView):
    # This class for completely deleting file from s3 and db
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            trash_file = TrashBin.objects.get(files_id=file_id)
            
        except Files.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the completely_delete method to delete the file
        file.completely_delete()
        trash_file.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)






