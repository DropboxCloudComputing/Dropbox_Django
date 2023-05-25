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






# from django.core.files.storage import FileSystemStorage
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from datetime import datetime
# from pytz import timezone
# from rest_framework.views import APIView
# from app.models import Files, Folder
# from .models import TrashBin
# from datetime import datetime


# # 파일 삭제 옵션 - 파일 삭제, 파일 복구, 파일 영구 삭제 
# class File_DeleteOpions(APIView):
#     # 파일 삭제
#     def delete_file(self, file_id):    
#         file_object = Files.objects.get(id = file_id)
#         file_object.removed = True
#         TrashBin.create_fl(self, file_object)
#         # 보관 기간 30일 
#         now = datetime.now()
        
#     # 파일 복구
#     def restore_file(self, file_id):
#         file_object = Files.objects.get(id = file_id)
#         file_object.removed = False
#         TrashBin.restore_fl(self, file_object)
        
#     # 파일 영구삭제 (DB에서 삭제)
#     @api_view(['DELETE'])
#     def delete_permanently_file(request, file_id):
#         data = Files.objects.get(id = file_id)
#         data.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)

    
# # 폴더 삭제, 폴더 복구, 폴더 영구 삭제    
# class Folder_DeleteOptions(APIView):
#     # 폴더 삭제할 때 그 안에 파일도 삭제
#     def delete_folder(self, fd_id):
#         folder_object = Folder.objects.get(id = fd_id)
#         folder_object.removed = True
#         TrashBin.create_fl(self, folder_object)
#         # 보관 기간 30일
    
#     # 폴더 복구, 그 안에 있는 파일도 복구
#     def restore_file(self, fd_id):
#         folder_object = Folder.objects.get(id = fd_id)
#         folder_object.removed = False
#         TrashBin.restore_fd(self, folder_object)

#     # 폴더 영구 삭제, 그 안에 있는 파일도 영구 삭제
#     @api_view(['DELETE'])
#     def delete_permanently_folder(request, fd_id):
#         data = Folder.objects.get(folder_id = fd_id)
#         data.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)
