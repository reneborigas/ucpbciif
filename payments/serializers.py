from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from loans.models import AmortizationStatus,Amortization,AmortizationItem,Status
from users.models import CustomUser
 
# from borrowers.serializers import BorrowerSerializer

from loans import PMT




def generateAmortizationSchedule(loan,lastPayment,currentAmortization):
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

    currentAmortization.amortizationItems.all()

    # for i in range(int(noOfPaymentSchedules)):
    i = 1
    loanAmount = lastPayment.outStandingBalance
           
    for amortizationItem in currentAmortization.amortizationItems.order_by('id').all():
        print(currentAmortization.amortizationItems.all().count())
        print("count")
        print(amortizationItem.total)
        
        print(paidItems)
        print(i)
        print("heres")
        if (i  <= (paidItems) ):
           
            print(loanAmount)
            print("pasok")
            amortizationItem.amortization = amortization
            amortizationItem.pk =None
            if (i  == (paidItems) ):
                amortizationItem.principalBalance = loanAmount
                amortizationItem.total =  lastPayment.total
                  
            amortizationItem.save()

        else:
            if (loanAmount>0):
                pmt = pmt.getPayment(loanAmount,loan.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - (i-1))

                
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
                
                 
            else:
                amortizationItem = AmortizationItem(
                schedule = schedule,
                amortization = amortization,
                days= loan.term.paymentPeriod.paymentCycle,
                principal = 0,
                interest = 0,
                vat = 0,
                total = 0,
                principalBalance = 0,
                amortizationStatus = AmortizationStatus.objects.get(pk=1), 
                )
                
            
                loanAmount = pmt.nextStartingValue

            amortizationItem.save()
        schedule = schedule + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)
        i = i+1

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
    paymentType_name = serializers.ReadOnlyField(source='paymentType.name')
     
    
    amortizationItem_schedule  = serializers.ReadOnlyField(source='amortizationItem.schedule')
    amortizationItem_principal  = serializers.ReadOnlyField(source='amortizationItem.principal')
    amortizationItem_interest = serializers.ReadOnlyField(source='amortizationItem.interest')
    amortizationItem_total  = serializers.ReadOnlyField(source='amortizationItem.total')
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data) 

        payment.amortization.amortizationStatus = AmortizationStatus.objects.get(pk=2)
        payment.amortization.save()
        # payment.loan.getCurrentAmortizationItem.amortizationStatus  = AmortizationStatus.objects.get(pk=2)
        # payment.loan.getCurrentAmortizationItem.save()

        generateAmortizationSchedule(payment.loan,payment,payment.amortization)

        return payment

    def update(self, instance, validated_data):
         

        return instance
    
    class Meta:
        model = Payment        
        fields = '__all__'
