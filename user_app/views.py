from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import SigninSirializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse  


def login_view(request):
        if request.method == 'POST' :
            data = JSONParser().parse(request) # password = request.data['password']
            tokenData = SigninSirializer.validate(data)

            response = JsonResponse({
                'user' : str(tokenData['user']),
                'refresh_token' : tokenData['refresh_token'],
                'access_token' : tokenData['access_token']
            })
            response.set_cookie('access_token', tokenData['access_token']) # cookie로 header에 access token 보냄

            return response
        
        return JsonResponse({
              "message":"http error"
        })
  

def logout(request):
        if request.method == 'POST' :
            response = JsonResponse({
                "message" : "success"
            })
            response.set_cookie('access_token', '') #header cookie정보 비우기
        return response