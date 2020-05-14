from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class GenderTypeSerializer(ModelSerializer):
    class Meta:
        model = GenderType
        fields = '__all__'