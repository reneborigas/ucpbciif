from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from committees.models import Note


class DocumentType(models.Model):     
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
        related_name="documentTypeCreatedBy",
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

class Signatory(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    documentType = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="signatories",
    )
    position = models.ForeignKey(
        'committees.Position',
        on_delete=models.CASCADE,
        related_name="signatoryPositions",
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="signatoryCreatedBy",
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
        
class Document(models.Model):     
    code = models.CharField(
        max_length=255,
        blank = True,
        null = False, 
    )
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )    
    documentType = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="documentTypeDocuments",
    )
    borrower = models.ForeignKey(
        'borrowers.Borrower',
        on_delete=models.CASCADE,
        related_name="documents",
    )  
    parentDocument = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        related_name="childDocuments",
        null=True,
        blank=True
    )
    loan = models.ForeignKey(
        'loans.Loan',
        on_delete=models.CASCADE,
        related_name="loanDocuments",
        blank=True,
        null=True
    )
    creditLine = models.ForeignKey(
        'loans.CreditLine',
        on_delete=models.CASCADE,
        related_name="creditLineDocuments",
        blank=True,
        null=True
    )
    subProcess = models.ForeignKey(
        'processes.SubProcess',
        on_delete=models.CASCADE,
        related_name="documentSubProcesses",
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
        related_name="documentCreatedBy",
        null = True,
    )

    
    dateApproved = models.DateTimeField(
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
    loanid=None
    
    notes = GenericRelation(Note)
    subProcessId = None
    committeeId = None
    def __str__(self):
        return "%s" % (self.name)


    def getCurrentStatus(self):
        return self.documentMovements.all().order_by('-id').first().status


class DocumentMovement(models.Model):     
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="documentMovements",
    )
    outputId=None
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    ) 
    step = models.ForeignKey(
        'processes.Step',
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="stepDocumentMovements",
    )
    output = models.ForeignKey(
        'processes.Output',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="outputDocumentMovements",
    )
    committee = models.ForeignKey(
        'committees.Committee',
        on_delete=models.CASCADE,
        related_name="documentMovementCommittes",
    )
    status = models.ForeignKey(
        'processes.Statuses',
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="documentMovementStatuses",
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
        related_name="documentMovementCreatedBy",
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
        return "%s - %s - %s" % (self.name,self.status,self.document)





