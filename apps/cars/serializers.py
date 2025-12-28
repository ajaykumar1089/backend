from rest_framework import serializers
from ..models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'  # This will include all fields from the Car model

class CarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'brand', 'fuel_type', 'transmission_type', 'price_per_day', 'available']  # Specify fields for detailed view