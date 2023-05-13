from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import TrashBin, Files
from .serializers import FilesSerializer, TrashBinSerializer

class TrashBinSearchAPI(APIView):
    def get(self, request):
        token = request.query_params.get('token', None)
        if not token:
            return Response({'responsecode': '400', 'description': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Token 유효성 검사 로직

        trashbin_objs = TrashBin.objects.filter(users_id=request.user.id)
        serializer = TrashBinSerializer(trashbin_objs, many=True)

        return Response({'responsecode': '200', 'description': 'Success', 'trashbin': serializer.data}, status=status.HTTP_200_OK)

'''
@login_required
@api_view(['POST'])
def trashbinClear(request):
    token = request.data.get('token', None)
    if not token:
        return Response({'responsecode': 'FAILURE', 'description': 'Token is required.'})
    
    # 유효한 토큰인지 확인하는 로직
    
    TrashBin.objects.all().delete()
    return Response({'responsecode': 'SUCCESS', 'description': 'Trashbin is cleared.'})

@login_required
@api_view(['POST'])
def restoreFile(request):
    token = request.data.get('token', None)
    file_id = request.data.get('file_id', None)
    if not token:
        return Response({'responsecode': 'FAILURE', 'description': 'Token is required.'})
    if not file_id:
        return Response({'responsecode': 'FAILURE', 'description': 'File ID is required.'})
    
    # 유효한 토큰인지 확인하는 로직
    
    trashbin_obj = get_object_or_404(TrashBin, files_id=file_id)
    # 복구 로직
    trashbin_obj.delete()
    
    return Response({'responsecode': 'SUCCESS', 'description': 'The file is restored.'})

@login_required
@api_view(['POST'])
def restoreFolder(request):
    token = request.data.get('token', None)
    folder_id = request.data.get('folder_id', None)
    if not token:
        return Response({'responsecode': 'FAILURE', 'description': 'Token is required.'})
    if not folder_id:
        return Response({'responsecode': 'FAILURE', 'description': 'Folder ID is required.'})
    
    # 유효한 토큰인지 확인하는 로직
    
    TrashBin.objects.filter(folder_id=folder_id).delete()
    
    return Response({'responsecode': 'SUCCESS', 'description': 'The folder is restored.'})

@login_required
@api_view(['POST'])
def trashbinDeleteFile(request):
    token = request.data.get('token', None)
    file_id = request.data.get('file_id', None)
    if not token:
        return Response({'responsecode': 'FAILURE', 'description': 'Token is required.'})
    if not file_id:
        return Response({'responsecode': 'FAILURE', 'description': 'File ID is required.'})
    
    # 유효한 토큰인지 확인하는 로직
'''