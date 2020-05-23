from django.db import models
from django.utils import timezone
 
    
class Process(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    code = models.CharField(
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
        related_name="processCreatedBy",
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




class SubProcess(models.Model):     
    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    code = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )

    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name="subProcesses",
   
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
        related_name="subProcessCreatedBy",
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


class Statuses(models.Model):  

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )

    code = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
 
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="statuses",
   
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
        related_name="statusesCreatedBy",
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
class Requirements(models.Model):  

    name = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
    code = models.CharField(
        max_length=255,
        blank = False,
        null = False, 
    )
 
    subProcess = models.ForeignKey(
        SubProcess,
        on_delete=models.CASCADE,
        related_name="requirements",
   
    )

    optional = models.BooleanField(
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
        related_name="requirementsCreatedBy",
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
