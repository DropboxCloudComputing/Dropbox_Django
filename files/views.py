from http.client import NOT_FOUND
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileSerializer, FileUploadSerializer
from .models import Files
import boto3
import string
import random

## This is a random string generator
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class FileUploadView(APIView):
    # File Upload
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            file = request.FILES['file']
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3_bucket_name = 'suhron'
            s3_name = f"{id_generator(10)}.{file.name}"
            s3_client.upload_fileobj(file, s3_bucket_name, s3_name)
            s3_url =  f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_name}"
            serializer.validated_data['s3key'] = s3_url
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDownloadView(APIView):
    # File Download
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        # Retrieve the file object based on the file_id
        try:
            file = Files.objects.get(id=file_id, user_id=request.user)
        except Files.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the S3 key for the file
        s3_key = file.s3key.split('/')[-1]
        print(s3_key)
        # Download the file from S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        s3_bucket_name = 'suhron'
        file_obj = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_key)

        # Prepare the file response
        response = FileResponse(file_obj['Body'].read())
        response['Content-Disposition'] = f'attachment; filename="{file.file_name}"'

        return response


class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all files from the database
        files = Files.objects.all()

        # Serialize the files
        serializer = FileSerializer(files, many=True)

        # Return the serialized data as the response
        return Response(serializer.data)


class FileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, file_id):
        try:
            file = Files.objects.get(id=file_id)
            file.watched()
            files = Files.objects.filter(file_name=file.file_name).order_by('-version')
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)
        except Files.DoesNotExist:
            raise NOT_FOUND("File not found.")
        

### Trash Functions

class FileRemovetoTrashView(APIView):
    # This class for removing file to Trash
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            file.removing()  # This will mark the file as removed
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class FileRecoverfromTrashView(APIView):
    # This class for recoviring file from Trash
    permission_classes = [IsAuthenticated]
    def put(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
            file.recover()  # This will mark the file as recovered
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Files.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class FilePermanentDeleteView(APIView):
    # This class for completely deleting file from s3 and db
    permission_classes = [IsAuthenticated]
    def delete(self, request, file_id, format=None):
        try:
            file = Files.objects.get(id=file_id)
        except Files.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        # Call the completely_delete method to delete the file
        file.completely_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

