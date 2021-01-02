from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Notification


@receiver(post_save)
def my_handler(sender, instance, created, **kwargs):
    # Returns false if 'sender' is NOT a subclass of AbstractModel
    if not issubclass(sender, Event):
        return
    else:
        Notification.objects.create(
            profile=instance.user_to,
            message=instance.get_notification_str()
        )