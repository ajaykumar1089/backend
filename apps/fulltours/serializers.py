from rest_framework import serializers
from .models import Itinerary, ItineraryImage, FullTourCity, PickupLocation, Fulltour, FulltourImage
# FulltourTransmission, FulltourFuelType, FulltourRentalType,

 # FulltourModelYear


class ItineraryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']


class ItinerarySerializer(serializers.ModelSerializer):
    images = ItineraryImageSerializer(many=True, read_only=True)  # nested images

    class Meta:  # ✅ fixed indentation here
        model = Itinerary
        fields = [
            'id', 'fulltour', 'dayNum', 'name', 'city',
            'district', 'state_province', 'country',
            'description', 'images', 'created_at', 'updated_at'
        ]


class FulltourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FulltourImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'created_at']

# class FulltourBrandSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = FulltourBrand
        # fields = '__all__'

class FullTourCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FullTourCity
        fields = '__all__'

# class FulltourModelYearSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = FulltourModelYear
        # fields = '__all__'

# class FulltourFuelTypeSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = FulltourFuelType
        # fields = '__all__'

# class FulltourTransmissionSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = FulltourTransmission
        # fields = '__all__'

class PickupLocationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = PickupLocation
        fields = ['id', 'name', 'address', 'city', 'city_name', 'latitude', 'longitude']

class FulltourSerializer(serializers.ModelSerializer):
    # brand_name = serializers.CharField(source='brand.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    service_provider_name = serializers.CharField(source='service_provider.username', read_only=True)
    pickup_locations = PickupLocationSerializer(many=True, read_only=True)
    # transmission_type = serializers.CharField(source='transmission.type', read_only=True)
    # fuel_type_name = serializers.CharField(source='fuel_type.type', read_only=True)
    # rental_type_name = serializers.CharField(source='rental_type.type', read_only=True)
    fulltour_images = FulltourImageSerializer(many=True, read_only=True)
    primary_image = serializers.CharField(read_only=True)
    all_images = serializers.ListField(read_only=True)
    #model_year_display = serializers.CharField(source='model_year.year', read_only=True)  # Display the year
    
    class Meta:
        model = Fulltour
        fields = [
            'id', 'service_provider', 'service_provider_name', 'title', 'model', 'description',
             # 'model_year', 'model_year_display', 'transmission', 'transmission_type',
            # 'fuel_type', 'fuel_type_name', 'rental_type', 'rental_type_name',
            # 'engine_capacity', 'mileage',
			'city', 'city_name', 'pickup_locations',
            'price_per_hour', 'price_per_person', 'price_per_day', 'price_per_week', 'price_per_month', 
            'safety_deposit', 'operating_hours', 'available', 'documents_required',
            'terms_and_conditions', 'fulltour_images', 'primary_image', 'all_images', 
            'rating', 'total_reviews', 'total_trips', 'created_at'
        ]
        read_only_fields = ['id', 'service_provider', 'rating', 'total_reviews', 'created_at']

class FulltourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fulltour
        fields = [
            'title',
			# 'model', 
			# 'model_year', 
			# 'transmission', 'fuel_type',
            # 'rental_type', 'engine_capacity', 'mileage', 
			'city', 'price_per_hour', 'price_per_person',
            'price_per_day', 'price_per_week', 'price_per_month', 'safety_deposit',
            'operating_hours', 'documents_required', 'terms_and_conditions',
            'description'
        ]