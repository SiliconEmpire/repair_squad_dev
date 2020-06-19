from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=20)
    pick_up_address = models.TextField()
    state = models.CharField(max_length=300)
    city = models.CharField(max_length=300)

    # PhoneField(blank = True, help_text = 'Contact phone number', E164_only=False, default = '+2348132450841')
    def __str__(self):
        return f'{self.user.username} Profile'