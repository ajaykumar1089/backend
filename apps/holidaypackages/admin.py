from django.contrib import admin
from .models import Itinerary, ItineraryImage
from .models import (
    HolidayPackageCity,
    # HolidaypackageTransmission,
    # HolidaypackageFuelType,
    # HolidaypackageRentalType,
    # HolidaypackageBrand,
    # HolidaypackageModelYear,
    PickupLocation,
    HolidaypackageImage,
    HolidaypackageAvailability,
    HolidaypackageReview,
    Holidaypackage
)


#------------------itenaries start----------------
class ItineraryImageInline(admin.TabularInline):
    model = ItineraryImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('dayNum', 'name', 'holidaypackage', 'city', 'district', 'state_province', 'country', 'created_at')
    search_fields = ('dayNum','name', 'holidaypackage__title', 'city', 'district', 'state_province', 'country', 'description')
    list_filter = ('city', 'state_province', 'country', 'holidaypackage')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ItineraryImageInline]

	#-----------------------itnaries end------------------------

# ------------------------------
# Inline Admins
# ------------------------------
class HolidaypackageImageInline(admin.TabularInline):
    model = HolidaypackageImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


class HolidaypackageAvailabilityInline(admin.TabularInline):
    model = HolidaypackageAvailability
    extra = 1
    fields = ('date', 'is_available', 'notes', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


class HolidaypackageReviewInline(admin.TabularInline):
    model = HolidaypackageReview
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('user', 'rating', 'review_text', 'verified_booking', 'helpful_count', 'created_at', 'updated_at')


# ------------------------------
# Main Model Admin
# ------------------------------
@admin.register(Holidaypackage)
class HolidaypackageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'city','price_per_person',
        'price_per_day', 'available', 'rating'
    )
    list_filter = (
       
        'available', 'city'
		# 'model_year'
    )
    search_fields = ('title', 'city__name')
    readonly_fields = ('created_at', 'updated_at', 'rating', 'total_reviews', 'total_trips')
    inlines = [HolidaypackageImageInline, HolidaypackageAvailabilityInline, HolidaypackageReviewInline]
    list_per_page = 20
    ordering = ('-created_at',)


# ------------------------------
# Simple Models
# ------------------------------
@admin.register(HolidayPackageCity)
class HolidayPackageCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state', 'country')


# @admin.register(HolidaypackageTransmission)
# class HolidaypackageTransmissionAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(HolidaypackageFuelType)
# class HolidaypackageFuelTypeAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(HolidaypackageRentalType)
# class HolidaypackageRentalTypeAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(HolidaypackageBrand)
# class HolidaypackageBrandAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    # search_fields = ('name',)


# @admin.register(HolidaypackageModelYear)
# class HolidaypackageModelYearAdmin(admin.ModelAdmin):
    # list_display = ('year',)
    # ordering = ('-year',)


@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address', 'city__name')


@admin.register(HolidaypackageImage)
class HolidaypackageImageAdmin(admin.ModelAdmin):
    list_display = ('holidaypackage', 'is_primary', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('holidaypackage__title',)
    readonly_fields = ('created_at',)


@admin.register(HolidaypackageAvailability)
class HolidaypackageAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('holidaypackage', 'date', 'is_available', 'created_at')
    list_filter = ('is_available', 'date')
    search_fields = ('holidaypackage__title',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(HolidaypackageReview)
class HolidaypackageReviewAdmin(admin.ModelAdmin):
    list_display = ('holidaypackage', 'user', 'rating', 'verified_booking', 'created_at')
    list_filter = ('rating', 'verified_booking')
    search_fields = ('user__email', 'holidaypackage__title')
    readonly_fields = ('created_at', 'updated_at')
