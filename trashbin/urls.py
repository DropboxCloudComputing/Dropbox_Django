from django.urls import path
from . import views
from .views import FileRemovetoTrashView, FileRecoverfromTrashView, FilePermanentDeleteView


urlpatterns = [
    path('remove/<int:file_id>/', FileRemovetoTrashView.as_view(), name='file-remove'),
    path('recover/<int:file_id>/', FileRecoverfromTrashView.as_view(), name='file-recover'),
    path('delete/<int:file_id>/', FilePermanentDeleteView.as_view(), name='file-permanent-delete'),
]