from django.contrib import admin
from .models import (
    UserstoriesPlaceType, UserstoriesJourneyType, UserstoriesCity, Userstories, 
    UserstoriesImage, UserstoriesLike, UserstoriesComment
)

@admin.register(UserstoriesPlaceType)
class storiesPlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type',)

@admin.register(UserstoriesJourneyType)
class storiesJourneyTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type',)

@admin.register(UserstoriesCity)
class UserstoriesCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state')
    list_filter = ('state', 'country')

@admin.register(Userstories)
class UserstoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'city', 'place_type', 'journey_type', 'is_featured', 'likes', 'views', 'created_at')
    list_filter = ('place_type', 'journey_type', 'is_featured', 'is_approved', 'created_at')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('likes', 'views', 'created_at', 'updated_at')

@admin.register(UserstoriesImage)
class UserstoriesImageAdmin(admin.ModelAdmin):
    list_display = ('story', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(UserstoriesLike)
class UserstoriesLikeAdmin(admin.ModelAdmin):
    list_display = ('story', 'user', 'created_at')

@admin.register(UserstoriesComment)
class UserstoriesCommentAdmin(admin.ModelAdmin):
    list_display = ('story', 'user', 'content', 'parent', 'created_at')
    list_filter = ('created_at',)