from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import boto3

User = get_user_model()

class TrashBin(models.Model):
    files_id = models.BigIntegerField()
    files_name = models.CharField(max_length=255)
    folder_id = models.BigIntegerField(null = True)
    users_id = models.BigIntegerField(primary_key = True)
    deleted_at = models.DateTimeField(auto_now_add = True)
    restored_at = models.DateTimeField(auto_now = True)

    class Meta:
        managed = True
        db_table = "trashbin"









    





