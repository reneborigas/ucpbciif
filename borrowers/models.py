from django.db import models
from django.utils import timezone
from datetime import date


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
