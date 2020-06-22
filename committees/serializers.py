from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *


class CommitteeSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)
    def create(self, validated_data):
        committee = Committee.objects.create(**validated_data) 
        return committee

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Committee          
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    committeeName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        note = Note.objects.create(**validated_data) 
        return note

    def update(self, instance, validated_data):
        instance.save()
        return instance
    
    class Meta:
        model = Note          
        fields = '__all__'

class PositionSerializer(ModelSerializer):

    def create(self, validated_data):
        position = Position.objects.create(**validated_data) 
        return position

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Position          
        fields = '__all__'       