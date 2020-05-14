from django.db import models

class GenderType(models.Model):
    name = models.CharField(
        max_length=255,
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
        related_name="genderTypeCreatedBy",
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

    class Meta:
        verbose_name = "Gender Type (System Essential)"
        verbose_name_plural = "Gender Types (System Essential)"

class CooperativeType(models.Model):    
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
        related_name="cooperativeTypeCreatedBy",
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

    class Meta:
        verbose_name = "Cooperative Type (System Essential)"
        verbose_name_plural = "Cooperative Types (System Essential)"