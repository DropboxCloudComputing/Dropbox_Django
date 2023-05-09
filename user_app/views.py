from django.contrib.auth import authenticate#, login
from django.http import HttpResponse
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from .serializers import SigninSirializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .forms import UserCreateForm
from django.shortcuts import redirect, render
from django.contrib import messages



def login_view(request):
        if request.method == 'POST' :
            data = JSONParser().parse(request) # password = request.data['password']
            tokenData = SigninSirializer.validate(data)

            email = data['email']
            user = Users.objects.get(email = email)
            SigninSirializer.update(user, tokenData
                                    )
            response = JsonResponse({
                'user' : str(tokenData['user']),
                'access_token' : tokenData['access_token'],
                'refresh_token': tokenData['refresh_token']
            })

            return response
        
        return JsonResponse({
              "message":"http error"
        })
  


def logout(request):

    if request.method == 'POST' :
        response = JsonResponse({
            "ResponseCode":200,
            "message" : "success"
        })
    else:
         response = JsonResponse({
            "message" : "error"
        })
    return response


def signup(request):
    # 입력된 정보로 회원가입 폼 셍상
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            username = form.cleaned_data.get('full_name')
            raw_password = form.cleaned_data.get('password1')
            # 추가 정보 저장
            user = Users.objects.create(id=form.id,
                                        full_name=form.username,
                                        email=request.POST['email'],
                                        password=form.password,
                                        created_at=form.date_joined,
                                        updated_at=form.date_joined
                                        )
            user.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            # # 사용자 인증
            # user = authenticate(username=username, password=raw_password)
            # # 회원가입 완료 후 로그인
            # login(request, user)
            # return redirect('index')
            return redirect('login_view')
    else:
        form = UserCreateForm()
    return render(request, 'user_app/signup.html', {'form': form})
