from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('print', TrashBinListAPI.as_view(), name = 'trashbin-list-print'), 
    path('clear', TrashBinClearAPI.as_view(), name = 'trashbin-clear'),
    path('remove/<int:file_id>/', FileRemoveAPI.as_view(), name='file-remove'),
    path('recover/<int:file_id>/', FileRecoverAPI.as_view(), name='file-recover'),
    path('delete/<int:file_id>/', FilePermanentlyDeleteAPI.as_view(), name='file-permanently-delete'),
]