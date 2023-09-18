from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from accounts.models import Account


@receiver(pre_save, sender=Account)
def delete_changed_avatar_on_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Account.objects.get(pk=instance.pk)
            if old_instance.avatar != instance.avatar:
                if old_instance.avatar != 'avatars/default_avatar.png':
                    old_instance.avatar.delete(save=False)
        except Account.DoesNotExist:
            pass


@receiver(pre_delete, sender=Account)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar and instance.avatar != 'avatars/default_avatar.png':
        instance.avatar.delete(save=False)
