from rest_framework import viewsets
from .models import Campervan
from .serializers import CampervanSerializer

class CampervanViewSet(viewsets.ModelViewSet):
    queryset = Campervan.objects.all()
    serializer_class = CampervanSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()