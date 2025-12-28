from rest_framework import serializers
from .models import Userstories

class UserstoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userstories
        fields = '__all__'