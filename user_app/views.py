from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import LoginSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse  

def login_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_email = data['email'] # email을 id로 사용
        obj = Users.objects.get(email=search_email)
        
        if data['password'] == obj.password:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

def logout(request):
    if request.method == 'POST' :
        response = JsonResponse({
            "message" : "success"
        })
    return response