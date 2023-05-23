from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.Serializer) :
    username = None
    last_login = None
    # id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=45)
    email = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=45)
    # token = serializers.CharField()

    # class Meta:
    #     model=Users
    #     fields = ['id', 'full_name', 'email','password']

    def create(self, validated_data):
        return Users.objects.create(**validated_data)
