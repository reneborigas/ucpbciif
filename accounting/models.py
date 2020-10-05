from django.db import models

class ChartOfAccountType(models.Model):
    title = models.CharField(
        max_length=255,
    )
    toIncrease = models.TextField(
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )    
    isDeleted = models.BooleanField(
        default=False,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="chartOfAccountTypesCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Chart of Accounts Type (System Essential)"
        verbose_name_plural = "Chart of Accounts Types (System Essential)"

class ChartOfAccount(models.Model):
    account = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        max_length=255,
        blank = True,
        null = True,
    )
    accountType = models.ForeignKey(
        ChartOfAccountType,
        on_delete=models.CASCADE,
        related_name="chartOfAccountType"
    )
    accountCode = models.CharField(
        max_length=255,
        blank = True,
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="chartOfAccountCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return "%s  %s : %s" % (self.accountCode,self.accountType,self.account)

    class Meta:
        verbose_name = "Chart of Account (System Essential)"
        verbose_name_plural = "Chart of Accounts (System Essential)"
        ordering = ['accountCode']