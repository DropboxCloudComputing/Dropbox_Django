from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Users(AbstractBaseUser):
    username = None
    last_login = None
    id = models.CharField(primary_key=True, max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

 
    USERNAME_FIELD = 'email'  # 로그인 ID로 이메일 사용(Id 필드)
    REQUIRED_FIELDS = ['password'] # 필수 작성 필드

    class Meta:
        managed = False
        db_table = 'users'

    # def __init__ (self, id, full_name, email, password):
    #     self.id = id
    #     self.full_name = full_name
    #     self.email = email
    #     self.password = password
