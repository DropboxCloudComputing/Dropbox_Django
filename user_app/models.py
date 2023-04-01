from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

 
    USERNAME_FIELD = 'id'  # 로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['id','password'] # 필수 작성 필드

    class Meta:
        managed = False
        db_table = 'users'
