from django.urls import path, include
from . import views

urlpatterns = [
    path("share/", views.shareFolder),
    path("get/sharedfolder/", views.getSharedFolders),
    path("create/", views.folderCreate),
    path("delete/", views.folderDelete),
    path("verify/", views.folderVerifyName),
    path("getContents/", views.contentsInFolder)
]