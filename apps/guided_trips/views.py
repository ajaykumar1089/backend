from rest_framework import viewsets
from .models import GuidedTrip
from .serializers import GuidedTripSerializer

class GuidedTripViewSet(viewsets.ModelViewSet):
    queryset = GuidedTrip.objects.all()
    serializer_class = GuidedTripSerializer

    def perform_create(self, serializer):
        serializer.save()  # You can add custom logic here if needed

    def perform_update(self, serializer):
        serializer.save()  # You can add custom logic here if needed

    def perform_destroy(self, instance):
        instance.delete()  # You can add custom logic here if needed