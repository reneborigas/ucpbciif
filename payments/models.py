from django.db import models
from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum

class PaymentStatus(models.Model):  
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    ) 
    isDefault = models.BooleanField(
        default=False
    )    
    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="paymentStatusCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    isFinalStatus = models.BooleanField(
        default=False,
    )

    isNegativeResult = models.BooleanField(
        default=False,
    )
    
    def __str__(self):
        return "%s" % (self.name  )
  




class PaymentType(models.Model):

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )    
      
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="paymentTypeCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)

      

class Payment(models.Model):

    loan =  models.ForeignKey(
        'loans.Loan',
        on_delete=models.CASCADE,
        related_name="payments",
    ) 
    amortization =  models.ForeignKey(
        'loans.Amortization',
        on_delete=models.CASCADE,
        related_name="payments",
    ) 
      
    cash = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    check = models.DecimalField( max_digits=12, decimal_places=2,blank=False)
    checkNo = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )    
    bankAccount = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )    
    total = models.DecimalField( max_digits=24, decimal_places=2,blank=False)
 
    paymentType =  models.ForeignKey(
       PaymentType,
        on_delete=models.SET_NULL,
        related_name="loans",
          null = True,
    )
    

    balance = models.DecimalField( max_digits=24, decimal_places=2,blank=False)

    outStandingBalance = models.DecimalField( max_digits=24, decimal_places=2,blank=False)

    overPayment = models.DecimalField( max_digits=24, decimal_places=2,blank=False)

     

    paymentStatus = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="paymentStatuses",
    )

    description = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="paymentCreatedBy",
        null = True,
    )
    
    dateTendered = models.DateTimeField(
        auto_now_add=True,
       
    )
    datePayment = models.DateTimeField(
        blank=True,
        null=True
       
    )

    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
     

    def __str__(self):
        return "%s %s" % (self.loan,self.total)

    # def getLatestAmortization(self):
      
    #     return  self.amortizations.order_by('-id').first()

    # def getTotalAmortizationInterest(self):
         
    #     latestAmortization = self.amortizations.order_by('-id').first()
      
    #     if latestAmortization: 
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']  
    #     return 0

    # def getTotalAmortizationPayment(self):
    #     latestAmortization = self.amortizations.order_by('-id').first()
      
    #     if latestAmortization: 
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']   
    #     return 0
              
       
 