from django.contrib import admin
from .models import *

admin.site.register(Loan)
admin.site.register(Term)
admin.site.register(PaymentPeriod)
admin.site.register(Status)
 