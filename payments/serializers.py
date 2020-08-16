from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import *
from loans.models import AmortizationStatus,Amortization,AmortizationItem,Status
from users.models import CustomUser
from django.db.models import  Q
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
            dateReleased = loan.dateReleased  + timezone.timedelta(days=1),
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
                amortizationItem.total =  lastPayment.total - ( lastPayment.additionalInterest + lastPayment.penalty )
                # amortizationItem.days =  lastPayment.days
                amortizationItem.days =  loan.term.paymentPeriod.paymentCycle

                amortizationItem.schedule = schedule
                amortizationItem.principal = lastPayment.principal
                amortizationItem.interest = lastPayment.interest
                amortizationItem.daysExceed = lastPayment.daysExceed
                amortizationItem.daysAdvanced = lastPayment.daysAdvanced
                amortizationItem.additionalInterest =  lastPayment.additionalInterest
                amortizationItem.penalty =  lastPayment.penalty
                # print("balance")
                # print(lastPayment.balance)
                # if lastPayment.balance > 0:
                #     print(lastPayment.balance)
                #     print("balance2")
                #     amortizationItem.amortizationStatus = AmortizationStatus.objects.get(pk=3) #partial
                #     amortizationItem.principal = lastPayment.balance
                #     amortizationItem.interest = principalBalance * (loan.interestRate.interestRate/100) * loan.term.paymentPeriod.paymentCycle/360
            amortizationItem.save()
            # schedule = lastPayment.datePayment
        else:
            if (loanAmount>0):
                pmt = pmt.getPayment(loanAmount,loan.interestRate.interestRate,loan.term.days,noOfPaymentSchedules,noOfPaymentSchedules - (i-1))

                
                amortizationItem = AmortizationItem(
                schedule = schedule,
                amortization = amortization,
                days= loan.term.paymentPeriod.paymentCycle,
                principal = pmt.principal,
                interest = pmt.interest,
                additionalInterest = 0,
                penalty = 0,
                vat = 0,
                total = pmt.payment,
                principalBalance = pmt.nextStartingValue,
                amortizationStatus = AmortizationStatus.objects.get(pk=1), 
                )
                amortizationItem.save()
                loanAmount = pmt.nextStartingValue
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
                
            
            

                amortizationItem.save()
        schedule = schedule + timezone.timedelta(days=loan.term.paymentPeriod.paymentCycle)
        i = i+1

class PaymentStatusSerializer(ModelSerializer):
     
    def create(self, validated_data):
        paymentStatus = PaymentStatus.objects.create(**validated_data) 

        return paymentStatus

    def update(self, instance, validated_data):
         
        return instance
    
    class Meta:
        model = PaymentStatus        
        fields = '__all__'

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
    paymentStatus_name = serializers.ReadOnlyField(source='paymentStatus.name')
    amortizationItem_schedule  = serializers.ReadOnlyField(source='amortizationItem.schedule')
    amortizationItem_principal  = serializers.ReadOnlyField(source='amortizationItem.principal')
    amortizationItem_interest = serializers.ReadOnlyField(source='amortizationItem.interest')

    # amortizationItem_additional_interest = serializers.ReadOnlyField(source='amortizationItem.additionalInterest')
    # amortizationItem_penalty = serializers.ReadOnlyField(source='amortizationItem.penalty')
    # amortizationItem_total_with_penalty = serializers.ReadOnlyField(source='amortizationItem.totalToPayWithPenalty')
    

    amortizationItem_total  = serializers.ReadOnlyField(source='amortizationItem.totalToPay')
    borrower_name  = serializers.ReadOnlyField(source='loan.borrower.cooperative.name')
    borrower_id  = serializers.ReadOnlyField(source='loan.borrower.borrowerId')
    # loan_no  = serializers.ReadOnlyField(source='amortizationItem.total')

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data) 
        if payment.balance <= 0:
           
            payment.amortization.amortizationStatus = AmortizationStatus.objects.get(pk=2) #paid
       
       
        payment.amortization.save()

       
        # payment.loan.getCurrentAmortizationItem.amortizationStatus  = AmortizationStatus.objects.get(pk=2)
        # payment.loan.getCurrentAmortizationItem.save()
        
        
        # payment.amortization.amortizationItems.update(amortizationStatus=AmortizationStatus.objects.get(pk=2))
        if payment.balance >= 1:
            amortizationItem = payment.loan.getCurrentAmortizationItem()
            amortizationItem.amortizationStatus  = AmortizationStatus.objects.get(pk=3)
            amortizationItem.principal = payment.balance
            amortizationItem.interest =  payment.interestPayment - payment.interestPayment 
            amortizationItem.total = amortizationItem.interest + amortizationItem.principal
            amortizationItem.save()
        else:
            payment.amortization.amortizationItems.update(amortizationStatus=AmortizationStatus.objects.get(pk=2))
        
            generateAmortizationSchedule(payment.loan,payment,payment.amortization)
        # else: 
        #    
        return payment

    def update(self, instance, validated_data):
         
        return instance
    
    class Meta:
        model = Payment        
        fields = '__all__'
