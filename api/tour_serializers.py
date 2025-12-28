from rest_framework import serializers
from apps.Tours.models import (
    TourCity, TourTransmission, TourFuelType, TourBrand, TourModelYear,
    Tour, TourImage, TourAvailability, TourReview
)

class TourCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCity
        fields = '__all__'

class TourTransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourTransmission
        fields = '__all__'

class TourFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourFuelType
        fields = '__all__'

class TourBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBrand
        fields = '__all__'

class TourModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourModelYear
        fields = '__all__'

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = '__all__'

class TourAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAvailability
        fields = '__all__'

class TourReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TourReview
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = TourImageSerializer(many=True, read_only=True, source='Tour_images')
    reviews = TourReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Tour
        fields = '__all__'

class TourListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Tour listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Tour
        fields = [
            'id', 'Tour_name', 'brand_name', 'model', 'city_name', 
            'fuel_type_name', 'price_per_hour', 'price_per_day',
            'rating', 'total_trips', 'is_available', 'primary_image'
        ]