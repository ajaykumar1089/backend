from django.contrib import admin
from .models import InsightCategory, TravelInsight, InsightLike, InsightComment

@admin.register(InsightCategory)
class InsightCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon')
    search_fields = ('name',)

@admin.register(TravelInsight)
class TravelInsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'insight_type', 'category', 'author', 'is_published', 'is_featured', 'views', 'created_at')
    list_filter = ('insight_type', 'category', 'is_published', 'is_featured', 'created_at')
    search_fields = ('title', 'content', 'summary')
    readonly_fields = ('views', 'likes', 'shares', 'created_at', 'updated_at')
    
@admin.register(InsightLike)
class InsightLikeAdmin(admin.ModelAdmin):
    list_display = ('insight', 'user', 'created_at')
    
@admin.register(InsightComment)
class InsightCommentAdmin(admin.ModelAdmin):
    list_display = ('insight', 'user', 'content', 'parent', 'created_at')
    list_filter = ('created_at',)