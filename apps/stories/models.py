from django.db import models
from django.contrib.auth import get_user_model
from .utils import story_image_upload_path

User = get_user_model()


class UserstoriesPlaceType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type


class UserstoriesJourneyType(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.type


class UserstoriesCity(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Stories Cities"


class Userstories(models.Model):
    # Basic Info
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    # Location Details
    city = models.ForeignKey(UserstoriesCity, on_delete=models.CASCADE)
    specific_place = models.CharField(max_length=255, null=True, blank=True)
    place_type = models.ForeignKey(UserstoriesPlaceType, on_delete=models.CASCADE)
    journey_type = models.ForeignKey(UserstoriesJourneyType, on_delete=models.CASCADE)

    # Journey Details
    duration_days = models.IntegerField(null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)

    # stories Details
    summary = models.TextField(max_length=500, help_text="Brief summary of the story")
    tags = models.JSONField(default=list, blank=True)

    # Interactions
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.email}"

    @property
    def primary_image(self):
        """Get the primary image for the story"""
        primary_img = self.story_images.filter(is_primary=True).first()
        if primary_img and primary_img.image:
            return primary_img.image.url
        first_img = self.story_images.first()
        if first_img and first_img.image:
            return first_img.image.url
        return None

    @property
    def all_images(self):
        """Get all image URLs for the story"""
        return [img.image.url for img in self.story_images.all() if img.image]

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Stories"


class UserstoriesImage(models.Model):
    story = models.ForeignKey(Userstories, related_name='story_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=story_image_upload_path, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.story.title} - Image {self.id}"


class UserstoriesLike(models.Model):
    story = models.ForeignKey(Userstories, on_delete=models.CASCADE, related_name='story_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')


class UserstoriesComment(models.Model):
    story = models.ForeignKey(Userstories, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.story.title}"

    class Meta:
        ordering = ['created_at']
