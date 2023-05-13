from django.urls import path, include
from . import views

urlpatterns = [
    path("share/", views.shareFolder),
    path("get/sharedfolder/", views.getSharedFolders),
]