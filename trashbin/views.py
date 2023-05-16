from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from pytz import timezone
from rest_framework.views import APIView
from app.models import Files, Folder
from .models import TrashBin

# 파일 삭제 옵션 - 파일 삭제, 파일 복구, 파일 영구 삭제 / 폴더 삭제, 폴더 복구, 폴더 영구 삭제 
class DeleteOpions:
    # 파일 삭제
    def delete_file(self, file_id):    
        file_object = Files.objects.get(id = file_id)
        file_object.removed = True
        TrashBin.create_fl(self, file_object)
        # 기간 보관 ... !

    # 파일 복구
    def restore_file(self, file_id):
        file_object = Files.objects.get(id = file_id)
        file_object.removed = False
        TrashBin.restore_fl(self, file_object)
        
    # 파일 영구삭제 (DB에서 삭제)
    @api_view(['DELETE'])
    def delete_permanently_file(request, file_id):
        data = Files.objects.get(id = file_id)
        data.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    # 폴더 삭제할 때 그 안에 파일도 삭제
    def delete_folder(self, fd_id):
        folder_object = Folder.objects.get(id = fd_id)
        folder_object.removed = True
        TrashBin.create_fl(self, folder_object)
    
    # 폴더 복구, 그 안에 있는 파일도 복구
    def restore_file(self, fd_id):
        folder_object = Folder.objects.get(id = fd_id)
        folder_object.removed = False
        TrashBin.restore_fd(self, folder_object)

    # 폴더 영구 삭제, 그 안에 있는 파일도 영구 삭제
    @api_view(['DELETE'])
    def delete_permanently_folder(request, fd_id):
        data = Folder.objects.get(folder_id = fd_id)
        data.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
