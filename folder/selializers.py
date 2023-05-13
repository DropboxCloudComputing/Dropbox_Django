from .models import Folder, Permission
from rest_framework import serializers

class FolderSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(max_length=45)
    folder_id = serializers.IntegerField(read_only = True)

    class Meta(object):
        model = Folder
        fields = ['folder_name', 'folder_id']
