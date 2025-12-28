from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.tours.models import (
    TourCity, TourTransmission, TourFuelType, TourBrand, TourModelYear,
    Tour, TourImage, TourAvailability, TourReview
)
from .Tours_serializers import (
    TourCitySerializer, TourTransmissionSerializer, TourFuelTypeSerializer,
    TourBrandSerializer, TourModelYearSerializer, TourSerializer, TourListSerializer,
    TourImageSerializer, TourAvailabilitySerializer, TourReviewSerializer
)

class TourCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourCity.objects.all()
    serializer_class = TourCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class TourTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourTransmission.objects.all()
    serializer_class = TourTransmissionSerializer

class TourFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourFuelType.objects.all()
    serializer_class = TourFuelTypeSerializer

class TourBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourBrand.objects.all()
    serializer_class = TourBrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class TourModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourModelYear.objects.all()
    serializer_class = TourModelYearSerializer
    ordering = ['-year']

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.select_related(
        'city', 'transmission', 'fuel_type', 'brand', 'model_year', 'service_provider'
    ).prefetch_related('Tour_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Tour_name', 'model', 'brand__name', 'city__name']
    filterset_fields = [
        'city', 'brand', 'fuel_type', 'transmission', 'model_year',
        'is_available', 'price_per_hour', 'price_per_day'
    ]
    ordering_fields = ['Tour_name', 'price_per_hour', 'price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return TourSerializer

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
            # Find Tours that are available for the requested date range
            unavailable_Tours = TourAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('Tour_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_Tours)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a Tour"""
        Tour = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = TourAvailability.objects.filter(Tour=Tour)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = TourAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a Tour"""
        Tour = self.get_object()
        reviews = TourReview.objects.filter(Tour=Tour).select_related('user')
        serializer = TourReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured Tours"""
        featured_Tours = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = TourListSerializer(featured_Tours, many=True)
        return Response(serializer.data)

class TourAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TourAvailability.objects.select_related('Tour')
    serializer_class = TourAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Tour', 'date', 'is_available']
    ordering = ['date']

class TourReviewViewSet(viewsets.ModelViewSet):
    queryset = TourReview.objects.select_related('Tour', 'user')
    serializer_class = TourReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Tour', 'rating', 'verified_booking']
    ordering = ['-created_at']