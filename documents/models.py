from django.db import models
from django.utils import timezone
  


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
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    ) 
    documentType = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    borrower = models.ForeignKey(
        'borrowers.Borrower',
        on_delete=models.CASCADE,
        related_name="borrowers",
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
 


class DocumentMovement(models.Model):     
     
    Document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="documentMovements",
    )

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
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
        return "%s" % (self.name)





