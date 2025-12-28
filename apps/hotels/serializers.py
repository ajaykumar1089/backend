from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'  # Include all fields from the Hotel model

class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'price', 'description', 'amenities', 'availability']  # Specify fields for creation

class HotelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['price', 'description', 'amenities', 'availability']  # Specify fields for updates