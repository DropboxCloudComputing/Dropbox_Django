from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Users(AbstractBaseUser):
    username = None
    last_login = None
    id = models.BigIntegerField(primary_key=True)
    full_name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

 
    USERNAME_FIELD = 'email'  # 로그인 ID로 이메일 사용(Id 필드)
    REQUIRED_FIELDS = ['password'] # 필수 작성 필드

    class Meta:
        managed = False
        db_table = 'users'

