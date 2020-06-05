from django.contrib import admin
from .models import *

admin.site.register(Process)
admin.site.register(SubProcess)
admin.site.register(Statuses)
admin.site.register(Requirements)
admin.site.register(Step)
admin.site.register(Output)