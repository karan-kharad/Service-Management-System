from django.contrib import admin
from api.models import *

class RepairJobInline(admin.TabularInline):
    model = RepairJob 


class JobAdmin(admin.ModelAdmin):
    inline = [
        RepairJobInline
        ]
    
admin.site.register(RepairJob)    
# Register your models here.
