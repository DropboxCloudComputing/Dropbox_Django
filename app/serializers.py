from rest_framework import serializers
from .models import Files, Memo
from django.utils import timezone
import os


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Files
        fields = ('id',  'favorites', 'folder_id', 'memo', 'version', 's3key', 'file')
        read_only_fields = ('id', 'favorites', 'version', 'removed')

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
        file = validated_data.pop('file')
        print(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data): 
        instance.memo = validated_data.get('memo', instance.memo)
        instance.last_modified = timezone.now()
        instance.save()
        return instance
    


class FileDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id',)
        read_only_fields = ('id', 'favorites', 'folder_id', 'created_at', 'last_modified', 'user', 'memo', 'version', 's3key', 'removed')

    def update(self, instance, validated_data):
        instance.removed = True
        instance.save()
        return instance

    def validate(self, attrs):
        user = self.context['request'].user

        if user != attrs['user']:
            raise serializers.ValidationError("You don't have permission to delete this file.")

        return attrs
    
    
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files 
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'last_modified')
        
        
        
class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ('id', 'memo')
        read_only_fields = ('id',)
        
'''    def update(self, instance, validated_data):
        instance.memo = validated_data.get('memo', instance.memo)
        instance.last_modified = timezone.now()
        instance.save()
        return instance
    
    def delete(self, instance, validated_data):
        instance.memo = ""
        return instance
'''
    
