from django.urls import path
from .views import FileSearch

urlpatterns = [
    path('file-search/<int:sort_id>', FileSearch.as_view(), name='file-search'),
]