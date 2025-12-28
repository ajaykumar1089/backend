from rest_framework import serializers
from apps.fulltours.models import (
    Itinerary, ItineraryImage, FulltourCity,
    Fulltour, FulltourImage, FulltourAvailability, FulltourReview
)
class ItinerarySerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)    
    images = ItineraryImageSerializer(many=True, read_only=True, source='Itinerary_images')    
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Itinerary
          fields = 'id', 'name', 'dayNum', 
		
class FulltourCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FulltourCity
        fields = '__all__'


class FulltourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FulltourImage
        fields = '__all__'

class FulltourAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FulltourAvailability
        fields = '__all__'

class FulltourReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = FulltourReview
        fields = '__all__'

class FulltourSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = FulltourImageSerializer(many=True, read_only=True, source='fulltour_images')
    reviews = FulltourReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Fulltour
        fields = '__all__'

class FulltourListSerializer(serializers.ModelSerializer):
    """Simplified serializer for fulltour listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Fulltour
        fields = [
            'id', 'fulltour_name', 'city_name', 
            'price_per_person', 'price_per_hour', 'price_per_day',
            'rating', 'total_trips', 'is_available', 'primary_image'
        ]