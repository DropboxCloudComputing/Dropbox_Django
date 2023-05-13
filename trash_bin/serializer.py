from rest_framework import serializers
from .models import TrashBin

class TrashBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrashBin
        fields = '__all__'