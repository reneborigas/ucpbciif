from django.db import models
from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Prefetch, F, Case, When, Value as V, Count, Sum


class PaymentStatus(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    isDefault = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="paymentStatusCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
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
        return "%s" % (self.name)


class PaymentType(models.Model):
    code = models.CharField(
        max_length=255,
        blank=True,
        null=False,
    )
    transactionType = models.CharField(
        max_length=255,
        blank=True,
        null=False,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    transactionDescription = models.CharField(
        max_length=255,
        blank=True,
        null=False,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="paymentTypeCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)


class CheckStatus(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    isDefault = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="checkStatusesCreatedBy",
        null=True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.name)


class Check(models.Model):
    loan = models.ForeignKey(
        "loans.Loan",
        on_delete=models.CASCADE,
        related_name="checks",
    )
    amortizationItem = models.ForeignKey(
        "loans.AmortizationItem",
        on_delete=models.CASCADE,
        related_name="checks",
    )
    dateReceived = models.DateTimeField(blank=True, null=True)
    bankBranch = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    checkNo = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    pnNo = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    area = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    dateWarehoused = models.DateTimeField(blank=True, null=True)
    warehousingBatchNo = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    checkStatus = models.ForeignKey(
        CheckStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="checkStatuses",
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%s - %s %s" % (self.checkNo, self.bankBranch, self.checkStatus)


class Payment(models.Model):
    loan = models.ForeignKey(
        "loans.Loan",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    pdc = models.ForeignKey(Check, on_delete=models.SET_NULL, related_name="payments", blank=True, null=True)
    amortization = models.ForeignKey(
        "loans.Amortization",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amortizationItem = models.ForeignKey(
        "loans.AmortizationItem",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    days = models.PositiveIntegerField(blank=False, null=False, default=0)
    daysExceed = models.PositiveIntegerField(blank=False, null=False, default=0)
    daysAdvanced = models.PositiveIntegerField(blank=False, null=False, default=0)
    principal = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    accruedInterest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    interest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    totalToPay = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

    additionalInterest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

    penalty = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    totalToPayWithPenalty = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

    principalBalance = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    cash = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    check = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    interestPayment = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    accruedInterestPayment = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    penaltyPayment = models.DecimalField(max_digits=12, decimal_places=2, blank=False)

    exemptAdditionalInterest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    exemptPenalty = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    checkNo = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    bankAccount = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    total = models.DecimalField(max_digits=24, decimal_places=2, blank=False)
    paymentType = models.ForeignKey(
        PaymentType,
        on_delete=models.SET_NULL,
        related_name="loans",
        null=True,
    )
    balance = models.DecimalField(max_digits=24, decimal_places=2, blank=False)
    outStandingBalance = models.DecimalField(max_digits=24, decimal_places=2, blank=False)
    overPayment = models.DecimalField(max_digits=24, decimal_places=2, blank=False)
    paymentFromOverPayment = models.DecimalField(max_digits=24, decimal_places=2, blank=False)
    paymentStatus = models.ForeignKey(
        PaymentStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="paymentStatuses",
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="paymentCreatedBy",
        null=True,
    )
    dateTendered = models.DateTimeField(
        auto_now_add=True,
    )
    datePayment = models.DateTimeField(blank=True, null=True)
    isPaymentExtension = models.BooleanField(
        default=False,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    
    def __str__(self):
        return "%s - %s %s" % (self.id, self.loan, self.total)

    # def getLatestAmortization(self):

    #     return  self.amortizations.order_by('-id').first()

    # def getTotalAmortizationInterest(self):

    #     latestAmortization = self.amortizations.order_by('-id').first()

    #     if latestAmortization:
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']
    #     return 0

    # def getTotalAmortizationPayment(self):
    #     latestAmortization = self.amortizations.order_by('-id').first()

    #     if latestAmortization:
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F('total') ))['totalAmortizationPayment']
    #     return 0
