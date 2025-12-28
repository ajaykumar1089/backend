from django.contrib import admin
from .models import (
    CampervanCity, CampervanTransmission, CampervanFuelType, CampervanBrand,
    CampervanModelYear, CampervanToilet, CampervanShower, CampervanAmenity,
    CampervanPickupLocation, Campervan, CampervanImage, CampervanAvailability, CampervanReview
)

@admin.register(CampervanCity)
class CampervanCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state')
    list_filter = ('state', 'country')

@admin.register(CampervanTransmission)
class CampervanTransmissionAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CampervanFuelType)
class CampervanFuelTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CampervanBrand)
class CampervanBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CampervanModelYear)
class CampervanModelYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('-year',)

@admin.register(CampervanToilet)
class CampervanToiletAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CampervanShower)
class CampervanShowerAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CampervanAmenity)
class CampervanAmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(CampervanPickupLocation)
class CampervanPickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    search_fields = ('name', 'address')
    list_filter = ('city',)

@admin.register(Campervan)
class CampervanAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model_year', 'transmission', 'fuel_type', 'price_per_day', 'available', 'service_provider')
    search_fields = ('title', 'model', 'brand__name')
    list_filter = ('brand', 'fuel_type', 'transmission', 'available', 'created_at')
    readonly_fields = ('rating', 'total_reviews', 'total_trips', 'created_at', 'updated_at')
    filter_horizontal = ('pickup_locations', 'amenities')

@admin.register(CampervanImage)
class CampervanImageAdmin(admin.ModelAdmin):
    list_display = ('campervan', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(CampervanAvailability)
class CampervanAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('campervan', 'date', 'is_available')
    list_filter = ('is_available', 'date')

@admin.register(CampervanReview)
class CampervanReviewAdmin(admin.ModelAdmin):
    list_display = ('campervan', 'user', 'rating', 'verified_booking', 'created_at')
    list_filter = ('rating', 'verified_booking', 'created_at')