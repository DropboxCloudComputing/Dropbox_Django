from django import forms
from django.contrib.auth.models import User
from . import models

# class SignUpForm(forms.Form) : 
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField()
#      #비밀번호
#     password = models.CharField(widget=forms.PasswordInput, max_length=255)
#     #비밀번호 확인
#     password1 = models.CharField(widget=forms.PasswordInput, label="Confirm Password", max_length=255) 