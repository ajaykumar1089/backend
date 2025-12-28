from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('traveller', 'Traveller'),
        ('service_provider', 'Service Provider'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='traveller')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    preferences = models.TextField(null=True, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    
    # Profile Privacy
    is_profile_public = models.BooleanField(default=True)
    
    # Service Provider specific fields
    firm_name = models.CharField(max_length=255, null=True, blank=True)
    helpdesk_number = models.CharField(max_length=15, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    business_registration = models.CharField(max_length=100, null=True, blank=True)
    
    # Additional contact info
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    verification_token_expires = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_traveller(self):
        return self.user_type == 'traveller'
    
    @property
    def is_service_provider(self):
        return self.user_type == 'service_provider'
    
    @property
    def display_name(self):
        """Get the display name for the user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.firm_name and self.is_service_provider:
            return self.firm_name
        else:
            return self.email
    
    def generate_verification_token(self):
        """Generate a new verification token that expires in 24 hours"""
        self.verification_token = str(uuid.uuid4())
        self.verification_token_expires = timezone.now() + timedelta(hours=24)
        # Don't save here - let the caller handle saving for better control
        return self.verification_token
    
    def is_verification_token_valid(self, token):
        """Check if the verification token is valid and not expired"""
        if not self.verification_token or not self.verification_token_expires:
            return False
        
        return (
            self.verification_token == token and 
            timezone.now() < self.verification_token_expires
        )