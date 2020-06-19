from django.db.models.signals import pre_save
from .models import RepairOrderModel
from django.dispatch import receiver
from .utils import unique_repair_order_id_generator


@receiver(pre_save, sender=RepairOrderModel)
def update_repai_order_id(sender, instance, **kwargs):
    if instance.order_id == "":
        instance.order_id = unique_repair_order_id_generator(instance)

# @receiver(pre_save, sender=ServiceReqModel)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()