from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.holidaypackages.models import (
    Itinerary, ItineraryImage, HolidaypackageCity,
    Holidaypackage, HolidaypackageImage, HolidaypackageAvailability, HolidaypackageReview
)
from .Holidaypackages_serializers import (
    ItinerarySerializer, HolidaypackageCitySerializer, HolidaypackageSerializer, HolidaypackageListSerializer,
    HolidaypackageImageSerializer, HolidaypackageAvailabilitySerializer, HolidaypackageReviewSerializer
)

class ItineraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class HolidaypackageCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HolidaypackageCity.objects.all()
    serializer_class = HolidaypackageCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class HolidaypackageViewSet(viewsets.ModelViewSet):
    queryset = Holidaypackage.objects.select_related(
        'city', 'service_provider'
    ).prefetch_related('Holidaypackage_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Holidaypackage_name', 'city__name']
    filterset_fields = [
        'city',
        'is_available', 'price_per_hour','price_per_person', 'price_per_day'
    ]
    ordering_fields = ['Holidaypackage_name', 'price_per_hour', 'price_per_person', 'price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return HolidaypackageListSerializer
        return HolidaypackageSerializer

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
            # Find Holidaypackages that are available for the requested date range
            unavailable_Holidaypackages = HolidaypackageAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('Holidaypackage_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_Holidaypackages)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a Holidaypackage"""
        Holidaypackage = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = HolidaypackageAvailability.objects.filter(Holidaypackage=Holidaypackage)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = HolidaypackageAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a Holidaypackage"""
        Holidaypackage = self.get_object()
        reviews = HolidaypackageReview.objects.filter(Holidaypackage=Holidaypackage).select_related('user')
        serializer = HolidaypackageReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured Holidaypackages"""
        featured_Holidaypackages = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = HolidaypackageListSerializer(featured_Holidaypackages, many=True)
        return Response(serializer.data)

class HolidaypackageAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = HolidaypackageAvailability.objects.select_related('Holidaypackage')
    serializer_class = HolidaypackageAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Holidaypackage', 'date', 'is_available']
    ordering = ['date']

class HolidaypackageReviewViewSet(viewsets.ModelViewSet):
    queryset = HolidaypackageReview.objects.select_related('Holidaypackage', 'user')
    serializer_class = HolidaypackageReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Holidaypackage', 'rating', 'verified_booking']
    ordering = ['-created_at']