from django.db import models
from django.utils import timezone
from borrowers.models import Borrower
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum

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




class LoanProgram(models.Model):

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )    
    creditLineAmount = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    remarks = models.TextField(
        blank = True,
        null = True,
    )

    description = models.TextField(
        blank = True,
        null = True,
    )


    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="loanProgramCreatedBy",
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

    def getActiveCreditline(self,borrower):
       
        if self.programLoans.all().last():
            return self.programCreditLines.filter(status__name='APPROVED',borrower=borrower).last()

        return None

    def getActiveLoan(self,borrower):
       
        if self.programLoans.all().last():
            return self.programLoans.filter(status__name='RELEASED',borrower=borrower).last()

        return None

    def getTotalAvailments(self,borrower):
         
        if(not self.programLoans.filter(status__name='RELEASED',borrower=borrower)):
            return 0
        return self.programLoans.filter(status__name='RELEASED',borrower=borrower).aggregate(totalAvailments=Sum(F('amount') ))['totalAvailments'] 

   

class CreditLine(models.Model):

    borrower =  models.ForeignKey(
        'borrowers.Borrower',
        on_delete=models.CASCADE,
        related_name="creditLines",
    )
    

    loanProgram =  models.ForeignKey(
       LoanProgram,
        on_delete=models.CASCADE,
        related_name="programCreditLines", 
    )

    amount = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False) 

    term =  models.ForeignKey(
       Term,
        on_delete=models.SET_NULL,
        related_name="creditLines",
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
        related_name="creditLineStatuses",
    )
 
     
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="loanCreatedBy",
        null = True,
    )

    dateApproved = models.DateTimeField(
        blank=True,
        null=True
    )

    dateExpired = models.DateTimeField(
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
        return "%s %s" % (self.borrower,self.amount)
 
    def getRemainingCreditLine(self):
        totalLoanAvailments=  self.loans.filter(status__name='RELEASED').aggregate(totalLoanAvailments=Sum(F('amount') ))['totalLoanAvailments'] 
        if totalLoanAvailments:
            return self.amount - int(totalLoanAvailments)
        return self.amount

class Loan(models.Model):

    borrower =  models.ForeignKey(
        'borrowers.Borrower',
        on_delete=models.CASCADE,
        related_name="loans",
    )
    
    

    creditLine =  models.ForeignKey(
       CreditLine,
        on_delete=models.CASCADE,
        related_name="loans", 
    )

    loanProgram =  models.ForeignKey(
       LoanProgram,
        on_delete=models.CASCADE,
        related_name="programLoans", 
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
        related_name="creditLineCreatedBy",
        null = True,
    )
    dateApproved = models.DateTimeField(
        blank=True,
        null=True
    )
    dateReleased = models.DateTimeField(
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
        return "%s %s" % (self.borrower,self.amount)

    def getTotalAmortizationInterest(self):
        return self.amortizations.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest'] 

    def getTotalAmortizationPayment(self):
         return self.amortizations.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment'] 

class Amortization(models.Model):


    
    
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="amortizations",
        blank=True,
        null=True
    )

    days = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=0
    )


    schedule = models.DateTimeField(
        blank=True,
        null=True
    )
    
    principal = models.DecimalField( max_digits=12, decimal_places=2,blank=False)
    
    interest = models.DecimalField( max_digits=12, decimal_places=2,blank=False)
    
    vat = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    total = models.DecimalField( max_digits=12, decimal_places=2,blank=False)
    
    principalBalance = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="amortizationStatuses",
    )
 
     
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="amortizationCreatedBy",
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
        return "%s %s" % (self.loan,self.schedule)


 