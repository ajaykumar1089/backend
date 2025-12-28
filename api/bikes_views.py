from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.bikes.models import (
    BikeCity, BikeTransmission, BikeFuelType, BikeBrand, BikeModelYear,
    Bike, BikeImage, BikeAvailability, BikeReview
)
from .bikes_serializers import (
    BikeCitySerializer, BikeTransmissionSerializer, BikeFuelTypeSerializer,
    BikeBrandSerializer, BikeModelYearSerializer, BikeSerializer, BikeListSerializer,
    BikeImageSerializer, BikeAvailabilitySerializer, BikeReviewSerializer
)

class BikeCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeCity.objects.all()
    serializer_class = BikeCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class BikeTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeTransmission.objects.all()
    serializer_class = BikeTransmissionSerializer

class BikeFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeFuelType.objects.all()
    serializer_class = BikeFuelTypeSerializer

class BikeBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeBrand.objects.all()
    serializer_class = BikeBrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class BikeModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeModelYear.objects.all()
    serializer_class = BikeModelYearSerializer
    ordering = ['-year']

class BikeViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.select_related(
        'city', 'transmission', 'fuel_type', 'brand', 'model_year', 'service_provider'
    ).prefetch_related('bike_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bike_name', 'model', 'brand__name', 'city__name']
    filterset_fields = [
        'city', 'brand', 'fuel_type', 'transmission', 'model_year',
        'is_available', 'price_per_hour', 'price_per_day'
    ]
    ordering_fields = ['bike_name', 'price_per_hour', 'price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BikeListSerializer
        return BikeSerializer

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
            # Find bikes that are available for the requested date range
            unavailable_bikes = BikeAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('bike_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_bikes)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a bike"""
        bike = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = BikeAvailability.objects.filter(bike=bike)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = BikeAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a bike"""
        bike = self.get_object()
        reviews = BikeReview.objects.filter(bike=bike).select_related('user')
        serializer = BikeReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured bikes"""
        featured_bikes = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = BikeListSerializer(featured_bikes, many=True)
        return Response(serializer.data)

class BikeAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = BikeAvailability.objects.select_related('bike')
    serializer_class = BikeAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['bike', 'date', 'is_available']
    ordering = ['date']

class BikeReviewViewSet(viewsets.ModelViewSet):
    queryset = BikeReview.objects.select_related('bike', 'user')
    serializer_class = BikeReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['bike', 'rating', 'verified_booking']
    ordering = ['-created_at']