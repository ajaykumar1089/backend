from django.contrib import admin
from .models import Booking, BookingPayment, BookingReview

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'service_type', 'status', 'payment_status', 'total_cost', 'start_date', 'end_date', 'service_provider')
    search_fields = ('booking_reference', 'user__email', 'contact_name', 'contact_email')
    list_filter = ('service_type', 'status', 'payment_status', 'created_at', 'start_date')
    readonly_fields = ('booking_reference', 'booking_date', 'created_at', 'updated_at')
    date_hierarchy = 'start_date'

@admin.register(BookingPayment)
class BookingPaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'payment_method', 'amount', 'transaction_id', 'status', 'created_at')
    search_fields = ('transaction_id', 'booking__booking_reference')
    list_filter = ('payment_method', 'status', 'created_at')
    readonly_fields = ('created_at', 'processed_at')

@admin.register(BookingReview)
class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'rating', 'would_recommend', 'created_at')
    search_fields = ('booking__booking_reference', 'user__email', 'review_text')
    list_filter = ('rating', 'would_recommend', 'created_at')
    readonly_fields = ('created_at',)