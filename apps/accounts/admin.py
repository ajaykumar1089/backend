from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'user_type', 'firm_name', 'is_verified', 'is_profile_public', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_profile_public', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'firm_name', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Info', {
            'fields': ('user_type', 'phone_number', 'profile_picture', 'preferences', 'social_links', 'location', 'is_profile_public')
        }),
        ('Service Provider Info', {
            'fields': ('firm_name', 'helpdesk_number', 'business_address', 'business_registration')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_contact_name')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_token', 'verification_token_expires')
        }),
    )

admin.site.register(User, UserAdmin)