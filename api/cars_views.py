from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.cars.models import (
    CarCity, CarTransmission, CarFuelType, CarType, CarBrand, CarModelYear,
    Car, CarImage, CarAvailability, CarReview
)
from .cars_serializers import (
    CarCitySerializer, CarTransmissionSerializer, CarFuelTypeSerializer,
    CarTypeSerializer, CarBrandSerializer, CarModelYearSerializer, 
    CarSerializer, CarListSerializer, CarImageSerializer, 
    CarAvailabilitySerializer, CarReviewSerializer
)

class CarCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarCity.objects.all()
    serializer_class = CarCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class CarTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarTransmission.objects.all()
    serializer_class = CarTransmissionSerializer

class CarFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarFuelType.objects.all()
    serializer_class = CarFuelTypeSerializer

class CarTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarType.objects.all()
    serializer_class = CarTypeSerializer

class CarBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class CarModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModelYear.objects.all()
    serializer_class = CarModelYearSerializer
    ordering = ['-year']

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.select_related(
        'city', 'transmission', 'fuel_type', 'vehicle_type', 'brand', 'model_year', 'service_provider'
    ).prefetch_related('car_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['car_name', 'model', 'brand__name', 'city__name']
    filterset_fields = [
        'city', 'brand', 'fuel_type', 'transmission', 'vehicle_type', 
        'model_year', 'is_available', 'seating_capacity'
    ]
    ordering_fields = ['car_name', 'price_per_hour', 'price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        return CarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(
                Q(price_per_hour__gte=min_price) | Q(price_per_day__gte=min_price)
            )
        if max_price:
            queryset = queryset.filter(
                Q(price_per_hour__lte=max_price) | Q(price_per_day__lte=max_price)
            )
        
        # Filter by availability date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            unavailable_cars = CarAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('car_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_cars)
        
        # Filter by seating capacity
        min_seats = self.request.query_params.get('min_seats')
        max_seats = self.request.query_params.get('max_seats')
        
        if min_seats:
            queryset = queryset.filter(seating_capacity__gte=min_seats)
        if max_seats:
            queryset = queryset.filter(seating_capacity__lte=max_seats)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a car"""
        car = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = CarAvailability.objects.filter(car=car)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = CarAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a car"""
        car = self.get_object()
        reviews = CarReview.objects.filter(car=car).select_related('user')
        serializer = CarReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured cars"""
        featured_cars = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = CarListSerializer(featured_cars, many=True)
        return Response(serializer.data)

class CarAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = CarAvailability.objects.select_related('car')
    serializer_class = CarAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['car', 'date', 'is_available']
    ordering = ['date']

class CarReviewViewSet(viewsets.ModelViewSet):
    queryset = CarReview.objects.select_related('car', 'user')
    serializer_class = CarReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['car', 'rating', 'verified_booking']
    ordering = ['-created_at']