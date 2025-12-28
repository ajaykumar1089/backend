from django.contrib import admin
from .models import (
    TripRegion, TripCity, TripDifficultyLevel, TripType, SupportFeature,
    JoinType, GuidedTrip, TripImage, TripParticipant
)

@admin.register(TripRegion)
class TripRegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TripCity)
class TripCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'region', 'country')
    search_fields = ('name', 'state')
    list_filter = ('region', 'state', 'country')

@admin.register(TripDifficultyLevel)
class TripDifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'description')
    search_fields = ('level',)

@admin.register(TripType)
class TripTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type',)

@admin.register(SupportFeature)
class SupportFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature', 'description')
    search_fields = ('feature',)

@admin.register(JoinType)
class JoinTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type',)

@admin.register(GuidedTrip)
class GuidedTripAdmin(admin.ModelAdmin):
    list_display = ('trip_name', 'vehicle_type', 'region', 'difficulty_level', 'duration_days', 'fare_per_person', 'is_active', 'created_at')
    list_filter = ('vehicle_type', 'region', 'difficulty_level', 'trip_type', 'is_active', 'created_at')
    search_fields = ('trip_name', 'description', 'created_by__email')
    readonly_fields = ('rating', 'total_reviews', 'total_trips_completed', 'created_at', 'updated_at')

@admin.register(TripImage)
class TripImageAdmin(admin.ModelAdmin):
    list_display = ('trip', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(TripParticipant)
class TripParticipantAdmin(admin.ModelAdmin):
    list_display = ('trip', 'participant', 'status', 'joined_date')
    list_filter = ('status', 'joined_date')