from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import boto3

User = get_user_model()

class TrashBin(models.Model):
    files_id = models.BigIntegerField(null= True)
    folder_id = models.BigIntegerField(null = True)
    users_id = models.BigIntegerField(primary_key = True)
    deleted_at = models.DateTimeField(auto_now_add = True)
    restored_at = models.DateTimeField(auto_now = True)

    def deleting_time(self, *args, **kwargs):
        self.deleted_at
        self.save()

    def recovering_time(self, *args, **kwargs):
        self.restored_at
        self.save()

    class Meta:
        managed = True
        db_table = "trashbin"

#     @classmethod
#     # 휴지통에 파일 넣기
#     def create_fl(cls, files_obj):
#         if files_obj.removed:
#             trashbin_obj = cls(files_id = files_obj.files_id, folder_id = files_obj.folder_id, users_id = files_obj.users_id)
#             trashbin_obj.save()
#             deleted_day = cls.deleted_at
#             return Response(status = 200)

#         now = datetime.now()
#         diff = now - deleted_day
#         if diff.days > 30:
#             files_obj.removed = False


#     # 휴지통에서 파일 복구
#     def restore_fl(cls, files_obj):
#         trashbin_obj = TrashBin.objects.get(files_id = files_obj.files_id)    
#         if files_obj.removed != True :
#             del trashbin_obj
#             TrashBin.objects.all().update()
#             return Response(status = 200)
        
        
#     # 휴지통에 폴더 넣기 - 폴더 안에 있는 파일들도 삭제...
#     # 폴더 안에 있는 파일이 여러 개면 파일 아이디도 여러 개...
#     def create_fd(cls, folder_obj, files_obj):
#         if folder_obj.removed:
#             trashbin_obj = cls(files_id = files_obj.files_id, folder_id = folder_obj.folder_id, users_id = folder_obj.users_id)
#             trashbin_obj.save()
#             deleted_day = cls.deleted_at
#             return Response(status = 200)
        
#         now = datetime.now()
#         diff = now - deleted_day
#         if diff.days > 30:
#             folder_obj.removed = False
#             files_obj.removed = False
#             # 폴더 안에 있는 모든 파일
#             cls.restore_fl(cls, files_obj)

#     # 휴지통에서 폴더 복구 - 폴더 안에 있는 파일들도 복구...    
#     def restore_fd(cls, folder_obj):
#         trashbin_obj = TrashBin.objects.get(folder_id = folder_obj.files_id)     
#         if folder_obj.removed != True :
#             #
#             del trashbin_obj
#             TrashBin.objects.all().update()
#             return Response(status = 200)





    





