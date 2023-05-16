from django.urls import path
from . import views
from .views import FileDownloadView, Files, FileUploadView, FileRemovetoTrashView, FileRecoverfromTrashView, FilePermanentDeleteView, FileListView, FileDetailView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name="file-upload"),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),
    path('remove/<int:file_id>/', FileRemovetoTrashView.as_view(), name='file-remove'),
    path('recover/<int:file_id>/', FileRecoverfromTrashView.as_view(), name='file-recover'),
    path('delete/<int:file_id>/', FilePermanentDeleteView.as_view(), name='file-permanent-delete'),
    path('files/', FileListView.as_view(), name='file-show'),
    path('file/<int:file_id>', FileDetailView.as_view(), name='file-show-by-id'),
]
