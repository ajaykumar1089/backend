from django.contrib import admin
from .models import (
    PilgrimRegion, PilgrimPackageType, PilgrimFeature, PilgrimDifficultyLevel,
    PilgrimageDestination, PilgrimTour, PilgrimTourImage, PilgrimHotel, PilgrimHotelImage
)

@admin.register(PilgrimRegion)
class PilgrimRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(PilgrimPackageType)
class PilgrimPackageTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type',)

@admin.register(PilgrimFeature)
class PilgrimFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature', 'description')
    search_fields = ('feature',)

@admin.register(PilgrimDifficultyLevel)
class PilgrimDifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'description')
    search_fields = ('level',)

@admin.register(PilgrimageDestination)
class PilgrimageDestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'region', 'best_time_to_visit')
    search_fields = ('name', 'city', 'state')
    list_filter = ('region', 'state', 'country')

@admin.register(PilgrimTour)
class PilgrimTourAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'state', 'duration_days', 'package_type', 'price_per_person', 'is_active', 'service_provider')
    search_fields = ('title', 'description', 'state')
    list_filter = ('region', 'package_type', 'difficulty_level', 'is_active', 'created_at')
    readonly_fields = ('rating', 'total_reviews', 'total_bookings', 'created_at', 'updated_at')
    filter_horizontal = ('destinations', 'features')

@admin.register(PilgrimTourImage)
class PilgrimTourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(PilgrimHotel)
class PilgrimHotelAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'state', 'region', 'property_type', 'price_per_night', 'available', 'service_provider')
    search_fields = ('title', 'description', 'city', 'state')
    list_filter = ('region', 'property_type', 'bed_preference', 'available', 'created_at')
    readonly_fields = ('rating', 'total_reviews', 'total_bookings', 'created_at', 'updated_at')
    filter_horizontal = ('near_destinations',)

@admin.register(PilgrimHotelImage)
class PilgrimHotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')