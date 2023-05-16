from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Files(models.Model):
    #id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    size = models.IntegerField()
    favorites = models.BooleanField(default=False)
    folder_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    #user_id = models.ForeignKey(User, to_field = 'user_id', on_delete = models.CASCADE) 여기서 자꾸 오류 나는데
    user_id = models.AutoField(primary_key = True)
    memo = models.TextField(null=True)
    version = models.IntegerField(default=1)
    removed = models.BooleanField(default=False)
    s3key = models.CharField(max_length=255, null=True)

    class Meta:
        managed = True
        db_table = "files"