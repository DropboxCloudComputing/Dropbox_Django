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
    
class FileDetail(APIView):
    def get(self, request, id):
        try:   
            model = Files.objects.get(id = id)            
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializers = FilesSerializer(model)
        return Response(serializers.data)
    
class MemoList(APIView):
    serializer_class = MemoSerializer

    def get(self, request):
        model = Files.objects.all().values('id', 'memo')
        serializer = MemoSerializer(model, many = True)
        return Response(serializer.data)

class MemoDetail(APIView):
    serializer_class = MemoSerializer
    
    def get(self, request, id):
        try:   
            model = Files.objects.get(id = id)      
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializers = FilesSerializer(model)
        return Response(serializers.data)
    
    def put(self, request, id):
        try:
            model = Files.objects.get(id = id)
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        serializers = MemoSerializer(model, data=request.data, partial = True)
        
        if serializers.is_valid():
            model.last_modified = timezone.now()
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        Memo = Files.objects.get(id = id)
        Memo.memo =''
        Memo.last_modified = timezone.now()
        serializers = MemoSerializer(Memo, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

