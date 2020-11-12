from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import Signal, receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile._default_manager.get_or_create(user=instance)


user_registered = Signal()
user_verified = Signal()
