from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from payments.serializers import PaymentSerializer

# from borrowers.serializers import BorrowerSerializer




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




class InterestRateSerializer(ModelSerializer):
   
    def create(self, validated_data):
        interestRate = InterestRate.objects.create(**validated_data) 
        return interestRate

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = InterestRate        
        fields = '__all__'

class AmortizationItemSerializer(ModelSerializer):
    # termName = serializers.CharField(read_only=True) 

    # isItemPaid = serializers.CharField(read_only=True)
    amortizationStatus_name = serializers.ReadOnlyField(source='amortizationStatus.name')
    def create(self, validated_data):
        amortizationitem = AmortizationItem.objects.create(**validated_data) 
        return amortizationitem

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = AmortizationItem        
        fields = '__all__'

class AmortizationSerializer(ModelSerializer):
    # termName = serializers.CharField(read_only=True) 
    amortizationItems = AmortizationItemSerializer(many=True,read_only=True)
    totalAmortizationInterest = serializers.CharField(read_only=True)
    totalObligations = serializers.CharField(read_only=True)
    def create(self, validated_data):
        amortization = Amortization.objects.create(**validated_data) 
        return amortization

    def update(self, instance, validated_data):
        # instance.loanAmount = validated_data.get("loanAmount", instance.loanAmount)
        # instance.loanName = validated_data.get("loanName", instance.loanName)
        # instance.borrower =  validated_data.get("borrower", instance.borrower)
        instance.save()

        return instance
    
    class Meta:
        model = Amortization        
        fields = '__all__'

class StatusSerializer(ModelSerializer): 
 

    def create(self, validated_data):
        status = Status.objects.create(**validated_data) 
        return status

    def update(self, instance, validated_data): 
        instance.save()

        return instance
    
    class Meta:
        model = Status        
        fields = '__all__'


class CreditLineSerializer(ModelSerializer): 

    term_name = serializers.ReadOnlyField(source='term.name')
    interestRate_amount = serializers.ReadOnlyField(source='interestRate.interestRate')
    status_name = serializers.ReadOnlyField(source='status.name')
    loanProgram_name = serializers.ReadOnlyField(source='loanProgram.name')
    borrower_name = serializers.ReadOnlyField(source='borrower.cooperative.name')
    remainingCreditLine = serializers.CharField(read_only=True)
    totalAvailment = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        creditLine = CreditLine.objects.create(**validated_data) 
        return creditLine

    def update(self, instance, validated_data): 
        instance.save()

        return instance
    
    class Meta:
        model = CreditLine        
        fields = '__all__'
 

class LoanSerializer(ModelSerializer):
    # termName = serializers.CharField(read_only=True) 
    loanStatus_name = serializers.ReadOnlyField(source='loanStatus.name')
    payments = PaymentSerializer(many=True,read_only=True)
    creditLine_amount= serializers.ReadOnlyField(source='creditLine.amount')
    creditLine_dateApproved = serializers.ReadOnlyField(source='creditLine.dateApproved')
    creditLine_dateExpired = serializers.ReadOnlyField(source='creditLine.dateExpired')
    borrower_name = serializers.ReadOnlyField(source='borrower.cooperative.name')
    borrower_id = serializers.ReadOnlyField(source='borrower.borrowerId')
    amortizations     =  AmortizationSerializer(many=True,read_only=True)
    term_name = serializers.ReadOnlyField(source='term.name')
    interestRate_amount = serializers.ReadOnlyField(source='interestRate.interestRate')
    loanProgram_name = serializers.ReadOnlyField(source='loanProgram.name')
    totalAmortizationInterest = serializers.CharField(read_only=True)
    totalObligations = serializers.CharField(read_only=True)
    latestAmortization =  AmortizationSerializer(read_only=True)

    latestPayment =  PaymentSerializer(read_only=True)

    outStandingBalance = serializers.CharField(read_only=True)
    interestBalance= serializers.CharField(read_only=True)

    totalPayment = serializers.CharField(read_only=True)
    currentAmortizationItem =   AmortizationItemSerializer(read_only=True)

    
    # status=StatusSerializer(read_only=True)
    term = TermSerializer(read_only=True)
    parentLastDocumentCreditLine = CreditLineSerializer(read_only=True)
    # borrower = BorrowerSerializer(read_only=True)
    def create(self, validated_data):

        loan = Loan.objects.create(**validated_data) 
        loan.term = loan.creditLine.term
        loan.save()
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
    activeCreditLine = CreditLineSerializer(read_only=True)
    totalAvailments = serializers.CharField(read_only=True)
    def create(self, validated_data):
        loanProgram = LoanProgram.objects.create(**validated_data) 
        return loanProgram

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = LoanProgram        
        fields = '__all__'


