from .models import TrashBin
from rest_framework import serializers

class TrashBinSerializer(serializers.ModelSerializer):
    # files_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()
    users_id = serializers.IntegerField()
    class Meta(object):
        model = TrashBin
        fields = ['folder_id', 'users_id']