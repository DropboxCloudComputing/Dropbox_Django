from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import SigninSirializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse  
import json

def login_view(request):
        if request.method == 'POST' :
            data = JSONParser().parse(request)
         
            email = data['email']
            # password = request.data['password']

            tokenData = SigninSirializer.validate(data)
            print(type(tokenData['user']))
            return JsonResponse({
                'user' : str(tokenData['user']),
                'refresh_token' : tokenData['refresh_token'],
                'access_token' : tokenData['access_token']
            })
        return JsonResponse({
              "message":"http error"
        })
# class UserLoginAPI(APIView):
#     def login_view(self, request):
#         email = request.data['email']
#         password = request.data['password']
#         obj = Users.objects.get(email=email)

#         data = SigninSirializer.validate(self, obj)

#         return data
    
    # if request.method == 'POST':
    #     data = JSONParser().parse(request)
        # search_email = data['email'] # email을 id로 사용
        # obj = Users.objects.get(email=search_email)

        # if Users.objects.filter(email=search_email) is None:
        #     return HttpResponse(status=300)
        # elif data['password'] != obj.password:
        #     return HttpResponse(status=400)

        # serializer = self.serializer_class(data=data)

        # if serializer.is_valid(raise_exception=False):
        #     user = serializer.validated_data['user']
        #     access = serializer.validated_data['access']
        #     refresh = serializer.validated_data['refresh']

        #     return JsonResponse({
        #     	'user': user,
        #         'access': access,
        #         'refresh': refresh
        #     })

            
        # else:
        #     return HttpResponse(status=400)


    

def logout(request):
        if request.method == 'POST' :
            response = JsonResponse({
                "message" : "success"
            })
        return response