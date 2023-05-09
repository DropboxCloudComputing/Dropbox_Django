from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Users


class UserCreateForm(UserCreationForm):
    full_name = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ["full_name", "email", "password1"]#username, password1

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data("email")
        if commit:
            user.save()
        return user