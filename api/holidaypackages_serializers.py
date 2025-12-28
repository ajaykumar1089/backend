from rest_framework import serializers
from apps.holidaypackages.models import (
    Itinerary, ItineraryImage, HolidaypackageCity,
    Holidaypackage, HolidaypackageImage, HolidaypackageAvailability, HolidaypackageReview
)
class ItinerarySerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)    
    images = ItineraryImageSerializer(many=True, read_only=True, source='Itinerary_images')    
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Itinerary
          fields = 'id', 'name', 'dayNum', 
		
class HolidaypackageCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidaypackageCity
        fields = '__all__'


class HolidaypackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidaypackageImage
        fields = '__all__'

class HolidaypackageAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidaypackageAvailability
        fields = '__all__'

class HolidaypackageReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = HolidaypackageReview
        fields = '__all__'

class HolidaypackageSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = HolidaypackageImageSerializer(many=True, read_only=True, source='holidaypackage_images')
    reviews = HolidaypackageReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Holidaypackage
        fields = '__all__'

class HolidaypackageListSerializer(serializers.ModelSerializer):
    """Simplified serializer for holidaypackage listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Holidaypackage
        fields = [
            'id', 'holidaypackage_name', 'city_name', 
            'price_per_person', 'price_per_hour', 'price_per_day',
            'rating', 'total_trips', 'is_available', 'primary_image'
        ]