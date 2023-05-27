from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name="file-upload"),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),

    # path('files/', FileListView.as_view(), name='file-show'),
    # path('file/<int:file_id>', FileDetailView.as_view(), name='file-show-by-id'),
    path('remove/<int:file_id>/', FileRemovetoTrashView.as_view(), name='file-remove'),
    path('recover/<int:file_id>/', FileRecoverfromTrashView.as_view(), name='file-recover'),
    path('delete/<int:file_id>/', FilePermanentDeleteView.as_view(), name='file-permanent-delete'),
    path('files/', FileList.as_view(), name = 'File_list'),
    path('files/<int:id>' , FileDetail.as_view(), name = 'File_detail'),
    path('memos/<int:id>' , MemoDetail.as_view(), name = 'Memo_Detail'),
    path('memos' , MemoList.as_view(), name = 'Memo_list'), 
    path('files/<int:id>/favorite/', FileFavoriteToggle.as_view(), name='file-favorite-toggle'),
#    path('file-search/<int:sort_id>', FileSearch.as_view(), name='file-search'),

]