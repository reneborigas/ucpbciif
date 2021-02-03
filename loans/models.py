from django.db import models
from django.utils import timezone
from borrowers.models import Borrower
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Prefetch, F, Case, When, Value as V, Count, Sum, Q, Subquery
from payments.models import Check
from datetime import date


class Status(models.Model):
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
        related_name="statusCreatedBy",
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


class AmortizationStatus(models.Model):
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
        related_name="amortizationStatusesCreatedBy",
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


class LoanStatus(models.Model):
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
        related_name="loanStatusesCreatedBy",
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


class PaymentPeriod(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    paymentCycle = models.PositiveIntegerField(default=720, validators=[MinValueValidator(1), MaxValueValidator(720)])

    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="paymentPeriodCreatedBy",
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


class Term(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    days = models.PositiveIntegerField(default=720, validators=[MinValueValidator(1), MaxValueValidator(5000)])
    principalPaymentPeriod = models.ForeignKey(
        PaymentPeriod,
        on_delete=models.SET_NULL,
        related_name="principalPaymentPeriod",
        null=True,
    )
    interestPaymentPeriod = models.ForeignKey(
        PaymentPeriod,
        on_delete=models.SET_NULL,
        related_name="interestPaymentPeriod",
        null=True,
    )
    remarks = models.TextField(
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="termCreatedBy",
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


class LoanProgram(models.Model):
    code = models.CharField(
        max_length=25,
        blank=False,
        null=False,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
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
        related_name="loanProgramCreatedBy",
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

    def getActiveCreditline(self, borrower):

        if self.programLoans.all().last():
            return self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last()

        return None

    def getActiveLoan(self, borrower):

        if self.programLoans.all().last():
            return self.programLoans.filter(
                Q(loanStatus__name="CURRENT")
                | Q(loanStatus__name="RESTRUCTURED CURRENT")
                | Q(loanStatus__name="RESTRUCTURED"),
                borrower=borrower,
            ).last()

        return None

    def getActiveCreditlineDateApproved(self, borrower):

        if self.programLoans.all().last():
            if self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last() is not None:
                return self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last().dateApproved

        return None

    def getActiveCreditlineDateExpired(self, borrower):

        if self.programLoans.all().last():
            if self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last() is not None:
                return self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last().dateExpired

        return None

    def getActiveCreditlineAmount(self, borrower):

        if self.programLoans.all().last():
            if self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last() is not None:
                return self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last().amount

        return None

    def getActiveCreditlineAvailableBalance(self, borrower):

        if not self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            borrower=borrower,
        ):
            return 0

        loans = self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            borrower=borrower,
        )
        totalAvailments = 0
        availableBalance = 0

        for loan in loans:
            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()
            totalAvailments = totalAvailments + loan.totalAmortizationPrincipal

        if self.programLoans.all().last():
            availableBalance = (
                self.programCreditLines.filter(status__name="APPROVED", borrower=borrower).last().amount
                - totalAvailments
            )

        return availableBalance

    def getOverallLoan(self):

        if not self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):
            return 0
        return self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ).aggregate(totalAvailments=Sum(F("amount")))["totalAvailments"]

    def getOverallLoanPercentage(self, totalLoans):

        from decimal import Decimal

        if not self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):
            return 0
        return (
            self.programLoans.filter(
                Q(loanStatus__name="CURRENT")
                | Q(loanStatus__name="RESTRUCTURED CURRENT")
                | Q(loanStatus__name="RESTRUCTURED")
            ).aggregate(totalAvailments=Sum(F("amount")))["totalAvailments"]
            / Decimal(totalLoans)
        ) * 100

    def getTotalAvailments(self, borrower):

        # if(not self.programLoans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),borrower=borrower)):
        #     return 0
        # return self.programLoans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),borrower=borrower).aggregate(totalAvailments=Sum(F('amount') ))['totalAvailments']

        if not self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            borrower=borrower,
        ):
            return 0

        loans = self.programLoans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED"),
            borrower=borrower,
        )
        totalAvailments = 0

        for loan in loans:

            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()
            print(loan.totalAmortizationPrincipal)
            totalAvailments = totalAvailments + loan.totalAmortizationPrincipal

        return totalAvailments

    def get_1to30Days(self):
        return 0

    def get_31to90Days(self):
        return 0

    def get_91to180Days(self):
        return 0

    def get_181to360Days(self):
        return 0

    def get_over360Days(self):
        return 0

    def get_total(self):
        return 0


class InterestRate(models.Model):

    interestRate = models.DecimalField(max_digits=5, decimal_places=2, blank=False)

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="interestRateCreatedBy",
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
        return "%s" % (self.interestRate)


class CreditLine(models.Model):
    borrower = models.ForeignKey(
        "borrowers.Borrower",
        on_delete=models.CASCADE,
        related_name="creditLines",
    )
    loanProgram = models.ForeignKey(
        LoanProgram,
        on_delete=models.CASCADE,
        related_name="programCreditLines",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    interestRate = models.ForeignKey(
        InterestRate,
        on_delete=models.CASCADE,
        related_name="creditLines",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        related_name="creditLines",
        null=True,
    )
    purpose = models.TextField(
        blank=True,
        null=True,
    )
    security = models.TextField(
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="creditLineStatuses",
    )
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="loanCreatedBy",
        null=True,
    )
    dateApproved = models.DateTimeField(blank=True, null=True)
    dateExpired = models.DateTimeField(blank=True, null=True)
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    dateUpdated = models.DateTimeField(
        auto_now=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )
    totalAvailment = 0

    def __str__(self):
        return "%s %s" % (self.borrower, self.amount)

    def getRemainingCreditLine(self):
        # totalLoanAvailments = self.loans.filter(loanStatus__name="CURRENT").aggregate(
        #     totalLoanAvailments=Sum(F("amount"))
        # )["totalLoanAvailments"]
        # if totalLoanAvailments:
        #     return self.amount - int(totalLoanAvailments)
        return self.amount - self.getTotalAvailment()

    # def getTotalAvailment(self):
    #     totalLoanAvailments=  self.loans.filter(loanStatus__name='CURRENT').aggregate(totalLoanAvailments=Sum(F('amount') ))['totalLoanAvailments']
    #     if totalLoanAvailments:
    #         return   int(totalLoanAvailments)
    #     return 0
    def getTotalAvailment(self):

        # if(not self.programLoans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),borrower=borrower)):
        #     return 0
        # return self.programLoans.filter(Q(loanStatus__name='CURRENT') | Q(loanStatus__name='RESTRUCTURED CURRENT') | Q(loanStatus__name='RESTRUCTURED'),borrower=borrower).aggregate(totalAvailments=Sum(F('amount') ))['totalAvailments']

        if not self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        ):
            return 0

        loans = self.loans.filter(
            Q(loanStatus__name="CURRENT")
            | Q(loanStatus__name="RESTRUCTURED CURRENT")
            | Q(loanStatus__name="RESTRUCTURED")
        )
        totalAvailments = 0
        totalPrincipalPayment = 0 
        for loan in loans:
            loan.totalAmortizationPrincipal = loan.getTotalAmortizationPrincipal()
            totalAvailments = totalAvailments + loan.totalAmortizationPrincipal

             
            totalPrincipalPayment = totalPrincipalPayment + loan.getTotalPrincipalPayment()

        totalAvailments = totalAvailments - totalPrincipalPayment
        print("totalPrincipalPayment")
        print(totalPrincipalPayment)
        return totalAvailments


class Loan(models.Model):
    pnNo = models.CharField(blank=True, null=True, max_length=25)
    borrower = models.ForeignKey(
        "borrowers.Borrower",
        on_delete=models.CASCADE,
        related_name="loans",
    )
    creditLine = models.ForeignKey(
        CreditLine,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    loanProgram = models.ForeignKey(
        LoanProgram,
        on_delete=models.CASCADE,
        related_name="programLoans",
    )
    interestRate = models.ForeignKey(
        InterestRate,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    # interestRate = models.DecimalField( max_digits=5, decimal_places=2,blank=False)
    term = models.ForeignKey(
        Term,
        on_delete=models.SET_NULL,
        related_name="loans",
        null=True,
    )
    purpose = models.TextField(
        blank=True,
        null=True,
        default="For relending within the coconut community with priority to coconut farmer members",
    )
    security = models.TextField(
        blank=True,
        null=True,
        default="Post-dated checks and JSS of BODs, Manager and Treasurer",
    )
    loanStatus = models.ForeignKey(
        LoanStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="loanStatuses",
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
        related_name="creditLineCreatedBy",
        null=True,
    )
    isRestructured = models.BooleanField(
        default=False,
    )
    dateApproved = models.DateTimeField(blank=True, null=True)
    dateReleased = models.DateTimeField(blank=True, null=True)
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
        return "%s %s %s %s" % (self.pnNo, self.id, self.borrower, self.amount)

    def getLatestAmortization(self):
        if self.isRestructured:
            return self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
        else:
            return self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()

    def getLatestDraftAmortization(self):
        return self.amortizations.filter(amortizationStatus__name="DRAFT").order_by("-id").first()

    def getLatestPayment(self):
        return self.payments.filter(paymentStatus__name="TENDERED").order_by("-id").first()

    def getTotalAmortizationAccruedInterest(self):
        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )

            if latestAmortization:
                totalInterests = latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID")
                if totalInterests:
                    return latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID").aggregate(
                        totalAmortizationInterest=Sum(F("accruedInterest"))
                    )["totalAmortizationInterest"]
                else:
                    return 0
        else:
            latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()
            if latestAmortization:
                return latestAmortization.amortizationItems.aggregate(
                    totalAmortizationInterest=Sum(F("accruedInterest"))
                )["totalAmortizationInterest"]
        return 0

    def getTotalAmortizationInterest(self):
        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )

            if latestAmortization:
                totalInterests = latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID")
                if totalInterests:
                    return latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID").aggregate(
                        totalAmortizationInterest=Sum(F("interest"))
                    )["totalAmortizationInterest"]
                else:
                    return 0
        else:
            latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()
            if latestAmortization:
                return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F("interest")))[
                    "totalAmortizationInterest"
                ]
        return 0

    def getTotalAmortizationPrincipal(self):
        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )

            if latestAmortization:
                totalInterests = latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID")
                if totalInterests:
                    return latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID").aggregate(
                        totalAmortizationPrincipal=Sum(round(F("principal"), 2))
                    )["totalAmortizationPrincipal"]

                else:
                    return 0
        else:

            # latestAmortization = self.amortizations.filter(amortizationStatus__name='UNPAID').order_by('-id').first()

            # if latestAmortization:
            #     return latestAmortization.amortizationItems.aggregate(totalAmortizationPrincipal=Sum(F('principal') ))['totalAmortizationPrincipal']
            return self.amount
        return 0

    def getTotalDraftAmortizationInterest(self):
        latestAmortization = self.amortizations.filter(amortizationStatus__name="DRAFT").order_by("-id").first()

        if latestAmortization:
            return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F("interest")))[
                "totalAmortizationInterest"
            ]
        return 0

    def getTotalDraftAmortizationAccruedInterest(self):
        latestAmortization = self.amortizations.filter(amortizationStatus__name="DRAFT").order_by("-id").first()

        if latestAmortization:
            return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F("accruedInterest")))[
                "totalAmortizationInterest"
            ]
        return 0

    # def getTotalAmortizationInterestByAmortization(self,amortizationId):

    #     latestAmortization = self.amortizations.filter(amortization__id=amortizationId,amortizationStatus__name='UNPAID').order_by('-id').first()

    #     if latestAmortization:
    #         return latestAmortization.amortizationItems.aggregate(totalAmortizationInterest=Sum(F('interest') ))['totalAmortizationInterest']
    #     return 0

    def getTotalObligations(self):

        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )
            if latestAmortization:
                totalObligations = latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID")
                if totalObligations:
                    return latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID").aggregate(
                        totalObligations=Sum(F("total"))
                    )["totalObligations"]
                else:
                    return 0
        else:
            latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()

            if latestAmortization:
                return latestAmortization.amortizationItems.aggregate(totalObligations=Sum(F("total")))[
                    "totalObligations"
                ]
        return 0

    def getTotalAmortizationPayment(self):
        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )
        else:
            latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()

        if latestAmortization:
            return latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F("total")))[
                "totalAmortizationPayment"
            ]
        return 0

    def getOutstandingBalance(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]

        if self.isRestructured:
            latestAmortization = (
                self.amortizations.filter(amortizationStatus__name="RESTRUCTURED").order_by("-id").first()
            )
            if latestAmortization:

                balance = latestAmortization.amortizationItems.filter(amortizationStatus__name="PAID").aggregate(
                    totalAmortizationPayment=Sum(F("total"))
                )["totalAmortizationPayment"]
                if balance:
                    return balance - totalPayments
                return 0

        else:
            latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()
            
            if latestAmortization:
                return (
                    latestAmortization.amortizationItems.aggregate(totalAmortizationPayment=Sum(F("total")))[
                        "totalAmortizationPayment"
                    ]
                    - totalPayments
                )

        return 0

    def getInterestBalance(self):

        latestPayment = self.payments.filter(paymentStatus__name="TENDERED").order_by("-id").first()

        if latestPayment:

            # return self.getTotalAmortizationInterest() -  latestPayment.amortizationItem.interest
            return (
                self.getTotalAmortizationInterest()
                - self.payments.filter(paymentStatus__name="TENDERED").aggregate(totalPaidInterest=Sum(F("interest")))[
                    "totalPaidInterest"
                ]
            )
        return 0

    def getTotalPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]
            return totalPayments

        return 0

    def getTotalPrincipalPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = (
                self.payments.aggregate(totalPayments=Sum(F("cash")))["totalPayments"]
                + self.payments.aggregate(totalPayments=Sum(F("check")))["totalPayments"]
            )
            return totalPayments

        return 0

    def getTotaInterestPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("interestPayment")))["totalPayments"]
            return totalPayments

        return 0

    def getTotalAccruedInterestPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("accruedInterestPayment")))["totalPayments"]
            return totalPayments

        return 0

    def getTotalPenaltyPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("penaltyPayment")))["totalPayments"]
            return totalPayments

        return 0

    def getTotalTotalInterestPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("interestPayment")))["totalPayments"] + (
                self.payments.aggregate(totalPayments=Sum(F("accruedInterestPayment")))["totalPayments"]
            )
            return totalPayments

        return 0

    def getTotalAdditionalInterestPayment(self):
        totalPayments = 0
        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("interestPayment")))["totalPayments"] - (
                self.payments.aggregate(totalPayments=Sum(F("interest")))["totalPayments"]
                - self.payments.aggregate(totalPayments=Sum(F("accruedInterest")))["totalPayments"]
            )
            return totalPayments

        return 0

    def getCurrentAmortizationItem(self):

        latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()
        amortizations = self.amortizations.filter(amortizationStatus__name="PAID")

        if latestAmortization:
            # i = 0
            # for item in latestAmortization.amortizationItems.order_by('id').all():
            #     if (i==amortizations.count()):
            #         return item
            #     i = i + 1
            latestAmortizationItem = (
                latestAmortization.amortizationItems.filter(
                    Q(amortizationStatus__name="UNPAID") | Q(amortizationStatus__name="PARTIAL")
                )
                .order_by("id")
                .first()
            )

            check = 0
            cash = 0
            interestPayment = 0
            accruedInterestPayment =0 
            if latestAmortizationItem:
                if latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("check")))["totalPayments"]:
                    check = latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("check")))["totalPayments"]

                if latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("cash")))["totalPayments"]:
                    cash = latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("cash")))["totalPayments"]

                if latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("interestPayment")))["totalPayments"]:
                    interestPayment = latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("interestPayment")))["totalPayments"]
                if latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("accruedInterestPayment")))["totalPayments"]:
                    accruedInterestPayment = latestAmortizationItem.payments.aggregate(totalPayments=Sum(F("accruedInterestPayment")))["totalPayments"]

                paidPrincipal = cash + check
                
                # print(paidPrincipal)
                latestAmortizationItem.principal = latestAmortizationItem.principal - paidPrincipal
                latestAmortizationItem.interest = latestAmortizationItem.interest - interestPayment - accruedInterestPayment
                latestAmortizationItem.accruedInterest = latestAmortizationItem.accruedInterest - accruedInterestPayment 
                latestAmortizationItem.total = latestAmortizationItem.principal  + latestAmortizationItem.interest     
            return latestAmortizationItem

    def getLastAmortizationItem(self):

        latestAmortization = (
            self.amortizations.filter(Q(amortizationStatus__name="UNPAID") | Q(amortizationStatus__name="RESTRUCTURED"))
            .order_by("-id")
            .first()
        )
        amortizations = self.amortizations.filter(amortizationStatus__name="PAID")

        if latestAmortization:
            return latestAmortization.amortizationItems.order_by("-id").first()

    def getLastAmortizationItemSchedule(self):
        latestAmortization = (
            self.amortizations.filter(Q(amortizationStatus__name="UNPAID") | Q(amortizationStatus__name="RESTRUCTURED"))
            .order_by("-id")
            .first()
        )
        amortizations = self.amortizations.filter(amortizationStatus__name="PAID")

        if latestAmortization:
            latestAmortizationItem = (
                latestAmortization.amortizationItems.filter(
                    Q(amortizationStatus__name="UNPAID") | Q(amortizationStatus__name="PARTIAL")
                )
                .order_by("id")
                .first()
            )
            if latestAmortizationItem:
                return latestAmortizationItem.schedule

    def getCurrentAmortization(self):

        latestAmortization = self.amortizations.filter(amortizationStatus__name="UNPAID").order_by("-id").first()

        return latestAmortization


class Amortization(models.Model):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="amortizations",
        blank=True,
        null=True,
    )
    amortizationStatus = models.ForeignKey(
        AmortizationStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="amortizationStatusesAmortizations",
    )
    dateReleased = models.DateTimeField(blank=True, null=True)
    schedules = models.PositiveIntegerField(blank=False, null=False, default=0)
    cycle = models.PositiveIntegerField(blank=False, null=False, default=0)
    termDays = models.PositiveIntegerField(blank=False, null=False, default=0)
    createdBy = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        related_name="amortizationCreatedBy",
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
        return "%s %s" % (self.loan, self.amortizationStatus.name)

    def getTotalAmortizationInterest(self):
        return self.amortizationItems.aggregate(totalAmortizationInterest=Sum(F("interest")))[
            "totalAmortizationInterest"
        ]

    def getTotalAmortizationAccruedInterest(self):
        return self.amortizationItems.aggregate(totalAmortizationInterest=Sum(F("accruedInterest")))[
            "totalAmortizationInterest"
        ]

    def getTotalAmortizationPrincipal(self):
        return self.amortizationItems.aggregate(totalAmortizationPrincipal=Sum(F("principal")))[
            "totalAmortizationPrincipal"
        ]

    def getTotalObligations(self):
        return self.amortizationItems.aggregate(totalObligations=Sum(F("total")))["totalObligations"]


# class IsCurrentAmortizationItem(models.Manager):
#     def get_queryset(self):
#         now = timezone.now()
#         start = now - datetime.timedelta(days=7)
#         return super(PublishedLastWeekManager, self).get_queryset().filter(published_date__range=[start, now])


class AmortizationItem(models.Model):
    amortization = models.ForeignKey(
        Amortization,
        on_delete=models.CASCADE,
        related_name="amortizationItems",
        blank=True,
        null=True,
    )

    
    days = models.PositiveIntegerField(blank=False, null=False, default=0)
    daysExceed = models.PositiveIntegerField(blank=False, null=False, default=0)
    daysAdvanced = models.PositiveIntegerField(blank=False, null=False, default=0)
    schedule = models.DateField(blank=True, null=True)
    principal = models.DecimalField(max_digits=12, decimal_places=3, blank=False)
    deductAccruedInterest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    accruedInterest = models.DecimalField(max_digits=12, decimal_places=3, blank=False)
    interest = models.DecimalField(max_digits=12, decimal_places=3, blank=False)
    additionalInterest = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    penalty = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    vat = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    principalBalance = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    amortizationStatus = models.ForeignKey(
        AmortizationStatus,
        on_delete=models.CASCADE,
        # limit_choices_to={'subProcess': document_.subProcess},
        related_name="amortizationItemStatuses",
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
        return "%s %s: %s %s" % (
            self.amortization.loan.id,
            self.id,
            self.schedule,
            self.amortizationStatus,
        )
    def loanId(self):
        return "%s" % (
            self.amortization.loan.id, 
        )
    def getPDC(self):
        latestPDC = self.checks.all().first()
        print(latestPDC)
        return latestPDC

    def isMaturingAmortizationItem(self):
        return self == self.amortization.loan.getCurrentAmortizationItem()

    def isOnCurrentAmortization(self):
        return self.amortization == self.amortization.loan.getCurrentAmortization()

    def getTotalPayment(self):
        totalPayments = 0

        if self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]:
            totalPayments = self.payments.aggregate(totalPayments=Sum(F("total")))["totalPayments"]
            return totalPayments
        return 0

    def getAging(self):
        delta = date.today() - self.schedule
        if int(delta.days) >= 1 and int(delta.days) <= 30:
            return "1-30 days"
        elif int(delta.days) >= 31 and int(delta.days) <= 90:
            return "31-90 days"
        elif int(delta.days) >= 91 and int(delta.days) <= 180:
            return "91-180 days"
        elif int(delta.days) >= 181 and int(delta.days) <= 360:
            return "181-360 days"
        else:
            return "Over 360 days"

    def getAgingOrder(self):
        delta = date.today() - self.schedule
        if int(delta.days) >= 1 and int(delta.days) <= 30:
            return 1
        elif int(delta.days) >= 31 and int(delta.days) <= 90:
            return 2
        elif int(delta.days) >= 91 and int(delta.days) <= 180:
            return 3
        elif int(delta.days) >= 181 and int(delta.days) <= 360:
            return 4
        else:
            return 5

    class Meta:
        ordering = ("id",)

    # def isPaid(self):
    #     if  (self.payments.filter(isDeleted=False).count() > 0):
    #         return 'PAID'
    #     return 'UNPAID'