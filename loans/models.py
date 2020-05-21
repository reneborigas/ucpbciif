from django.db import models
from django.utils import timezone
from borrowers.models import Borrower

class Loan(models.Model):
    borrower = models.OneToOneField(
        Borrower,
        on_delete=models.SET_NULL,
        related_name="loanBorrower",
        null = True,
    )
    loanName = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )    
    loanAmount = models.DecimalField(
        default = 0,
        max_length = 256,
        decimal_places = 2,
        max_digits = 20,
        blank = True,
        null = True
    )  