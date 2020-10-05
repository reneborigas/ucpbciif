from django.db import models

class Vendor(models.Model):
    vendorName = models.CharField(
        max_length=255,
    )
    tinNumber = models.CharField(
        max_length=255,
        blank = True,
        null = True,
    )
    status = models.CharField(
        max_length=255,
        blank = True,
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
        related_name="vendorCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return "%s" % (self.vendorName)

class Contact(models.Model):
    borrower = models.OneToOneField(
        'borrowers.Borrower',
        on_delete=models.SET_NULL,
        related_name="contactBorrower",
        null = True,
        blank=True,
    )
    vendor = models.OneToOneField(
        Vendor,
        on_delete=models.SET_NULL,
        related_name="contactVendor",
        null = True,
        blank=True,
    )
    accountTypeChoice = (
        ('Vendor', 'Vendor'),
        ('Borrower', 'Borrower'),
    )
    accountType = models.CharField(
        max_length=10,
        choices = accountTypeChoice,
        default='Borrower',
    )

    def __str__(self):
        if (self.borrower):
            return "%s - %s" % (self.borrower, self.accountType)
        else:
            return "%s - %s" % (self.vendor, self.accountType)

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

class Taxes(models.Model):
    title = models.CharField(
        max_length=255,
    )
    isEnabled = models.BooleanField(
        default=True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="taxesCreatedBy",
        null = True,
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField( 
        default=False,
    )

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name = "Taxes (System Essential)"
        verbose_name_plural = "Taxes (System Essential)"

class TaxesRates(models.Model):
    tax = models.ForeignKey(
        'accounting.Taxes',
        on_delete=models.CASCADE,
        related_name="taxesRates",
    )
    rateName = models.TextField(
        blank = True,
        null = True,
    )
    taxRate = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    typeOfTaxChoice = (
        ('Normal', 'Normal'),
        ('Compounded', 'Compounded'),
    )
    typeOfTax = models.CharField(
        max_length=10,
        choices = typeOfTaxChoice,
        default='Normal',
    )

    def __str__(self):
        return "%s %s" % (self.tax, self.taxRate)

    class Meta:
        verbose_name = "Taxes Rate (System Essential)"
        verbose_name_plural = "Taxes Rates (System Essential)"

class TransactionType(models.Model):
    code = models.CharField(
        max_length=255,
    )
    title = models.CharField(
        max_length=255,
    )
    seriesLength = models.IntegerField(
        blank = True,
        null = True,
    )
    seriesStart = models.IntegerField(
        blank = True,
        null = True,
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="transactionTypeCreatedBy",
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
        verbose_name = "Transaction Type (System Essential)"
        verbose_name_plural = "Transaction Types (System Essential)"

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="transactionContact"
    )
    transactionType = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name="transactionTransactionType"
    )
    transactionNumber = models.TextField(
    )
    reference = models.TextField(
        blank = True,
        null = True,
    )
    transactionDate= models.DateField(
    )
    transactionDueDate = models.DateField(
        null=True,
        blank=True
    )
    transactionAmount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
    )
    transactionTax = models.TextField(
    )
    remarks = models.TextField(
        blank = True,
        null = True,
    )
    notes = models.TextField(
        blank = True,
        null = True,
    )
    status = models.TextField(
        blank = True,
        null = True,
    )
    checkNo = models.CharField(
        max_length=255,
        blank = True,
        null = True, 
    )
    createdBy = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name="transactionCreatedBy",
        null = True,
    )
    dateCreated = models.DateTimeField(
        auto_now_add=True,
    )
    isDeleted = models.BooleanField( 
        default=False,
    )

    def __str__(self):
        return "%s - %s (%s) - %s" % (self.transactionType,self.transactionNumber,self.status, self.transactionAmount)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

class TransactionDetails(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="transactionDetails"
    )
    reference = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="referenceTransactionDetail",
        null=True,
        blank=True,
    )
    item = models.TextField(
        blank = True,
        null = True,
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    quantity = models.IntegerField(
        blank = True,
        null = True,
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    discountRate = models.IntegerField(
        blank = True,
        null = True,
    )
    discountAmount = models.IntegerField(
        blank = True,
        null = True,
    )
    chartOfAccount = models.ForeignKey(
        ChartOfAccount,
        on_delete=models.SET_NULL,
        related_name="transactionChartOfAccount",
        blank = True,
        null = True,
    )
    chartOfAccountMovementChoice = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    )
    chartOfAccountMovement = models.CharField(
        max_length=10,
        choices = chartOfAccountMovementChoice,
        default='Debit',
    )
    totalAmount = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )

    def __str__(self):
        return "%s for %s - %s (%s)" % (self.transaction,self.chartOfAccountDebited, self.chartOfAccountCredited,self.totalAmount)

    class Meta:
        verbose_name = "Transaction Detail"
        verbose_name_plural = "Transaction Details"

class TransactionAllocations(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="allocation"
    )
    reference = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="referenceAllocation",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    allocationDate = models.DateField(
    )

    def __str__(self):
        return "%s for %s - %s" % (self.transaction,self.reference, self.amount)

    class Meta:
        verbose_name = "Transaction Allocation"
        verbose_name_plural = "Transaction Allocations"

class TransactionActions(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="actions"
    )
    action = models.TextField(
        blank = True,
        null = True,
    )
    committee = models.ForeignKey(
        'committees.Committee',
        on_delete=models.CASCADE,
        related_name="transactionActionsCommitee",
    )
    verified = models.BooleanField(
        default=False,
    )


    def __str__(self):
        return "%s : %s by %s - %s" % (self.transaction,self.action, self.committee, self.verified)

    class Meta:
        verbose_name = "Transaction Allocation"
        verbose_name_plural = "Transaction Allocations"