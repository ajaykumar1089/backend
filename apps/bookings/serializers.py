from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'  # Include all fields from the Booking model

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'service', 'start_date', 'end_date', 'status']  # Specify fields for creating a booking

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'start_date', 'end_date', 'status', 'created_at']  # Specify fields for detailed view