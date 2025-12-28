from rest_framework import serializers
from apps.cars.models import (
    CarCity, CarTransmission, CarFuelType, CarType, CarBrand, CarModelYear,
    Car, CarImage, CarAvailability, CarReview
)

class CarCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCity
        fields = '__all__'

class CarTransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarTransmission
        fields = '__all__'

class CarFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFuelType
        fields = '__all__'

class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'

class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = '__all__'

class CarModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelYear
        fields = '__all__'

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'

class CarAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAvailability
        fields = '__all__'

class CarReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CarReview
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    vehicle_type_name = serializers.CharField(source='vehicle_type.type', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = CarImageSerializer(many=True, read_only=True, source='car_images')
    reviews = CarReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Car
        fields = '__all__'

class CarListSerializer(serializers.ModelSerializer):
    """Simplified serializer for car listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    vehicle_type_name = serializers.CharField(source='vehicle_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Car
        fields = [
            'id', 'car_name', 'brand_name', 'model', 'city_name', 
            'fuel_type_name', 'vehicle_type_name', 'seating_capacity',
            'price_per_hour', 'price_per_day', 'rating', 'total_trips', 
            'is_available', 'primary_image'
        ]