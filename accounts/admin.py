from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, ActivityLog

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('totp_secret', 'is_email_verified')}),
    )
    list_display = ('username', 'email', 'is_email_verified', 'is_staff', 'is_active')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address', 'was_successful']
