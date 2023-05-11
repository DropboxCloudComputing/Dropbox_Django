from rest_framework.views import APIView
from .models import Files
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

class FileList(APIView):
    serializer_class = FilesSerializer

    def get(self, request):
        model = Files.objects.all()
        serializer = FilesSerializer(model, many = True)
        return Response(serializer.data)

class MemoUpdate(APIView):
    serializer_class = FilesMemoSerializer
    
    def put(self, request, id):
        try:
            file = Files.objects.get(pk=id)
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FilesMemoSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)