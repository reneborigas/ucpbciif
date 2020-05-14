from django.db import models

class GenderType(models.Model):
    title = models.CharField(
        max_length=255,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="genderTypeCreatedBy",
        null = True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Gender Type (System Essential)"
        verbose_name_plural = "Gender Types (System Essential)"
