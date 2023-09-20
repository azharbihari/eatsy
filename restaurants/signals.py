from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from restaurants.models import Restaurant
import os
from PIL import Image


@receiver(pre_save, sender=Restaurant)
def delete_changed_image_on_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Restaurant.objects.get(pk=instance.pk)
            if old_instance.image != instance.image:
                if old_instance.image != 'restaurant_images/default_restaurant_image.svg':
                    old_instance.image.delete(save=False)
        except Restaurant.DoesNotExist:
            pass


@receiver(pre_delete, sender=Restaurant)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image and instance.image != 'restaurant_images/default_restaurant_image.svg':
        instance.image.delete(save=False)
