from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.stories.models import (
    UserStoryCity,
    UserStory, UserStoryImage, UserStoryAvailability, UserStoryReview
)
from .UserStories_serializers import (
    UserStoryCitySerializer, UserStorySerializer, UserStoryListSerializer,
    UserStoryImageSerializer, UserStoryAvailabilitySerializer, UserStoryReviewSerializer
)

class UserStoryCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserStoryCity.objects.all()
    serializer_class = UserStoryCitySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'state']
    ordering_fields = ['name']
    ordering = ['name']

class UserStoryViewSet(viewsets.ModelViewSet):
    queryset = UserStory.objects.select_related(
        'city', 'service_provider'
    ).prefetch_related('UserStory_images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['UserStory_name', 'city__name']
    filterset_fields = [
        'city',
        'is_available', 'price_per_hour','price_per_person', 'price_per_day'
    ]
    ordering_fields = ['UserStory_name', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserStoryListSerializer
        return UserStorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
              
        
        # Filter by availability date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            # Find Storys that are available for the requested date range
            unavailable_Storys = StoryAvailability.objects.filter(
                date__range=[start_date, end_date],
                is_available=False
            ).values_list('UserStory_id', flat=True)
            
            queryset = queryset.exclude(id__in=unavailable_UserStories)
        
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get availability calendar for a Story"""
        Story = self.get_object()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        availability_queryset = UserStoryAvailability.objects.filter(UserStory=UserStory)
        
        if start_date:
            availability_queryset = availability_queryset.filter(date__gte=start_date)
        if end_date:
            availability_queryset = availability_queryset.filter(date__lte=end_date)
        
        serializer = UserStoryAvailabilitySerializer(availability_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a Story"""
        UserStory = self.get_object()
        reviews = StoryReview.objects.filter(UserStory=UserStory).select_related('user')
        serializer = UserStoryReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured Storys"""
        featured_Storys = self.get_queryset().filter(
            rating__gte=4.0, total_trips__gte=10, is_available=True
        )[:12]
        serializer = UserStoryListSerializer(featured_Storys, many=True)
        return Response(serializer.data)

class UserStoryAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = UserStoryAvailability.objects.select_related('UserStory')
    serializer_class = UserStoryAvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['UserStory', 'date', 'is_available']
    ordering = ['date']

class UserStoryReviewViewSet(viewsets.ModelViewSet):
    queryset = UserStoryReview.objects.select_related('UserStory', 'user')
    serializer_class = UserStoryReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['UserStory', 'rating', 'verified_booking']
    ordering = ['-created_at']