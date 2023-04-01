
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from .forms import LoginForm
from .models import Users
    
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        if form.is_valid():
            id = form.data.get("id")
            raw_password = form.cleaned_data.get("password")
            user = Users.objects.get(password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
        id = form.data.get("id")
        raw_password = form.cleaned_data.get("password")
        user = Users.objects.get(password=raw_password)
        return render(request, "login.html", {"form": form, "msg": msg, "id": id, "user": user, "pw": form.errors})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})