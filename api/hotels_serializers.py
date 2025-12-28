from rest_framework import serializers
from apps.hotels.models import (
    HotelCity, PropertyType, BedPreference, HotelFacility, RoomFacility,
    OutdoorFeature, ReservationType, Hotel, HotelImage, HotelAvailability, HotelReview
)

class HotelCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelCity
        fields = '__all__'

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class BedPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedPreference
        fields = '__all__'

class HotelFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFacility
        fields = '__all__'

class RoomFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFacility
        fields = '__all__'

class OutdoorFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutdoorFeature
        fields = '__all__'

class ReservationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationType
        fields = '__all__'

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'

class HotelAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAvailability
        fields = '__all__'

class HotelReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = HotelReview
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    property_type_name = serializers.CharField(source='property_type.type', read_only=True)
    bed_preference_type = serializers.CharField(source='bed_preference.type', read_only=True)
    reservation_type_name = serializers.CharField(source='reservation_type.type', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    
    facilities = HotelFacilitySerializer(many=True, read_only=True)
    room_facilities = RoomFacilitySerializer(many=True, read_only=True)
    outdoor_features = OutdoorFeatureSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True, source='hotel_images')
    reviews = HotelReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelListSerializer(serializers.ModelSerializer):
    """Simplified serializer for hotel listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    property_type_name = serializers.CharField(source='property_type.type', read_only=True)
    reservation_type_name = serializers.CharField(source='reservation_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'title', 'city_name', 'property_type_name', 'bedrooms', 
            'bathrooms', 'max_guests', 'price_per_day', 'rating', 
            'total_bookings', 'available', 'reservation_type_name', 'primary_image'
        ]