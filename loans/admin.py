from django.contrib import admin
from .models import *

admin.site.register(Loan)
admin.site.register(LoanProgram)
 
admin.site.register(Term)
admin.site.register(PaymentPeriod)
admin.site.register(Status)
admin.site.register(CreditLine)
admin.site.register(Amortization)
admin.site.register(AmortizationItem)
admin.site.register(AmortizationStatus)
admin.site.register(InterestRate)
  