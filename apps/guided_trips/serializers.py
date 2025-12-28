from rest_framework import serializers
from .models import GuidedTrip

class GuidedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidedTrip
        fields = '__all__'  # You can specify the fields you want to include here if needed.