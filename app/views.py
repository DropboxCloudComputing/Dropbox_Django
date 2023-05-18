from rest_framework.views import APIView
from .models import Files
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

class FileList(APIView):
    serializer_class = FilesSerializer

    def get(self, request):
        sort = request.query_params.get('sort', None)
        
        #파일을 이름, 사이즈, 즐겨찾기, 조회된 순서 로 가져옴 ## default 는 id 순서대로
        if sort == 'name':
            files = Files.objects.all().order_by('-file_name')
        
        elif sort == 'size':
            files = Files.objects.all().order_by('-size')
        
        elif sort == 'favorites':
            files = Files.objects.all().order_by('-favorites')
        
        elif sort == 'view_count':
            files = Files.objects.all().order_by('-view_count')
        
        else:
            files = Files.objects.all()
            
        serializer = FilesSerializer(files, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FileDetail(APIView):
    def get(self, request, id):
        try:   
            model = Files.objects.get(id = id)            
            model.increase_view_count()
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializers = FilesSerializer(model)
        return Response(serializers.data)
    
class FileFavoriteToggle(APIView):
    def put(self, request, id):
        try:
            file = Files.objects.get(id=id)
        except Files.DoesNotExist:
            return Response({'message': 'The file does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        file.favorites = not file.favorites  # favorites 값을 반전시킴
        file.save()
        
        return Response({'message': 'Favorites toggled successfully', 'favorites': file.favorites}, status=status.HTTP_200_OK)     
    
class MemoList(APIView):
    serializer_class = MemoSerializer

    def get(self, request):
        model = Files.objects.all().values('id', 'memo', 'last_modified')
        serializer = MemoSerializer(model, many = True)
        return Response(serializer.data)

class MemoDetail(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
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

