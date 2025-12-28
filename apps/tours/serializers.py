from rest_framework import serializers
from apps.tours.models import TourPackage, TourCity


class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = '__all__'


class TourCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCity
        fields = '__all__'
