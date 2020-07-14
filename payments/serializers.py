from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from loans.models import AmortizationStatus,Amortization,AmortizationItem,Status
from users.models import CustomUser
# from borrowers.serializers import BorrowerSerializer

from loans import PMT




def generateAmortizationSchedule(loan,lastPayment):
    paidItems = loan.amortizations.filter(amortizationStatus__name='PAID').count()

    noOfPaymentSchedules = loan.term.days / loan.term.paymentPeriod.paymentCycle
    schedule = loan.dateReleased  + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)

    pmt = PMT()
    
    print(pmt.payment)
    print(pmt.nextStartingValue)
    print(pmt.interest)
    print(pmt.principal)

    loanAmount = loan.amount
     

    amortization = Amortization( 
            loan = loan,
             
            amortizationStatus = AmortizationStatus.objects.get(pk=1),
            createdBy = CustomUser.objects.get(pk=1)
        )
    amortization.save()

    

    for i in range(int(noOfPaymentSchedules)):

        pmt = pmt.getPayment(loanAmount,loan.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - i)

        amortizationItem = AmortizationItem(
            schedule = schedule,
            amortization = amortization,
            days= loan.term.paymentPeriod.paymentCycle,
            principal = pmt.principal,
            interest = pmt.interest,
            vat = 0,
            total = pmt.payment,
            principalBalance = pmt.nextStartingValue,
            amortizationStatus = AmortizationStatus.objects.get(pk=1), 
        )
        amortizationItem.save()

        schedule = schedule + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)
        loanAmount = pmt.nextStartingValue
        
        print(paidItems - 1)
        print(i)
        print("heres")
        if (i == (paidItems - 1) ):
            loanAmount = lastPayment.outStandingBalance
            print(loanAmount)
            print("pasok")



class PaymentTypeSerializer(ModelSerializer):
     
    def create(self, validated_data):
        paymentType = PaymentType.objects.create(**validated_data) 
        return paymentType

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = PaymentType        
        fields = '__all__'

         
class PaymentSerializer(ModelSerializer):
     
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data) 

        payment.amortization.amortizationStatus = AmortizationStatus.objects.get(pk=2)
        payment.amortization.save()
        # payment.loan.getCurrentAmortizationItem.amortizationStatus  = AmortizationStatus.objects.get(pk=2)
        # payment.loan.getCurrentAmortizationItem.save()

        generateAmortizationSchedule(payment.loan,payment)

        return payment

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = Payment        
        fields = '__all__'
