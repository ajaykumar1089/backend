from django.db import models
from django.contrib.auth import get_user_model
from .utils import fulltour_image_upload_path
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

User = get_user_model()


def itinerary_image_upload_path(instance, filename):
    # uploads/itineraries/fulltour_title/filename.jpg
    return f"itineraries/{instance.itinerary.fulltour.title}/{filename}"


class Itinerary(models.Model):
    fulltour = models.ForeignKey(
        'Fulltour',  # use string reference to avoid circular import
        related_name='itineraries',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    dayNum = models.CharField(max_length=200, default='Day')
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    description = RichTextUploadingField()  # Rich textbox here #models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Itineraries"

    def __str__(self):
        return f"{self.name}, {self.state_province}"


class ItineraryImage(models.Model):
    itinerary = models.ForeignKey(
        'Itinerary',
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=itinerary_image_upload_path)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Itinerary Images"

    def __str__(self):
        return f"{self.alt_text}"


class FullTourCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Fulltour Cities"

    def __str__(self):
        return f"{self.name}, {self.state}"


class PickupLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.ForeignKey(FullTourCity, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    def __str__(self):
        return self.name


class FulltourImage(models.Model):
    fulltour = models.ForeignKey('Fulltour', related_name='fulltour_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=fulltour_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.fulltour.title} - Image {self.id}"


class FulltourAvailability(models.Model):
    fulltour = models.ForeignKey('Fulltour', related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fulltour', 'date')
        ordering = ['date']

    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.fulltour.title} - {self.date} - {status}"


class FulltourReview(models.Model):
    fulltour = models.ForeignKey('Fulltour', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    verified_booking = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fulltour', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.fulltour.title} - {self.rating} stars"


class Fulltour(models.Model):
    # Basic Info
    title = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(FullTourCity, on_delete=models.CASCADE)
    pickup_locations = models.ManyToManyField(PickupLocation)

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
    terms_and_conditions = RichTextUploadingField()  # Rich textbox here #models.TextField()
    description = RichTextUploadingField()  # Rich textbox here#models.TextField(blank=True)

    # Reviews & Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_trips = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def primary_image(self):
        """Get the primary image for the fulltour"""
        primary_img = self.fulltour_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        first_img = self.fulltour_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the fulltour"""
        return [img.image.url for img in self.fulltour_images.all() if img.image]

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
