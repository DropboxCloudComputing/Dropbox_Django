from django.urls import path
from . import views
from .views import FileDownloadView, Files, FileUploadView, FileListView, FileDetailView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name="file-upload"),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),
    path('files/', FileListView.as_view(), name='file-show'),
    path('file/<int:file_id>', FileDetailView.as_view(), name='file-show-by-id'),
]