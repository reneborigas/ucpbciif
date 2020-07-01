from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *





class PaymentPeriodSerializer(ModelSerializer):
     
    def create(self, validated_data):
        paymentPeriod = PaymentPeriod.objects.create(**validated_data) 
        return paymentPeriod

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = PaymentPeriod        
        fields = '__all__'

        

class TermSerializer(ModelSerializer):
    paymentPeriod = PaymentPeriodSerializer(read_only=True)
    termName = serializers.CharField(read_only=True)

    def create(self, validated_data):
        term = Term.objects.create(**validated_data) 
        return term

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = Term        
        fields = '__all__'





class LoanSerializer(ModelSerializer):
    # termName = serializers.CharField(read_only=True) 

    term_name = serializers.ReadOnlyField(source='term.name')
    loanProgram_name = serializers.ReadOnlyField(source='loanProgram.name')

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data) 
        return loan

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Loan        
        fields = '__all__'


        
class LoanProgramSerializer(ModelSerializer): 
    activeLoan = LoanSerializer(read_only=True)
    totalAvailments = serializers.CharField(read_only=True)
    def create(self, validated_data):
        loanProgram = LoanProgram.objects.create(**validated_data) 
        return loanProgram

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = LoanProgram        
        fields = '__all__'
