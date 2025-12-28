from rest_framework import serializers
from .models import BikeBrand, BikeCity, PickupLocation, Bike, BikeTransmission, BikeFuelType, BikeRentalType, BikeImage, BikeModelYear

class BikeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']

class BikeBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeBrand
        fields = '__all__'

class BikeCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeCity
        fields = '__all__'

class BikeModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeModelYear
        fields = '__all__'

class BikeFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeFuelType
        fields = '__all__'

class BikeTransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeTransmission
        fields = '__all__'

class PickupLocationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = PickupLocation
        fields = ['id', 'name', 'address', 'city', 'city_name', 'latitude', 'longitude']

class BikeSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    pickup_locations = PickupLocationSerializer(many=True, read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    rental_type_name = serializers.CharField(source='rental_type.type', read_only=True)
    bike_images = BikeImageSerializer(many=True, read_only=True)
    primary_image = serializers.CharField(read_only=True)
    all_images = serializers.ListField(read_only=True)
    model_year_display = serializers.CharField(source='model_year.year', read_only=True)  # Display the year
    
    class Meta:
        model = Bike
        fields = [
            'id', 'service_provider', 'service_provider_name', 'title', 'model', 'description',
            'brand', 'brand_name', 'model_year', 'model_year_display', 'transmission', 'transmission_type',
            'fuel_type', 'fuel_type_name', 'rental_type', 'rental_type_name',
            'engine_capacity', 'mileage', 'city', 'city_name', 'pickup_locations',
            'price_per_hour', 'price_per_day', 'price_per_week', 'price_per_month', 
            'safety_deposit', 'operating_hours', 'available', 'documents_required',
            'terms_and_conditions', 'bike_images', 'primary_image', 'all_images', 
            'rating', 'total_reviews', 'total_trips', 'created_at'
        ]
        read_only_fields = ['id', 'service_provider', 'rating', 'total_reviews', 'created_at']

class BikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = [
            'title', 'model', 'brand', 'model_year', 'transmission', 'fuel_type',
            'rental_type', 'engine_capacity', 'mileage', 'city', 'price_per_hour',
            'price_per_day', 'price_per_week', 'price_per_month', 'safety_deposit',
            'operating_hours', 'documents_required', 'terms_and_conditions',
            'description'
        ]