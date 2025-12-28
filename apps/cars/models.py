from django.db import models
from django.contrib.auth import get_user_model
from .utils import car_image_upload_path

User = get_user_model()

class CarCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Car Cities"

class CarTransmission(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CarFuelType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CarType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class CarBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CarModelYear(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ['-year']

class CarPickupLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.ForeignKey(CarCity, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey('Car', related_name='car_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=car_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.car.title} - Image {self.id}"

class CarAvailability(models.Model):
    car = models.ForeignKey('Car', related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('car', 'date')
        ordering = ['date']
    
    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.car.title} - {self.date} - {status}"

class CarReview(models.Model):
    car = models.ForeignKey('Car', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    verified_booking = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('car', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.car.title} - {self.rating} stars"

class Car(models.Model):
    # Basic Info
    title = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model_year = models.ForeignKey(CarModelYear, on_delete=models.CASCADE)
    city = models.ForeignKey(CarCity, on_delete=models.CASCADE)
    pickup_locations = models.ManyToManyField(CarPickupLocation)
    
    # Technical Specifications
    transmission = models.ForeignKey(CarTransmission, on_delete=models.CASCADE, default=1)
    vehicle_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    seating_capacity = models.IntegerField()
    fuel_type = models.ForeignKey(CarFuelType, on_delete=models.CASCADE)
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)
    mileage = models.CharField(max_length=50, null=True, blank=True)
    baggage_capacity = models.CharField(max_length=50, null=True, blank=True)
    
    # Duration and Rental Options
    DURATION_CHOICES = [
        ('1day', '1 Day'),
        ('2-7days', '2-7 Days'),
        ('7+days', '7+ Days'),
    ]
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1day')
    
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
        """Get the primary image for the car"""
        primary_img = self.car_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        # Fallback to first available image
        first_img = self.car_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the car"""
        return [img.image.url for img in self.car_images.all() if img.image]

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