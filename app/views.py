from rest_framework.views import APIView
from .models import Files
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

class FileList(APIView):
    serializer_class = FilesSerializer
    # 파일을 정렬해서 보여주는 메소드
    def get(self, request):
        sort_by = request.query_params.get('sort_by', 'id')
        sort_order = request.query_params.get('sort_order', 'asc')
                
        #파일을 이름, 사이즈, 즐겨찾기, 조회된 순서 로 가져옴 ## default 는 id 순서대로
        if sort_by == 'name':
            sort_field = 'file_name'
        
        elif sort_by == 'size':
            sort_field = 'size'
        
        elif sort_by == 'favorites':
            sort_field = 'favorites'
        
        elif sort_by == 'view_count':
            sort_field = 'view_count'
        
        #기본 정렬은 id 순서대로
        else:
            sort_field = 'id'
            
        # 정렬 방식에 따라 정렬 수행
        if sort_order == 'desc':
            sort_field = '-' + sort_field  # 내림차순 정렬을 위해 '-' 추가
            
        #api/file_list/?sort_by=name&sort_order=desc
        
        files = Files.objects.all().order_by(sort_field)
        serializers = FilesSerializer(files, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

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

