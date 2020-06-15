from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from committees.serializers import PositionSerializer

class SubProcessSerializer(ModelSerializer):
     
    def create(self, validated_data):
        loan = SubProcess.objects.create(**validated_data) 
        return loan

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = SubProcess          
        fields = '__all__'

class OutputSerializer(ModelSerializer):
    stepName = serializers.CharField(read_only=True)
    stepStatus = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        output = Output.objects.create(**validated_data) 
        return output

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Output          
        fields = '__all__'       
        
class StepSerializer(ModelSerializer):
    outputs = OutputSerializer(many=True,required=False)
    position = PositionSerializer(many=True,required=False)
    def create(self, validated_data):
        step = Step.objects.create(**validated_data) 
        return step

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Step          
        fields = '__all__'   
        
class StepRequirementAttachmentSerializer(ModelSerializer):
    def create(self, validated_data):
        stepRequirementAttachment = StepRequirementAttachment.objects.create(**validated_data) 
        
        return stepRequirementAttachment

    def update(self, instance, validated_data):
        instance.save()

        return instance
    
    class Meta:
        model = StepRequirementAttachment          
        fields = '__all__'   
        
class StepRequirementSerializer(ModelSerializer):
    isRequiredText = serializers.CharField(read_only=True)
    stepRequirementAttachments =StepRequirementAttachmentSerializer(many=True,required=False)
    def create(self, validated_data):
        stepRequirement = StepRequirement.objects.create(**validated_data) 

        return stepRequirement

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = StepRequirement          
        fields = '__all__'   
