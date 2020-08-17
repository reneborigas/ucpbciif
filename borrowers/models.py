from django.db import models
from django.utils import timezone
from datetime import date
from django.db.models import Prefetch,F,Case,When,Value as V, Count, Sum,Q
from django.db.models.functions import Coalesce
from payments.models import Payment

class ContactPerson(models.Model):
    firstname = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    middlename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    lastname = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    address = models.TextField(
        blank = True,
        null = True,
    )
    telNo = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    emailAddress = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    phoneNo = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="contactPersonCreatedBy",
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
        return "%s %s %s" % (self.firstname,self.middlename,self.lastname)
    
class Cooperative(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    icRiskRating = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    tin = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    #ncorporations  
    cdaRegistrationDate  = models.DateField(
        default=date.today
    )
    initialMembershipSize = models.IntegerField(
        blank = False
    )
    membershipSize = models.IntegerField(
        blank = False
    )
    paidUpCapitalInitial = models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )
    noOfCooperators = models.IntegerField(
        blank = False
    )
    coconutFarmers = models.IntegerField(
        blank = False
    )
    #capital structure
    authorized =  models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )
    fullyPaidSharesNo = models.IntegerField(
        blank = False
    )    
    bookValue = models.IntegerField(
        blank = False
    )
    parValue =  models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )
    paidUp =  models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )
    fullyPaidPercent  = models.IntegerField(
        blank = False
    )    
    initialPaidUpShare = models.IntegerField(
        blank = False
    )    
    #financials, financial statemnts - will be a file attachment
    address = models.TextField(
        blank = True,
        null = True,
    )
    telNo = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    emailAddress = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    phoneNo = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )
    
    fax = models.CharField(
        max_length=255,
        null=True,
        blank=True 
    )    
    cooperativeType = models.ForeignKey(
        'settings.CooperativeType',
        on_delete=models.SET_NULL,
        related_name="cooperativeCooperativeType",
        null = True,
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
        related_name="cooperativeCreatedBy",
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

class Director(models.Model):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        related_name="directors",
        null = True,
    )
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    position = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    educationalAttainment = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    age = models.IntegerField(
        blank = False
    )
    yearsInCoop = models.IntegerField(
        blank = False
    )
    oSLoanWithCoop = models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )     
    status = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="directorCreatedBy",
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

class StandingCommittee(models.Model):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        related_name="standingCommittees",
        null = True,
    )
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    #Audit and Inventory or Credit Committee
    department = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    position = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    educationalAttainment = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    age = models.IntegerField(
        blank = False
    )
    yearsInCoop = models.IntegerField(
        blank = False
    )
    oSLoanWithCoop = models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )     
    status = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="standingCommitteeCreatedBy",
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

class Grant(models.Model):
    cooperative = models.ForeignKey(
        Cooperative,
        on_delete=models.CASCADE,
        related_name="grants",
        null = True,
    )
    donor = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    projectType = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    amount = models.DecimalField(
        default = 0,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )
    projectStatus = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="grantCreatedBy",
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

class Borrower(models.Model):
    borrowerId = models.AutoField(primary_key=True)
    cooperative = models.OneToOneField(
        Cooperative,
        on_delete=models.SET_NULL,
        related_name="borrowerCooperative",
        null = True,
    )
    contactPerson = models.OneToOneField(
        ContactPerson,
        on_delete=models.SET_NULL,
        related_name="borrowerContactPerson",
        null = True,
    ) 
    status = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    clientSince = models.DateField(
        null=True
    ) 
    remarks = models.TextField(
        blank = True,
        null = True,
    )    
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="borrowerCreatedBy",
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
        return "%s" % (self.cooperative)
    
    def getTotalAvailments(self):

        
         
        if(not self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'))):
            return 0
        
        
        loans = self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED')) 
        totalAvailments = 0
        for loan in loans:
            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal() 
            totalAvailments = totalAvailments + loan.totalAmortizationPrincipal

        return totalAvailments
        
    def getTotalOutstandingBalance(self):
         
        if(not self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'))):
            return 0
        totalBalance = 0 
        for loan in self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED')):

            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal() 

            balance = loan.totalAmortizationPrincipal - loan.getTotalPrincipalPayment()
            totalBalance = totalBalance + balance
            print(totalBalance)

        
        return totalBalance

    def getTotalAvailmentsPerProgram(self,loanProgramId):
         
        if(not self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),loanProgram_id=loanProgramId)):
            return 0
        return self.loans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),loanProgram_id=loanProgramId).aggregate(totalAvailments=Sum(F('amount') ))['totalAvailments'] 


    def getPayments(self):
        return Payment.objects.filter(loan__borrower=self).exclude(isDeleted=True).order_by('-id')

    
    def getTotalPayments(self): 
        return Payment.objects.filter(loan__borrower=self,paymentStatus__name='TENDERED').exclude(isDeleted=True).aggregate(totalPayments=Coalesce(Sum(F('total')),0))['totalPayments']

def attachment_directory_path(instance, filename):
    # ext = filename.split('.')[-1]
    # filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return 'attachments/borrowers/{0}/{1}'.format(instance.borrower.borrowerId, filename)

class BorrowerAttachment(models.Model):  
    fileName = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )

    fileAttachment = models.FileField(
        null = True,
        blank=True,
        upload_to=attachment_directory_path
    )

    borrower = models.ForeignKey(
        Borrower,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="borrowerAttachments",
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
        related_name="borrowerAttachmentCreatedBy",
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
        return "%s - %s" % (self.borrower,self.fileName)