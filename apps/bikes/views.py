from rest_framework import generics, viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Bike, BikeBrand, BikeCity, BikeFuelType, BikeTransmission, BikeModelYear, PickupLocation
from .serializers import BikeSerializer, BikeCreateSerializer, BikeBrandSerializer, BikeCitySerializer, BikeFuelTypeSerializer, BikeTransmissionSerializer, BikeModelYearSerializer, PickupLocationSerializer
from .location_utils import haversine_distance

class BikeViewSet(viewsets.ModelViewSet):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'city', 'transmission', 'fuel_type', 'model_year', 'available']
    search_fields = ['title', 'model', 'description', 'brand__name', 'city__name']
    ordering_fields = ['price_per_day', 'rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(service_provider=self.request.user)

class BikeRentView(generics.ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Bike.objects.filter(available=True)

class AvailableBikesView(generics.ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'city', 'transmission', 'fuel_type']
    search_fields = ['title', 'model', 'description']
    
    def get_queryset(self):
        queryset = Bike.objects.filter(available=True)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)
            
        return queryset.order_by('-rating')

class BookBikeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # This would integrate with the bookings app
        # For now, just return success response
        return Response({"message": "Booking request submitted"}, status=status.HTTP_201_CREATED)

class BikeDetailView(generics.RetrieveAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BikeFilterView(generics.ListAPIView):
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Bike.objects.filter(available=True)
        
        # Complex filtering logic as per business requirements
        brand_filters = self.request.query_params.getlist('brands[]')
        city_filters = self.request.query_params.getlist('cities[]')
        transmission_filters = self.request.query_params.getlist('transmissions[]')
        
        if brand_filters:
            queryset = queryset.filter(brand__name__in=brand_filters)
        if city_filters:
            queryset = queryset.filter(city__name__in=city_filters)
        if transmission_filters:
            queryset = queryset.filter(transmission__type__in=transmission_filters)
            
        return queryset.order_by('-rating')

class BikeFilterOptionsView(generics.GenericAPIView):
    """View to provide filter options for the frontend"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        # Import related models
        from .models import BikeTransmission, BikeFuelType, BikeRentalType
        
        # Get all unique filter options from the database
        brands = list(BikeBrand.objects.values_list('name', flat=True).distinct())
        cities = list(BikeCity.objects.values_list('name', flat=True).distinct())
        model_years = list(BikeModelYear.objects.values_list('year', flat=True).order_by('-year'))
        transmissions = list(BikeTransmission.objects.values_list('type', flat=True).distinct())
        fuel_types = list(BikeFuelType.objects.values_list('type', flat=True).distinct())
        rental_types = list(BikeRentalType.objects.values_list('type', flat=True).distinct())
        
        return Response({
            'brands': brands,
            'cities': cities,
            'model_years': model_years,
            'transmissions': transmissions,
            'fuel_types': fuel_types,
            'rental_types': rental_types,
        })

class NearbyBikesView(generics.ListAPIView):
    """View to get bikes near a specific location, sorted by distance"""
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = Bike.objects.filter(available=True)
        
        # Get user coordinates from query parameters
        user_lat = self.request.query_params.get('lat')
        user_lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)  # Default 10km radius
        
        if not user_lat or not user_lng:
            # Return all bikes if no coordinates provided
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            radius = float(radius)
        except ValueError:
            # Return all bikes if invalid coordinates
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        # Calculate distances for all bikes and filter by radius
        bikes_with_distance = []
        
        for bike in queryset:
            closest_distance = float('inf')
            closest_pickup_location = None
            
            # Find the closest pickup location for each bike
            for pickup_location in bike.pickup_locations.all():
                if pickup_location.latitude and pickup_location.longitude:
                    distance = haversine_distance(
                        user_lat, user_lng,
                        float(pickup_location.latitude),
                        float(pickup_location.longitude)
                    )
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_pickup_location = pickup_location
            
            # Add bike to results if within radius
            if closest_distance <= radius and closest_pickup_location:
                bikes_with_distance.append({
                    'bike': bike,
                    'distance': round(closest_distance, 2),
                    'closest_pickup': closest_pickup_location
                })
        
        # Sort by distance (ascending - nearest first)
        bikes_with_distance.sort(key=lambda x: x['distance'])
        
        # Serialize bikes and add distance information
        result_data = []
        for item in bikes_with_distance:
            bike_data = self.get_serializer(item['bike']).data
            bike_data['distance_km'] = item['distance']
            bike_data['closest_pickup_location'] = {
                'id': item['closest_pickup'].id,
                'name': item['closest_pickup'].name,
                'address': item['closest_pickup'].address,
                'latitude': str(item['closest_pickup'].latitude),
                'longitude': str(item['closest_pickup'].longitude),
            }
            result_data.append(bike_data)
        
        return Response(result_data)

class BikeModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeModelYear.objects.all()
    serializer_class = BikeModelYearSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PickupLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']  # Allow filtering by city

class BikeCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeCity.objects.all()
    serializer_class = BikeCitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BikeBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeBrand.objects.all()
    serializer_class = BikeBrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BikeFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeFuelType.objects.all()
    serializer_class = BikeFuelTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BikeTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BikeTransmission.objects.all()
    serializer_class = BikeTransmissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]