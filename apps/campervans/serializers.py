from rest_framework import serializers
from .models import Campervan

class CampervanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campervan
        fields = '__all__'  # You can specify the fields you want to include here if needed.