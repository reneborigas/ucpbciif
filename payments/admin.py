from django.contrib import admin
from .models import *

admin.site.register(Payment)
admin.site.register(PaymentStatus)
 
admin.site.register(PaymentType) 