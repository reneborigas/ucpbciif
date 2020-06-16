from django.db import models
from django.utils import timezone
 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
class Office(models.Model):     
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
        related_name="officeCreatedBy",
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




class Position(models.Model):     

    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name="positions",
   
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
        related_name="positionCreatedBy",
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



class Committee(models.Model):     

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE, 
        related_name="committees",
    )

    
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
        related_name="committeeCreatedBY",
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

  


class Note(models.Model):
    action_time = models.DateTimeField(
        auto_now_add=True,
    )
    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="committeeNotes"
    )
    action_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    note = models.CharField(
        max_length=255, 
        blank=False
    )
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name="note_content_type",
        blank=True,
        null = True,
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null = True,
    )
    content_object = GenericForeignKey(
        'content_type', 
        'object_id',
    )
    object_type = models.CharField(
        max_length=255,
        blank=True,
        null = True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    # apiLink = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null = True,
    # )
    # valueToDisplay = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null = True,
    # )

    def __str__(self):
        return "%s - %s %s %s" % (self.committee,self.action_type, self.content_type, self.object_id)

