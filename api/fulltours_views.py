from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.fulltours.models import (
    Itinerary, ItineraryImage, FulltourCity,
    Fulltour, FulltourImage, FulltourAvailability, FulltourReview
)
from .Fulltours_serializers import (
    ItinerarySerializer, FulltourCitySerializer, FulltourSerializer, FulltourListSerializer,
    FulltourImageSerializer, FulltourAvailabilitySerializer, FulltourReviewSerializer
)

class ItineraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class FulltourCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FulltourCity.objects.all()
    serializer_class = FulltourCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class FulltourViewSet(viewsets.ModelViewSet):
    queryset = Fulltour.objects.select_related(
        'city', 'service_provider'
    ).prefetch_related('Fulltour_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Fulltour_name', 'city__name']
    filterset_fields = [
        'city',
        'is_available', 'price_per_hour','price_per_person', 'price_per_day'
    ]
    ordering_fields = ['Fulltour_name', 'price_per_hour', 'price_per_person', 'price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return FulltourListSerializer
        return FulltourSerializer

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
            # Find Fulltours that are available for the requested date range
            unavailable_Fulltours = FulltourAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('Fulltour_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_Fulltours)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a Fulltour"""
        Fulltour = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = FulltourAvailability.objects.filter(Fulltour=Fulltour)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = FulltourAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a Fulltour"""
        Fulltour = self.get_object()
        reviews = FulltourReview.objects.filter(Fulltour=Fulltour).select_related('user')
        serializer = FulltourReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured Fulltours"""
        featured_Fulltours = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = FulltourListSerializer(featured_Fulltours, many=True)
        return Response(serializer.data)

class FulltourAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = FulltourAvailability.objects.select_related('Fulltour')
    serializer_class = FulltourAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Fulltour', 'date', 'is_available']
    ordering = ['date']

class FulltourReviewViewSet(viewsets.ModelViewSet):
    queryset = FulltourReview.objects.select_related('Fulltour', 'user')
    serializer_class = FulltourReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['Fulltour', 'rating', 'verified_booking']
    ordering = ['-created_at']