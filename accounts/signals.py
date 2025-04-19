from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, CustomUser
import pyotp
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
@receiver(post_save, sender=CustomUser)
def create_totp_secret(sender, instance, created, **kwargs):
    if created and not instance.totp_secret:
        instance.totp_secret = pyotp.random_base32()  # Generate unique TOTP secret
        instance.save()