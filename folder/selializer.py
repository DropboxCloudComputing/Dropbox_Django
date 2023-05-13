from .models import Folder, Permission
from rest_framework import serializers

class FolderSirializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = "__all__"

class SharedFolderSirializer(serializers.ModelSerializer):
    class Meta(object):
        model = Permission
        fields = "__all__"

class GetSharedFolderSirializer(serializers.ModelSerializer):
    folder = FolderSirializer(many = True, read_only=True)
    class Meta(object):
        model = Permission
        fields = ['folder']

