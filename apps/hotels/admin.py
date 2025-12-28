from django.contrib import admin
from .models import (
    HotelCity, PropertyType, BedPreference, HotelFacility, RoomFacility,
    ReservationType, OutdoorFeature, Hotel, HotelImage, HotelAvailability, HotelReview
)

@admin.register(HotelCity)
class HotelCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state')
    list_filter = ('state', 'country')

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(BedPreference)
class BedPreferenceAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(HotelFacility)
class HotelFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(RoomFacility)
class RoomFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ReservationType)
class ReservationTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(OutdoorFeature)
class OutdoorFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature',)
    search_fields = ('feature',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'property_type', 'bedrooms', 'bathrooms', 'price_per_day', 'available', 'service_provider')
    search_fields = ('title', 'description', 'city__name')
    list_filter = ('property_type', 'bed_preference', 'available', 'created_at')
    readonly_fields = ('rating', 'total_reviews', 'total_bookings', 'created_at', 'updated_at')
    filter_horizontal = ('facilities', 'room_facilities', 'outdoor_features')

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(HotelAvailability)
class HotelAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'date', 'is_available')
    list_filter = ('is_available', 'date')

@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'rating', 'verified_booking', 'created_at')
    list_filter = ('rating', 'verified_booking', 'created_at')