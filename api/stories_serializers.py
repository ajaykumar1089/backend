from rest_framework import serializers
from apps.Stories.models import (
    UserstoriesCity,
    Userstories, UserstoriesImage, UserstoriesAvailability, UserstoriesReview
)

class UserstoriesCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserstoriesCity
        fields = '__all__'


class UserstoriesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserstoriesImage
        fields = '__all__'

class UserstoriesAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserstoriesAvailability
        fields = '__all__'

class UserstoriesReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserstoriesReview
        fields = '__all__'

class UserstoriesSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #model_year_value = serializers.IntegerField(source='model_year.year', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    images = UserstoriesImageSerializer(many=True, read_only=True, source='fulltour_images')
    reviews = UserstoriesReviewSerializer(many=True, read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Userstories
        fields = '__all__'

class UserstoriesListSerializer(serializers.ModelSerializer):
    """Simplified serializer for fulltour listings"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    #brand_name = serializers.CharField(source='brand.name', read_only=True)
    #fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    primary_image = serializers.URLField(read_only=True)
    
    class Meta:
        model = Userstories
        fields = [
            'id', 'fulltour_name', 'city_name', 
            'price_per_person', 'price_per_hour', 'price_per_day',
            'rating', 'total_trips', 'is_available', 'primary_image'
        ]