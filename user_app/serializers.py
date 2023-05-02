from .models import Users
from rest_framework import serializers

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'password']