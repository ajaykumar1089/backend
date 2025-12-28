from django.db import models
from django.contrib.auth import get_user_model
from .utils import bike_image_upload_path

User = get_user_model()

class BikeCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Bike Cities"

class BikeTransmission(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class BikeFuelType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class BikeRentalType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class BikeBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BikeModelYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['-year']  # Show newest years first

class PickupLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.ForeignKey(BikeCity, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return self.name

class BikeImage(models.Model):
    bike = models.ForeignKey('Bike', related_name='bike_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=bike_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.bike.title} - Image {self.id}"

class BikeAvailability(models.Model):
    bike = models.ForeignKey('Bike', related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bike', 'date')
        ordering = ['date']
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.bike.title} - {self.date} - {status}"

class BikeReview(models.Model):
    bike = models.ForeignKey('Bike', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    verified_booking = models.BooleanField(default=False)  # True if user actually booked this bike
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bike', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.bike.title} - {self.rating} stars"

class Bike(models.Model):
    # Basic Info
    title = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey(BikeBrand, on_delete=models.CASCADE)
    model_year = models.ForeignKey(BikeModelYear, on_delete=models.CASCADE)  # Now properly normalized
    city = models.ForeignKey(BikeCity, on_delete=models.CASCADE)
    pickup_locations = models.ManyToManyField(PickupLocation)
    
    # Technical Specifications
    transmission = models.ForeignKey(BikeTransmission, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(BikeFuelType, on_delete=models.CASCADE)
    rental_type = models.ForeignKey(BikeRentalType, on_delete=models.CASCADE)
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)
    mileage = models.CharField(max_length=50, null=True, blank=True)
    
    # Pricing
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    safety_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Service Provider & Availability
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'service_provider'})
    operating_hours = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    
    # Details
    documents_required = models.TextField()
    terms_and_conditions = models.TextField()
    description = models.TextField(blank=True)
    
    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_trips = models.IntegerField(default=0)  # Number of completed trips
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} {self.model} - {self.title}"

    @property
    def primary_image(self):
        """Get the primary image for the bike"""
        primary_img = self.bike_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.bike_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the bike"""
        return [img.image.url for img in self.bike_images.all() if img.image]

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