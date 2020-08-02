from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
 


class NoteSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        notification = Notification.objects.create(**validated_data) 
        return notification

    def update(self, instance, validated_data):
        instance.save()
        return instance
    
    class Meta:
        model = Notification          
        fields = '__all__'
 