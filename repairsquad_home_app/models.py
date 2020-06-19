from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class QuickRepairOrderModel(models.Model):
    request_status_choices = [
        ('PENDING', 'PENDING'),
        ('CALLED', 'CALLED'),
    ]
    
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    terms_and_condition = models.BooleanField(default = True)
    req_count = models.IntegerField( default = 1) 
    request_status = models.CharField(max_length=20, choices = request_status_choices, default = 'PENDING')
    order_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.name} Order'

class RepairOrderModel(models.Model):
    device_type_choices = [
        ('LAPTOP', 'LAPTOP'),
        ('PHONE', 'PHONE'),
        ('DESKTOP', 'DESKTOP'),
        ('WRISTWATCH', 'WRISTWATCH'),
        ('DRONE', 'DRONE'),
        ('LED/LCD TV', 'LED/LCD TV'),
        ('OTHERS', 'OTHERS'),
    ]
    
    order_tracking_choices = [
        ('PENDING', 'PENDING'),
        ('PICKED UP', 'PICKED UP'),
        ('REPAIR IN PROGRESS', 'REPAIR IN PROGRESS'),
        ('REPAIR DONE', 'REPAIR DONE'),
        ('READY FOR DELIVERY', 'READY FOR DELIVERY'),
        ('DELIVERED','DELIVERED')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, default="")
    device_type = models.CharField(max_length=20, choices = device_type_choices, default = 'LAPTOP')
    brand = models.CharField(max_length=120, default="")
    model = models.CharField(max_length=120, default="")
    serial_no_or_IMEI = models.CharField(max_length=120, default="")
    fault_details = models.TextField()
    pick_up_date = models.DateField()
    order_tracking = models.CharField(max_length=50, choices = order_tracking_choices, default = 'PENDING')
    coupon_code = models.CharField(max_length=20, default="")
    survey = models.TextField()
    terms_and_condition = models.BooleanField(default = False)
    order_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.owner.username} Repair Order'
    
    # def get_absolute_url(self):
    #     return reverse('', kwargs={'pk': self.pk})
    
    

    