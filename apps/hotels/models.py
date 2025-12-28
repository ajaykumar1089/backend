from django.db import models
from django.contrib.auth import get_user_model
from .utils import hotel_image_upload_path

User = get_user_model()

class HotelCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Hotel Cities"

class PropertyType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class BedPreference(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class HotelFacility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Hotel Facilities"

class RoomFacility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Room Facilities"

class ReservationType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class OutdoorFeature(models.Model):
    feature = models.CharField(max_length=100)

    def __str__(self):
        return self.feature

class HotelImage(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='hotel_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.hotel.title} - Image {self.id}"

class HotelAvailability(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hotel', 'date')
        ordering = ['date']
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.hotel.title} - {self.date} - {status}"

class HotelReview(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    verified_booking = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hotel', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.hotel.title} - {self.rating} stars"

class Hotel(models.Model):
    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.ForeignKey(HotelCity, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    address = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    
    # Room Details
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    bed_preference = models.ForeignKey(BedPreference, on_delete=models.CASCADE)
    guest_capacity = models.IntegerField()
    
    # Duration Options
    DURATION_CHOICES = [
        ('1week', '1 Week'),
        ('1month', '1 Month'),
        ('6months', '6 Months'),
    ]
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1week')
    
    # Reservation & Outdoor
    reservation_type = models.ForeignKey(ReservationType, on_delete=models.CASCADE, default=1)
    outdoor_features = models.ManyToManyField(OutdoorFeature, blank=True)
    
    # Facilities & Amenities
    facilities = models.ManyToManyField(HotelFacility, blank=True)
    room_facilities = models.ManyToManyField(RoomFacility, blank=True)
    
    # Pricing
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    safety_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Service Provider & Availability
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'service_provider'})
    operating_hours = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    
    # Location
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Details
    documents_required = models.TextField()
    terms_and_conditions = models.TextField()
    
    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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

    def update_rating(self):
        """Update the average rating and total reviews count"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.0
            self.total_reviews = reviews.count()
        else:
            self.rating = 0.0
            self.total_reviews = 0
        self.save()

    @property
    def average_rating(self):
        """Get current average rating"""
        return round(self.rating, 1)

    @property
    def rating_breakdown(self):
        """Get rating breakdown (count for each star level)"""
        breakdown = {i: 0 for i in range(1, 6)}
        for review in self.reviews.all():
            breakdown[review.rating] += 1
        return breakdown

    class Meta:
        ordering = ['-created_at']