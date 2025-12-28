from django.db import models
from django.contrib.auth import get_user_model
from .utils import campervan_image_upload_path

User = get_user_model()

class CampervanCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Campervan Cities"

class CampervanTransmission(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CampervanFuelType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CampervanBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CampervanModelYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['-year']

class CampervanToilet(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CampervanShower(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CampervanAmenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Campervan Amenities"

class CampervanPickupLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.ForeignKey(CampervanCity, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return self.name

class CampervanImage(models.Model):
    campervan = models.ForeignKey('Campervan', related_name='campervan_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=campervan_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.campervan.title} - Image {self.id}"

class CampervanAvailability(models.Model):
    campervan = models.ForeignKey('Campervan', related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campervan', 'date')
        ordering = ['date']
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.campervan.title} - {self.date} - {status}"

class CampervanReview(models.Model):
    campervan = models.ForeignKey('Campervan', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    verified_booking = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campervan', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.campervan.title} - {self.rating} stars"

class Campervan(models.Model):
    # Basic Info
    title = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey(CampervanBrand, on_delete=models.CASCADE)
    model_year = models.ForeignKey(CampervanModelYear, on_delete=models.CASCADE)
    city = models.ForeignKey(CampervanCity, on_delete=models.CASCADE)
    pickup_locations = models.ManyToManyField(CampervanPickupLocation)
    
    # Technical Specifications
    transmission = models.ForeignKey(CampervanTransmission, on_delete=models.CASCADE, default=1)
    fuel_type = models.ForeignKey(CampervanFuelType, on_delete=models.CASCADE)
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)
    mileage = models.CharField(max_length=50, null=True, blank=True)
    seating_capacity = models.IntegerField()
    sleeping_capacity = models.IntegerField()
    baggage_capacity = models.CharField(max_length=50, null=True, blank=True)
    
    # Duration and Rental Options
    DURATION_CHOICES = [
        ('1day', '1 Day'),
        ('2-7days', '2-7 Days'),
        ('7+days', '7+ Days'),
    ]
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1day')
    
    # Amenities & Features
    toilet = models.ForeignKey(CampervanToilet, on_delete=models.CASCADE)
    shower = models.ForeignKey(CampervanShower, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(CampervanAmenity, blank=True)
    
    # Pricing
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
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
    total_trips = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} {self.model} - {self.title}"

    @property
    def primary_image(self):
        """Get the primary image for the campervan"""
        primary_img = self.campervan_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.campervan_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the campervan"""
        return [img.image.url for img in self.campervan_images.all() if img.image]

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