from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Bike, BikeBrand, BikeCity, BikeFuelType, BikeTransmission, BikeRentalType, 
    PickupLocation, BikeImage, BikeModelYear, BikeAvailability, BikeReview
)

class BikeImageInline(admin.TabularInline):
    model = BikeImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(BikeImage)
class BikeImageAdmin(admin.ModelAdmin):
    list_display = ('bike', 'is_primary', 'image_preview', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('bike__title', 'alt_text')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(BikeBrand)
class BikeBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BikeModelYear)
class BikeModelYearAdmin(admin.ModelAdmin):
    list_display = ('year',)
    ordering = ('-year',)

@admin.register(BikeCity)
class BikeCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state')

@admin.register(BikeFuelType)
class BikeFuelTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(BikeTransmission)
class BikeTransmissionAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(BikeRentalType)
class BikeRentalTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    list_filter = ('city',)
    search_fields = ('name', 'address')

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'get_model_year', 'price_per_day', 'available', 'image_count')
    search_fields = ('title', 'model', 'brand__name')
    list_filter = ('brand', 'fuel_type', 'transmission', 'available', 'city', 'model_year')
    ordering = ('-created_at',)
    filter_horizontal = ('pickup_locations',)
    inlines = [BikeImageInline]
    
    def get_model_year(self, obj):
        return obj.model_year.year
    get_model_year.short_description = "Model Year"
    get_model_year.admin_order_field = 'model_year__year'
    
    def image_count(self, obj):
        count = obj.bike_images.count()
        return f"{count} image{'s' if count != 1 else ''}"
    image_count.short_description = "Images"

@admin.register(BikeAvailability)
class BikeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('bike', 'date', 'is_available', 'notes')
    list_filter = ('is_available', 'date')
    search_fields = ('bike__title', 'notes')

@admin.register(BikeReview)
class BikeReviewAdmin(admin.ModelAdmin):
    list_display = ('bike', 'user', 'rating', 'verified_booking', 'helpful_count', 'created_at')
    list_filter = ('rating', 'verified_booking', 'created_at')
    search_fields = ('bike__title', 'user__email', 'review_text')