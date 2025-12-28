from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class InsightCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For frontend icons

    def __str__(self):
        return self.name

class TravelInsight(models.Model):
    INSIGHT_TYPE_CHOICES = [
        ('tip', 'Travel Tip'),
        ('trend', 'Travel Trend'),
        ('destination', 'Destination Info'),
        ('seasonal', 'Seasonal Info'),
        ('budget', 'Budget Guide'),
        ('safety', 'Safety Info'),
        ('culture', 'Cultural Info'),
        ('food', 'Food Guide'),
        ('transport', 'Transport Info'),
        ('accommodation', 'Accommodation Guide'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for listing")
    insight_type = models.CharField(max_length=50, choices=INSIGHT_TYPE_CHOICES)
    category = models.ForeignKey(InsightCategory, on_delete=models.CASCADE)
    
    # Location relevance
    relevant_states = models.JSONField(default=list, blank=True)  # States this insight applies to
    relevant_cities = models.JSONField(default=list, blank=True)  # Cities this insight applies to
    is_global = models.BooleanField(default=False)  # If true, applies everywhere
    
    # Content details
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='insights/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    
    # SEO and metadata
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    
    # Publishing
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class InsightLike(models.Model):
    insight = models.ForeignKey(TravelInsight, on_delete=models.CASCADE, related_name='insight_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('insight', 'user')

class InsightComment(models.Model):
    insight = models.ForeignKey(TravelInsight, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.insight.title}"

    class Meta:
        ordering = ['created_at']