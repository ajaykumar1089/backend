from django.db import models
from django.contrib.auth import get_user_model
from .utils import trip_image_upload_path

User = get_user_model()

class TripRegion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TripCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.ForeignKey(TripRegion, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Trip Cities"

class TripDifficultyLevel(models.Model):
    level = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.level

class TripType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type

class SupportFeature(models.Model):
    feature = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.feature

class JoinType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type

class TripImage(models.Model):
    trip = models.ForeignKey('GuidedTrip', related_name='trip_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=trip_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.trip.trip_name} - Image {self.id}"

class GuidedTrip(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('2_wheeler', '2 Wheeler'),
        ('4_wheeler', '4 Wheeler'),
    ]

    # Basic Info
    trip_name = models.CharField(max_length=255)
    description = models.TextField()
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    trip_type = models.ForeignKey(TripType, on_delete=models.CASCADE)
    difficulty_level = models.ForeignKey(TripDifficultyLevel, on_delete=models.CASCADE)
    
    # Destinations & Region
    region = models.ForeignKey(TripRegion, on_delete=models.CASCADE, default=1)
    from_destination = models.ForeignKey(TripCity, on_delete=models.CASCADE, related_name='trips_from')
    to_destination = models.ForeignKey(TripCity, on_delete=models.CASCADE, related_name='trips_to')
    intermediate_stops = models.JSONField(default=list, blank=True)  # List of intermediate cities/places
    
    # Trip Details
    duration_days = models.IntegerField()
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    group_capacity = models.IntegerField()
    min_participants = models.IntegerField(default=1)
    current_participants = models.IntegerField(default=0)
    
    # Support Features
    support_features = models.ManyToManyField(SupportFeature, blank=True)
    join_type = models.ForeignKey(JoinType, on_delete=models.CASCADE, default=1)
    
    # Dates & Schedule
    start_date = models.DateField()
    end_date = models.DateField()
    trip_schedule = models.JSONField(default=dict, blank=True)  # Daily itinerary
    
    # Pricing
    fare_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    includes = models.JSONField(default=list, blank=True)  # What's included in the price
    excludes = models.JSONField(default=list, blank=True)  # What's not included
    
    # Trip Leader
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_trips')
    guide_name = models.CharField(max_length=255, null=True, blank=True)
    guide_contact = models.CharField(max_length=15, null=True, blank=True)
    guide_experience = models.TextField(null=True, blank=True)
    
    # Status & Availability
    is_active = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)
    registration_deadline = models.DateField()
    
    # Requirements
    requirements = models.TextField(blank=True)  # What participants need to bring/know
    terms_and_conditions = models.TextField()
    
    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_trips_completed = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trip_name

    @property
    def primary_image(self):
        """Get the primary image for the trip"""
        primary_img = self.trip_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.trip_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the trip"""
        return [img.image.url for img in self.trip_images.all() if img.image]

    class Meta:
        ordering = ['-created_at']

class TripParticipant(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    trip = models.ForeignKey(GuidedTrip, on_delete=models.CASCADE, related_name='participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    joined_date = models.DateTimeField(auto_now_add=True)
    special_requests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.participant.email} - {self.trip.trip_name}"

    class Meta:
        unique_together = ('trip', 'participant')