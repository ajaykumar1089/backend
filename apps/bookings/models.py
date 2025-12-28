from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import random
import string

User = get_user_model()

class Booking(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('campervan', 'Campervan'),
        ('hotel', 'Hotel'),
        ('guided_trip', 'Guided Trip'),
        ('pilgrim_tour', 'Pilgrim Tour'),
        ('pilgrim_hotel', 'Pilgrim Hotel'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]

    # Basic Info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_reference = models.CharField(max_length=20, unique=True)
    
    # Service Details (Generic Foreign Key)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    service_object = GenericForeignKey('content_type', 'object_id')
    
    # Booking Dates
    booking_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_days = models.IntegerField()
    
    # Pricing
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Additional Details
    special_requests = models.TextField(blank=True)
    pickup_location = models.CharField(max_length=255, blank=True)
    drop_location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)  # Internal notes for service provider
    
    # Contact Info
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    emergency_contact = models.CharField(max_length=15, blank=True)
    
    # Documents (for verification)
    documents_submitted = models.JSONField(default=dict, blank=True)  # Store document info
    documents_verified = models.BooleanField(default=False)
    
    # Service Provider
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_bookings', limit_choices_to={'user_type': 'service_provider'})
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_bookings')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.user.email} - {self.service_type}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate unique booking reference
            while True:
                ref = 'TC' + ''.join(random.choices(string.digits, k=8))
                if not Booking.objects.filter(booking_reference=ref).exists():
                    self.booking_reference = ref
                    break
        super().save(*args, **kwargs)

    @property
    def can_be_cancelled(self):
        """Check if booking can be cancelled based on status and timing"""
        if self.status in ['completed', 'cancelled', 'refunded']:
            return False
        return True

    @property
    def is_active(self):
        """Check if booking is currently active"""
        return self.status == 'active'

class BookingPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.booking.booking_reference}"

class BookingReview(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review_text = models.TextField()
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.booking_reference} - {self.rating} stars"

    class Meta:
        unique_together = ('booking', 'user')