from django.contrib import admin
from .models import *

admin.site.register(Document)
admin.site.register(DocumentType)
admin.site.register(DocumentMovement)
admin.site.register(Signatory)