from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from committees.serializers import PositionSerializer 
from loans.serializers import LoanSerializer, CreditLineSerializer

class RelatedProcessSerializer(serializers.ModelSerializer):
    relatedProcesses = serializers.PrimaryKeyRelatedField(queryset=SubProcess.objects.all(), many=True)

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
    positions = PositionSerializer(many=True,required=False)
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

class SubProcessSerializer(ModelSerializer): 
    canCreateNewFile = serializers.CharField(read_only=True)
    parentLastDocumentLoan = LoanSerializer(read_only=True)
    parentLastDocumentCreditLine = CreditLineSerializer(read_only=True)
    # steps = StepSerializer(many=True,read_only=True)
    positions = PositionSerializer(many=True,required=False)
    relatedProcesses = RelatedProcessSerializer(many=True,read_only=True)
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


 
class ProcessRequirementAttachmentSerializer(ModelSerializer):
    def create(self, validated_data):
        processRequirementAttachment = ProcessRequirementAttachment.objects.create(**validated_data) 
        
        return processRequirementAttachment

    def update(self, instance, validated_data):
        instance.save()

        return instance
    
    class Meta:
        model = ProcessRequirementAttachment          
        fields = '__all__'   
        
class ProcessRequirementSerializer(ModelSerializer):
    isRequiredText = serializers.CharField(read_only=True)
    processRequirementAttachments =ProcessRequirementAttachmentSerializer(many=True,required=False)
    def create(self, validated_data):
        processRequirement = ProcessRequirement.objects.create(**validated_data) 

        return processRequirement

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = ProcessRequirement          
        fields = '__all__'   

        


class StatusSerializer(ModelSerializer):
     
    def create(self, validated_data):
        status = Statuses.objects.create(**validated_data) 

        return status

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Statuses          
        fields = '__all__'   


# class CanCreateFileSerializer(ModelSerializer):
#     can_add_new = serializers.CharField(read_only=True)
#     stepStatus = serializers.CharField(read_only=True)

#     class Meta:
#         model = Statuses          
#         fields = '__all__'  