from rest_framework import serializers
from .models import Files
import os


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Files
        fields = ('id', 'favorites', 'folder_id', 'created_at', 'last_modified', 'memo', 'version', 'removed', 's3key', 'clicked', 'file')

        extra_kwargs = {
            'file_name': {'write_only': True},
            'size': {'write_only': True},
        }


    def create(self, validated_data):
        print(validated_data)
        validated_data['user_id'] = self.context['request'].user

        file = self.context['request'].FILES['file']
        validated_data['file_name'] = file.name
        validated_data['size'] = file.size
        existing_files = Files.objects.filter(file_name=file.name, user_id=validated_data['user_id'])
        if existing_files.exists():
            # Get the latest version
            latest_version = existing_files.latest('version').version
            # Increment the version by 1
            validated_data['version'] = latest_version + 1

        file = validated_data.pop('file')
        print(validated_data)
        return super().create(validated_data)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('__all__')