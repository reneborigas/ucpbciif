from django.db import models
from django.utils import timezone
from borrowers.models import Borrower
from django.core.validators import MaxValueValidator, MinValueValidator 

class Status(models.Model):  
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
        related_name="loanStatusesCreatedBy",
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

class PaymentPeriod(models.Model):
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )    

    paymentCycle = models.PositiveIntegerField(default=720,validators=[MinValueValidator(1), MaxValueValidator(720)]) 
    


    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="paymentPeriodCreatedBy",
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

class Term(models.Model):

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )    

    days = models.PositiveIntegerField(default=720,validators=[MinValueValidator(1), MaxValueValidator(720)]) 
    
    paymentPeriod = models.OneToOneField(
        PaymentPeriod,
        on_delete=models.SET_NULL,
        related_name="terms",
        null = True,
    )

    remarks = models.TextField(
        blank = True,
        null = True,
    )

    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="termCreatedBy",
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




class Loan(models.Model):

    borrower =  models.ForeignKey(
        'borrowers.Borrower',
        on_delete=models.CASCADE,
        related_name="loans",
    )
  
    amount = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False) 

    term =  models.ForeignKey(
       Term,
        on_delete=models.SET_NULL,
        related_name="loans",
          null = True,
    )

    purpose = models.TextField(
        blank = True,
        null = True,
    )

    security = models.TextField(
        blank = True,
        null = True,
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="loanStatuses",
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
        related_name="loanCreatedBy",
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
        return "%s %s" % (self.borrower,self.amount)