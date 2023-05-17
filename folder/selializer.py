from .models import Folder, Permission
from rest_framework import serializers
# from user_app import UserSerializer

class FolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Folder
        fields = "__all__"

class SharedFolderSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Permission
        fields = "__all__"

class GetSharedFolderSerializer(serializers.ModelSerializer):
    folder = FolderSerializer(many = True, read_only=True)
    class Meta(object):
        model = Permission
        fields = ['folder']

class CreateFolderSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(max_length=45)
    # users = UserSerializer()
    # pfolder = FolderSerializer() #(many = True)

    def create(self, validated_data):
        return Folder.objects.create(**validated_data)
    class Meta(object):
        model = Folder
        fields = ['folder_name', 'users','pfolder']