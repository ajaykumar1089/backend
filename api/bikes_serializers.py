from rest_framework import serializers
from apps.bikes.models import (
    BikeCity, BikeTransmission, BikeFuelType, BikeBrand, BikeModelYear,
    Bike, BikeImage, BikeAvailability, BikeReview
)

class BikeCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeCity
        fields = '__all__'

class BikeTransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeTransmission
        fields = '__all__'

class BikeFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeFuelType
        fields = '__all__'

class BikeBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeBrand
        fields = '__all__'

class BikeModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeModelYear
        fields = '__all__'

class BikeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeImage
        fields = '__all__'

class BikeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeAvailability
        fields = '__all__'

class BikeReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = BikeReview
        fields = '__all__'

class BikeSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = BikeImageSerializer(many=True, read_only=True, source='bike_images')
    reviews = BikeReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Bike
        fields = '__all__'

class BikeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for bike listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Bike
        fields = [
            'id', 'bike_name', 'brand_name', 'model', 'city_name', 
            'fuel_type_name', 'price_per_hour', 'price_per_day',
            'rating', 'total_trips', 'is_available', 'primary_image'
        ]