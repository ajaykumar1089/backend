from django.shortcuts import render
from rest_framework import viewsets
from .models import PilgrimTour, PilgrimHotel
from .serializers import PilgrimTourSerializer, PilgrimHotelSerializer

class PilgrimTourViewSet(viewsets.ModelViewSet):
    queryset = PilgrimTour.objects.all()
    serializer_class = PilgrimTourSerializer

class PilgrimHotelViewSet(viewsets.ModelViewSet):
    queryset = PilgrimHotel.objects.all()
    serializer_class = PilgrimHotelSerializer