from django.contrib import admin
# from django.contrib.admin import AdminSite
from .models import *



# class UCPBLMSAdmin(AdminSite):
#     site_header = 'UCPB LMS Administration'

# admin_site = AdminSite(name="ucpbadmin")
admin.site.site_header = "UCPB LMS Admin"
admin.site.site_title = "UCPB LMS Admin Portal"
admin.site.index_title = "Welcome to UCPB LMS Admin Portal"
admin.site.register(Loan)
admin.site.register(LoanProgram)
 
admin.site.register(Term)
admin.site.register(PaymentPeriod)
admin.site.register(Status)
admin.site.register(CreditLine)
admin.site.register(Amortization)
 
 
class AmortizationItemAdmin(admin.ModelAdmin):
    list_display = ('id','loanId','schedule','principal' ,'deductAccruedInterest','accruedInterest','interest','additionalInterest','penalty','total','principalBalance','amortizationStatus')
    class Meta:
        model=AmortizationItem 
          
admin.site.register(AmortizationItem,AmortizationItemAdmin) 
admin.site.register(AmortizationStatus)
admin.site.register(InterestRate)
admin.site.register(LoanStatus)
    