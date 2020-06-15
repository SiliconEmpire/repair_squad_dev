from django.contrib import admin
from .models import (
    QuickRepairOrderModel,
)

class Repair_Squad_Home_App_QuickRepairOrderModel_Admin(admin.ModelAdmin):
    list_display = ('name', 'phone_number','req_count', 'request_status',)
    search_fields = ('phone_number',)
    list_per_page = 50

# Register your models here.
admin.site.register(QuickRepairOrderModel, Repair_Squad_Home_App_QuickRepairOrderModel_Admin)