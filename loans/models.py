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
        related_name="statusCreatedBy",
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


class AmortizationStatus(models.Model):  
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
        related_name="amortizationStatusesCreatedBy",
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
        return "%s" % (self.name  )

class LoanStatus(models.Model):  
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
    code = models.CharField(
        max_length=25,
        blank = False,
        null = False, 
    )    
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
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
            return self.programLoans.filter(loanStatus__name='CURRENT',borrower=borrower).last()

        return None

    def getTotalAvailments(self,borrower):
         
        if(not self.programLoans.filter(loanStatus__name='CURRENT',borrower=borrower)):
            return 0
        return self.programLoans.filter(loanStatus__name='CURRENT',borrower=borrower).aggregate(totalAvailments=Sum(F('amount') ))['totalAvailments'] 

   


class InterestRate(models.Model):

    interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False) 
     
    remarks = models.TextField(
        blank = True,
        null = True,
    )

    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="interestRateCreatedBy",
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
        return "%s" % (self.interestRate)


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

    # interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False) 
    interestRate =  models.ForeignKey(
       InterestRate,
        on_delete=models.CASCADE,
        related_name="creditLines", 
    )
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
    totalAvailment = 0

    def __str__(self):
        return "%s %s" % (self.borrower,self.amount)
 
    def getRemainingCreditLine(self):
        totalLoanAvailments=  self.loans.filter(loanStatus__name='CURRENT').aggregate(totalLoanAvailments=Sum(F('amount') ))['totalLoanAvailments'] 
        if totalLoanAvailments:
            return self.amount - int(totalLoanAvailments)
        return self.amount
    def getTotalAvailment(self):
        totalLoanAvailments=  self.loans.filter(loanStatus__name='CURRENT').aggregate(totalLoanAvailments=Sum(F('amount') ))['totalLoanAvailments'] 
        if totalLoanAvailments:
            return   int(totalLoanAvailments)
        return 0


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

    interestRate =  models.ForeignKey(
       InterestRate,
        on_delete=models.CASCADE,
        related_name="loans", 
    )
    amount = models.DecimalField( max_digits=12, decimal_places=2,blank=False)

    # interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False) 

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

    loanStatus = models.ForeignKey(
        LoanStatus,
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

    def getLatestAmortization(self):
      
        return  self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()

    def getLatestPayment(self):
      
        return  self.payments.filter(paymentStatus__name='TENDERED').order_by('-id').first()

    def getTotalAmortizationInterest(self):
         
        latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()
      
        if latestAmortization: 
            return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']  
        return 0


    # def getTotalAmortizationInterestByAmortization(self,amortizationId):
         
    #     latestAmortization = self.amortizations.filter(amortization__id=amortizationId,amortizationStatus__name='UNPAID').order_by('-id').first()
      
    #     if latestAmortization: 
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']  
    #     return 0

    def getTotalObligations(self):
         
        latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()
      
        if latestAmortization: 
            return latestAmortization.amortizationItems.aggregate(totalObligations=Sum(F('total') ))['totalObligations']  
        return 0

    def getTotalAmortizationPayment(self):
        latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()
      
        if latestAmortization: 
            return latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']   
        return 0

    def getOutstandingBalance(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']:
            totalPayments =  self.payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']
        latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()
        print(totalPayments)
        if latestAmortization: 
            
            return latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']  -  totalPayments
 
        return   0  
        
    def getInterestBalance(self):
  
         
        latestPayment =self.payments.filter(paymentStatus__name='TENDERED').order_by('-id').first()
         
        if latestPayment: 
           
            # return self.getTotalAmortizationInterest() -  latestPayment.amortizationItem.interest
            return self.getTotalAmortizationInterest() - self.payments.filter(paymentStatus__name='TENDERED').aggregate(totalPaidInterest=Sum(F('interest') ))['totalPaidInterest']
        return   0  

    def getTotalPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']:
            totalPayments =  self.payments.aggregate(totalPayments=Sum(F('total') ))['totalPayments']
            return  totalPayments
 
        return   0  

    def getCurrentAmortizationItem(self):
        
        latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()
        amortizations = self.amortizations.filter(amortizationStatus__name='PAID')


        if latestAmortization: 
            i = 0
            for item in latestAmortization.amortizationItems.order_by('id').all():
                if (i==amortizations.count()): 
                    return item
                i = i + 1 
  

class Amortization(models.Model): 
    
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="amortizations",
        blank=True,
        null=True
    )
     
    amortizationStatus = models.ForeignKey(
        AmortizationStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="amortizationStatusesAmortizations",
    )
    dateReleased = models.DateTimeField(
        blank=True,
        null=True
       
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
        return "%s %s" % (self.loan,self.amortizationStatus.name)

    def getTotalAmortizationInterest(self):
        return self.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']  
    
    def getTotalObligations(self):
        return self.amortizationItems.aggregate(totalObligations=Sum(F('total') ))['totalObligations'] 

class AmortizationItem(models.Model): 
    
    
    amortization = models.ForeignKey(
        Amortization,
        on_delete=models.CASCADE,
        related_name="amortizationItems",
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

    amortizationStatus = models.ForeignKey(
        AmortizationStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="amortizationItemStatuses",
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
        return "%s %s" % (self.amortization.loan,self.schedule) 

    # def isPaid(self):
    #     if  (self.payments.filter(isDeleted=False).count() > 0):
    #         return 'PAID'
    #     return 'UNPAID'