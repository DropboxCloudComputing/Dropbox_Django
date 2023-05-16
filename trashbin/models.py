from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.models import Files, Folder
from rest_framework.response import Response

User = get_user_model()

class TrashBin(models.Model):
    files_id = models.BigIntegerField()
    folder_id = models.BigIntegerField(null = True)
    users_id = models.BigIntegerField(primary_key = True)
    deleted_at = models.DateTimeField(default = timezone.now)
    restored_at = models.DateTimeField(default = timezone.now)

    class Meta:
        managed = True
        db_table = "trashbin"

    @classmethod
    # 휴지통에 파일 넣기 ---> 버전 처리 / 보관 기간 해결
    def create_fl(cls, files_obj):
        if files_obj.removed:
            trashbin_obj = cls(files_id = files_obj.files_id, folder_id = files_obj.folder_id, users_id = files_obj.users_id)
            trashbin_obj.save()
            return Response(status = 200)


    # 휴지통에서 파일 복구
    def restore_fl(cls, files_obj):
        trashbin_obj = TrashBin.objects.get(files_id = files_obj.files_id)     
        if files_obj.removed != True :
            del trashbin_obj
            TrashBin.objects.all().update()
            return Response(status = 200)
        
    # 휴지통에 폴더 넣기 - 폴더 안에 있는 파일들도 삭제...
    # 폴더 안에 있는 파일이 여러 개면 파일 아이디도 여러 개...
    def create_fd(cls, folder_obj, files_obj):
        if folder_obj.removed:
            trashbin_obj = cls(files_id = files_obj.files_id, folder_id = folder_obj.folder_id, users_id = folder_obj.users_id)
            trashbin_obj.save()
            return Response(status = 200)

    # 휴지통에서 폴더 복구 - 폴더 안에 있는 파일들도 복구...    
    def restore_fd(cls, folder_obj):
        trashbin_obj = TrashBin.objects.get(folder_id = folder_obj.files_id)     
        if folder_obj.removed != True :
            del trashbin_obj
            TrashBin.objects.all().update()
            return Response(status = 200)





    





