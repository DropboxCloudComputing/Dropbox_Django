# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
from django.contrib.auth.models import User
from .models import Users
from django.shortcuts import redirect, render

# 회원가입 폼 처리하는 뷰 함수
def signup(request) :
    # 입력된 정보로 회원가입 폼 셍상
    if request.method == "POST" : 
        user_form = User.objects.create_user(
            username= request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        # 추가 정보 저장
        user = Users.objects.create(id=user_form.id,
                                    full_name=user_form.username,
                                    email=request.POST['email'],
                                    password=user_form.password,
                                    created_at=user_form.date_joined,
                                    updated_at=user_form.date_joined
                                    )
        # 회원가입 완료 후 로그인 페이지로 이동
        return redirect('login')
    return render(request, 'user_app/signup.html')