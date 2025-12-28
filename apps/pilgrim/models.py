from django.db import models
from django.contrib.auth import get_user_model
from .utils import pilgrim_image_upload_path

User = get_user_model()

class PilgrimRegion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PilgrimPackageType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type

class PilgrimFeature(models.Model):
    feature = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.feature

class PilgrimDifficultyLevel(models.Model):
    level = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.level

class PilgrimageDestination(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.ForeignKey(PilgrimRegion, on_delete=models.CASCADE, default=1)
    country = models.CharField(max_length=100, default='India')
    description = models.TextField()
    significance = models.TextField()  # Religious significance
    best_time_to_visit = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

class PilgrimTourImage(models.Model):
    tour = models.ForeignKey('PilgrimTour', related_name='tour_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pilgrim_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.tour.title} - Image {self.id}"

class PilgrimTour(models.Model):
    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()
    destinations = models.ManyToManyField(PilgrimageDestination)
    region = models.ForeignKey(PilgrimRegion, on_delete=models.CASCADE, default=1)
    state = models.CharField(max_length=100)
    
    # Tour Details
    duration_days = models.IntegerField()
    difficulty_level = models.ForeignKey(PilgrimDifficultyLevel, on_delete=models.CASCADE)
    package_type = models.ForeignKey(PilgrimPackageType, on_delete=models.CASCADE)
    max_participants = models.IntegerField()
    min_participants = models.IntegerField(default=1)
    
    # Features
    features = models.ManyToManyField(PilgrimFeature, blank=True)
    
    # Pricing & Includes
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    includes = models.JSONField(default=list, blank=True)  # What's included
    excludes = models.JSONField(default=list, blank=True)  # What's excluded
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    itinerary = models.JSONField(default=dict, blank=True)  # Day-wise schedule
    
    # Service Provider
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'service_provider'})
    guide_included = models.BooleanField(default=True)
    guide_languages = models.JSONField(default=list, blank=True)
    
    # Details
    requirements = models.TextField(blank=True)
    terms_and_conditions = models.TextField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.region} ({self.duration_days} days)"

    @property
    def primary_image(self):
        """Get the primary image for the tour"""
        primary_img = self.tour_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.tour_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the tour"""
        return [img.image.url for img in self.tour_images.all() if img.image]

    class Meta:
        ordering = ['-created_at']

class PilgrimHotelImage(models.Model):
    hotel = models.ForeignKey('PilgrimHotel', related_name='hotel_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=pilgrim_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.hotel.title} - Image {self.id}"

class PilgrimHotel(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('hotel', 'Hotel'),
        ('homestay', 'Homestay'),
        ('resort', 'Resort'),
        ('lodge', 'Lodge'),
        ('dharamshala', 'Dharamshala'),
        ('ashram', 'Ashram'),
        ('guesthouse', 'Guesthouse'),
    ]
    
    BED_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('queen', 'Queen'),
        ('king', 'King'),
        ('dormitory', 'Dormitory'),
    ]

    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.ForeignKey(PilgrimRegion, on_delete=models.CASCADE, default=1)
    address = models.TextField()
    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    
    # Accommodation Details
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bed_preference = models.CharField(max_length=50, choices=BED_TYPE_CHOICES)
    guest_capacity = models.IntegerField()
    
    # Facilities
    facilities = models.JSONField(default=list, blank=True)  # Hotel facilities
    room_facilities = models.JSONField(default=list, blank=True)  # Room facilities
    religious_facilities = models.JSONField(default=list, blank=True)  # Prayer room, temple nearby, etc.
    
    # Pricing
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meals_included = models.BooleanField(default=False)
    meal_type = models.CharField(max_length=100, blank=True)  # Vegetarian, Jain, etc.
    
    # Location & Proximity
    near_destinations = models.ManyToManyField(PilgrimageDestination, blank=True)
    distance_to_temple = models.CharField(max_length=100, blank=True)  # Distance to main pilgrimage site
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Service Provider
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'service_provider'})
    
    # Details
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    terms_and_conditions = models.TextField()
    
    # Status
    available = models.BooleanField(default=True)
    
    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"

    @property
    def primary_image(self):
        """Get the primary image for the hotel"""
        primary_img = self.hotel_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.hotel_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the hotel"""
        return [img.image.url for img in self.hotel_images.all() if img.image]

    class Meta:
        ordering = ['-created_at']