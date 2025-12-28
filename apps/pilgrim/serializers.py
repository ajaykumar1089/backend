from rest_framework import serializers
from .models import PilgrimTour, PilgrimHotel

class PilgrimTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = PilgrimTour
        fields = '__all__'

class PilgrimHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PilgrimHotel
        fields = '__all__'