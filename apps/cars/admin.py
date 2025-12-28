from django.contrib import admin
from .models import (
    CarCity, CarTransmission, CarFuelType, CarType, CarBrand, 
    CarModelYear, CarPickupLocation, Car, CarImage, CarAvailability, CarReview
)

@admin.register(CarCity)
class CarCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state')
    list_filter = ('state', 'country')

@admin.register(CarTransmission)
class CarTransmissionAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CarFuelType)
class CarFuelTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CarModelYear)
class CarModelYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('-year',)

@admin.register(CarPickupLocation)
class CarPickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    search_fields = ('name', 'address')
    list_filter = ('city',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model_year', 'transmission', 'fuel_type', 'price_per_day', 'available', 'service_provider')
    search_fields = ('title', 'model', 'brand__name')
    list_filter = ('brand', 'fuel_type', 'transmission', 'vehicle_type', 'available', 'created_at')
    readonly_fields = ('rating', 'total_reviews', 'total_trips', 'created_at', 'updated_at')

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')

@admin.register(CarAvailability)
class CarAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'is_available')
    list_filter = ('is_available', 'date')

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'verified_booking', 'created_at')
    list_filter = ('rating', 'verified_booking', 'created_at')