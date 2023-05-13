from django.db import models
from app.models import Files
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

'''
class Files(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    size = models.IntegerField()
    favorites = models.BooleanField(default=False)
    folder_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    memo = models.TextField(null=True)
    version = models.IntegerField(default=1)
    removed = models.BooleanField(default=False)
    s3key = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True
        db_table = "files"
'''
        
class TrashBin(models.Model):
    id = models.BigAutoField(primary_key=True)
    files_id = models.BigIntegerField()
    folder_id = models.BigIntegerField(null=True)
    users_id = models.BigIntegerField()
    deleted_at = models.DateTimeField(default=timezone.now)
    
    @classmethod
    def create(cls, files_obj):
        if files_obj.removed:
            trashbin_obj = cls(files_id=files_obj.id, folder_id=files_obj.folder_id, users_id=files_obj.user_id.id)
            trashbin_obj.save()
        else :
            print(" instance not removed ")
    # files_obj = Files.objects.create(file_name='example.txt', size=1024, favorites=True, folder_id=1, user_id=user_obj, memo='example memo', version=1, removed=True)
    # Trashbin.create(files_obj)
