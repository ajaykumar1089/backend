from django.contrib import admin
from .models import Itinerary, ItineraryImage
from .models import (
    FullTourCity,
    # FulltourTransmission,
    # FulltourFuelType,
    # FulltourRentalType,
    # FulltourBrand,
    # FulltourModelYear,
    PickupLocation,
    FulltourImage,
    FulltourAvailability,
    FulltourReview,
    Fulltour
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
    list_display = ('dayNum', 'name', 'fulltour', 'city', 'district', 'state_province', 'country', 'created_at')
    search_fields = ('dayNum','name', 'fulltour__title', 'city', 'district', 'state_province', 'country', 'description')
    list_filter = ('city', 'state_province', 'country', 'fulltour')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ItineraryImageInline]

	#-----------------------itnaries end------------------------

# ------------------------------
# Inline Admins
# ------------------------------
class FulltourImageInline(admin.TabularInline):
    model = FulltourImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


class FulltourAvailabilityInline(admin.TabularInline):
    model = FulltourAvailability
    extra = 1
    fields = ('date', 'is_available', 'notes', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


class FulltourReviewInline(admin.TabularInline):
    model = FulltourReview
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('user', 'rating', 'review_text', 'verified_booking', 'helpful_count', 'created_at', 'updated_at')


# ------------------------------
# Main Model Admin
# ------------------------------
@admin.register(Fulltour)
class FulltourAdmin(admin.ModelAdmin):
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
    inlines = [FulltourImageInline, FulltourAvailabilityInline, FulltourReviewInline]
    list_per_page = 20
    ordering = ('-created_at',)


# ------------------------------
# Simple Models
# ------------------------------
@admin.register(FullTourCity)
class FullTourCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'country')
    search_fields = ('name', 'state', 'country')


# @admin.register(FulltourTransmission)
# class FulltourTransmissionAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(FulltourFuelType)
# class FulltourFuelTypeAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(FulltourRentalType)
# class FulltourRentalTypeAdmin(admin.ModelAdmin):
    # list_display = ('type',)
    # search_fields = ('type',)


# @admin.register(FulltourBrand)
# class FulltourBrandAdmin(admin.ModelAdmin):
    # list_display = ('name',)
    # search_fields = ('name',)


# @admin.register(FulltourModelYear)
# class FulltourModelYearAdmin(admin.ModelAdmin):
    # list_display = ('year',)
    # ordering = ('-year',)


@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address', 'city__name')


@admin.register(FulltourImage)
class FulltourImageAdmin(admin.ModelAdmin):
    list_display = ('fulltour', 'is_primary', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('fulltour__title',)
    readonly_fields = ('created_at',)


@admin.register(FulltourAvailability)
class FulltourAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('fulltour', 'date', 'is_available', 'created_at')
    list_filter = ('is_available', 'date')
    search_fields = ('fulltour__title',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FulltourReview)
class FulltourReviewAdmin(admin.ModelAdmin):
    list_display = ('fulltour', 'user', 'rating', 'verified_booking', 'created_at')
    list_filter = ('rating', 'verified_booking')
    search_fields = ('user__email', 'fulltour__title')
    readonly_fields = ('created_at', 'updated_at')
