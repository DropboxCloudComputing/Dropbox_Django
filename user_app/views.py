from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import LoginSerializer
from rest_framework.parsers import JSONParser

def login_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_id = data['id']
        obj = Users.objects.get(id=search_id)

        if data['password'] == obj.password:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)