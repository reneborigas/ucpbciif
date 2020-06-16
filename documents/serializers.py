from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *

from documents.models import * 
from committees.models import Committee
from processes.models import Statuses,Step,Output
from processes.serializers import OutputSerializer
from committees.serializers import NoteSerializer

class DocumentSerializer(ModelSerializer):
    subProcessName = serializers.CharField(read_only=True)
    documentTypeName = serializers.CharField(read_only=True)
    borrowerName = serializers.CharField(read_only=True)
    documentCode = serializers.CharField(read_only=True)
    notes = NoteSerializer(many=True)
    
    def create(self, validated_data): 
        
        committee = Committee.objects.get(pk=validated_data.get("committee", "1"))

        status = Statuses.objects.get(pk=1)

        document = Document.objects.create(**validated_data) 
        # document.code = document.subProcess.code + ("%03d" % document.id)
        # document.save()
        
        steps = Step.objects.filter(subProcess=document.subProcess) 
        step = steps.order_by('order').first()


        documentMovement = DocumentMovement(
        document = document ,name = step.name, committee= committee , status=status,step=step)
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



class DocumentMovementSerializer(ModelSerializer): 
    committeeName = serializers.CharField(read_only=True)
    statusName = serializers.CharField(read_only=True) 
    documentId = serializers.CharField(read_only=True)
    stepId = serializers.CharField(read_only=True)
    outputName= serializers.CharField(read_only=True)
    output= OutputSerializer(read_only=True)
    outputId= serializers.CharField()


    def create(self, validated_data): 
         
        document = Document.objects.get(pk=validated_data.get("document").id)
        outputId =  validated_data.get("outputId")
        print(outputId)
        output = Output.objects.get(id=outputId) 
        
        committee = Committee.objects.get(pk=validated_data.get("committee", "1").id)
        remarks = validated_data.get("remarks", "")
        documentMovement = DocumentMovement(
        document = document ,name = output.step.name,output=output, committee= committee , status=output.step.status,step=output.step,remarks=remarks)

        documentMovement.save()

        
        return documentMovement
 
    

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = DocumentMovement          
        fields = '__all__'