from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    totp_secret = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    active_sessions = models.JSONField(default=list)
    device_authorizations = models.JSONField(default=list)

    def __str__(self):
        return f"profile of {self.user.username}: first_name({self.user.first_name}), last_name({self.user.last_name})"

    def get_full_profile(self):
        return {
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "bio": self.bio,
            "address": self.address,
            "phone_number": self.phone_number,
        }


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    was_successful = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"
