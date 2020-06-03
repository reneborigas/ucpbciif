from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *

from documents.models import * 
from committees.models import Committee
from processes.models import Statuses

class DocumentSerializer(ModelSerializer):
    subProcessName = serializers.CharField(read_only=True)
    documentTypeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    def create(self, validated_data): 
        
        committee = Committee.objects.get(pk=validated_data.get("committee", "1"))

        status = Statuses.objects.get(pk=1)

        document = Document.objects.create(**validated_data) 
        documentMovement = DocumentMovement(
        document = document ,name = document.name + " Created", committee= committee , status=status)
        documentMovement.save()
 
        return document
 
    

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Document          
        fields = '__all__'