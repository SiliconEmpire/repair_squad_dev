from django.contrib import admin
from .models import (
    QuickRepairOrderModel,
    RepairOrderModel,
)

class Repair_Squad_Home_App_QuickRepairOrderModel_Admin(admin.ModelAdmin):
    list_display = ('name', 'phone_number','req_count', 'request_status',)
    search_fields = ('phone_number',)
    list_per_page = 50

# Register your models here.
admin.site.register(QuickRepairOrderModel, Repair_Squad_Home_App_QuickRepairOrderModel_Admin)

class Repair_Squad_Home_App_RepairOrderModel_Admin(admin.ModelAdmin):
    list_display = ('owner', 'order_id','pick_up_date', 'order_tracking', 'order_date',)
    search_fields = ('order_id',)
    list_filter = ('order_tracking','pick_up_date', 'order_date',)
    list_per_page = 50

admin.site.register(RepairOrderModel, Repair_Squad_Home_App_RepairOrderModel_Admin)