#from django.shortcuts import render
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from .serializers import *
#from rest_framework import status
#import boto3

from django.conf import settings
from dropbox.settings import USE_S3
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from app.models import Upload
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

@api_view(['POST'],)
def image_upload(request):
    if request.method == 'POST':
        image_file = request.FILES['image_file']
        image_type = request.POST['image_type']
        if True:
            upload = Upload(file = image_file,uploaded_at = datetime.now())
            upload.save()
            image_url = upload.file.url
        else:
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
        return Response(image_url,status=status.HTTP_200_OK)
    return Response(None,status=status.HTTP_400_BAD_REQUEST)

#class Image(APIView):
    #def post(self, request, format=None):
        #serializers = PhotoSerializer(data = request.data)
        #if serializers.is_valid():
            #serializers.save()
            #return Response(serializers.data, status = status.HTTP_201_CREATED)
        #return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)