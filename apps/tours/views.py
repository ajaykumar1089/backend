from rest_framework import viewsets
from apps.tours.models import TourPackage, TourCity
from apps.tours.serializers import TourPackageSerializer, TourCitySerializer


class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.all().order_by('-created_at')
    serializer_class = TourPackageSerializer


class TourCityViewSet(viewsets.ModelViewSet):
    queryset = TourCity.objects.all().order_by('name')
    serializer_class = TourCitySerializer
