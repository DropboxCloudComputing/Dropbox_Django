from rest_framework.views import APIView
from .serializers import *
from user_app.views import checkUser
from .models import Files
import itertools
from django.http import JsonResponse
from user_app.models import Users

class FileSearch(APIView):
    def get(self, request, **kwargs):
        sort = kwargs["sort_id"]
        user = checkUser(request)
        user = Users.objects.get(id = user.id)
        kwd = request.GET["kwd"]
        if kwd is None:
            filesQueryset = Files.objects.filter(user_id=user.id)
        else:
            filesQueryset = Files.objects.filter(user_id=user, file_name__icontains=kwd)

        serializer = FilesSerializer(filesQueryset, many=True)
        return JsonResponse(serializer.data, safe=False)