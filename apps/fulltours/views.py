from rest_framework import generics, viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Fulltour, FullTourCity, PickupLocation, Itinerary, ItineraryImage
 # FulltourFuelType, FulltourTransmission, FulltourModelYear,  
from .serializers import ItinerarySerializer, ItineraryImageSerializer, FulltourSerializer, FulltourCreateSerializer, FullTourCitySerializer, PickupLocationSerializer
# FulltourFuelTypeSerializer, FulltourTransmissionSerializer, FulltourModelYearSerializer, 
from .location_utils import haversine_distance

class ItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'fulltour']
    search_fields = ['name', 'description', 'city']
    ordering_fields = ['created_at', 'id']
    ordering = ['id']

    def get_queryset(self):
        queryset = Itinerary.objects.all().order_by('id')

        # ✅ Filter by ?fulltour=10
        fulltour_id = self.request.query_params.get('fulltour')
        if fulltour_id:
            queryset = queryset.filter(fulltour=fulltour_id)

        # ✅ Filter by ?fulltour__in=1,3,5 (optional)
        fulltour_in = self.request.query_params.get('fulltour__in')
        if fulltour_in:
            ids = [int(x) for x in fulltour_in.split(',') if x.isdigit()]
            queryset = queryset.filter(fulltour__in=ids)

        return queryset

    
class ItineraryImageViewSet(viewsets.ModelViewSet):
    queryset = ItineraryImage.objects.all().order_by('-created_at')
    serializer_class = ItineraryImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['itinerary']
    search_fields = ['alt_text']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class FulltourViewSet(viewsets.ModelViewSet):
    queryset = Fulltour.objects.all()
    serializer_class = FulltourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [ 'city', 'available']
    search_fields = ['title', 'model', 'description', 'city__name']
    ordering_fields = ['price_per_person', 'price_per_day', 'rating', 'created_at']		
    ordering = ['-created_at']

# class FulltourRentView(generics.ListAPIView):
    # serializer_class = FulltourSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    # def get_queryset(self):
        # return Fulltour.objects.filter(available=True)

class AvailableFulltoursView(generics.ListAPIView):
    serializer_class = FulltourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city']
    search_fields = ['title', 'model', 'description']
    
    def get_queryset(self):
        queryset = Fulltour.objects.filter(available=True)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)	
            
        return queryset.order_by('-rating')

class BookFulltourView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # This would integrate with the bookings app
        # For now, just return success response
        return Response({"message": "Booking request submitted"}, status=status.HTTP_201_CREATED)

class FulltourDetailView(generics.RetrieveAPIView):
    queryset = Fulltour.objects.all()
    serializer_class = FulltourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FulltourFilterView(generics.ListAPIView):
    serializer_class = FulltourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Fulltour.objects.filter(available=True)
        
        # Complex filtering logic as per business requirements
        # brand_filters = self.request.query_params.getlist('brands[]')
        city_filters = self.request.query_params.getlist('cities[]')
        # transmission_filters = self.request.query_params.getlist('transmissions[]')
        
        # if brand_filters:
            # queryset = queryset.filter(brand__name__in=brand_filters)
        if city_filters:
            queryset = queryset.filter(city__name__in=city_filters)
        # if transmission_filters:
            # queryset = queryset.filter(transmission__type__in=transmission_filters)
            
        return queryset.order_by('-rating')

class FulltourFilterOptionsView(generics.GenericAPIView):
    """View to provide filter options for the frontend"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        # Import related models
        from .models import FulltourTransmission, FulltourFuelType, FulltourRentalType
        
        # Get all unique filter options from the database
        # brands = list(FulltourBrand.objects.values_list('name', flat=True).distinct())
        cities = list(FullTourCity.objects.values_list('name', flat=True).distinct())
        #model_years = list(FulltourModelYear.objects.values_list('year', flat=True).order_by('-year'))
        # transmissions = list(FulltourTransmission.objects.values_list('type', flat=True).distinct())
        # fuel_types = list(FulltourFuelType.objects.values_list('type', flat=True).distinct())
        # rental_types = list(FulltourRentalType.objects.values_list('type', flat=True).distinct())
        
        return Response({
            # 'brands': brands,
            'cities': cities,
            # 'model_years': model_years,
            # 'transmissions': transmissions,
            # 'fuel_types': fuel_types,
            # 'rental_types': rental_types,
        })

class NearbyFulltoursView(generics.ListAPIView):
    """View to get fulltours near a specific location, sorted by distance"""
    serializer_class = FulltourSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = Fulltour.objects.filter(available=True)
        
        # Get user coordinates from query parameters
        user_lat = self.request.query_params.get('lat')
        user_lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)  # Default 10km radius
        
        if not user_lat or not user_lng:
            # Return all fulltours if no coordinates provided
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            radius = float(radius)
        except ValueError:
            # Return all fulltours if invalid coordinates
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        # Calculate distances for all fulltours and filter by radius
        fulltours_with_distance = []
        
        for fulltour in queryset:
            closest_distance = float('inf')
            closest_pickup_location = None
            
            # Find the closest pickup location for each fulltour
            for pickup_location in fulltour.pickup_locations.all():
                if pickup_location.latitude and pickup_location.longitude:
                    distance = haversine_distance(
                        user_lat, user_lng,
                        float(pickup_location.latitude),
                        float(pickup_location.longitude)
                    )
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_pickup_location = pickup_location
            
            # Add fulltour to results if within radius
            if closest_distance <= radius and closest_pickup_location:
                fulltours_with_distance.append({
                    'fulltour': fulltour,
                    'distance': round(closest_distance, 2),
                    'closest_pickup': closest_pickup_location
                })
        
        # Sort by distance (ascending - nearest first)
        fulltours_with_distance.sort(key=lambda x: x['distance'])
        
        # Serialize fulltours and add distance information
        result_data = []
        for item in fulltours_with_distance:
            fulltour_data = self.get_serializer(item['fulltour']).data
            fulltour_data['distance_km'] = item['distance']
            fulltour_data['closest_pickup_location'] = {
                'id': item['closest_pickup'].id,
                'name': item['closest_pickup'].name,
                'address': item['closest_pickup'].address,
                'latitude': str(item['closest_pickup'].latitude),
                'longitude': str(item['closest_pickup'].longitude),
            }
            result_data.append(fulltour_data)
        
        return Response(result_data)

# class FulltourModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = FulltourModelYear.objects.all()
    # serializer_class = FulltourModelYearSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class PickupLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']  # Allow filtering by city

class FullTourCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FullTourCity.objects.all()
    serializer_class = FullTourCitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ✅ Add autocomplete endpoint
    @action(detail=False, methods=['get'], url_path='autocomplete')
    def autocomplete(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([], status=200)
        
        cities = self.queryset.filter(name__icontains=query)[:10]
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)
	
class FullTourCityListCreateView(generics.ListCreateAPIView):
    queryset = FullTourCity.objects.all().order_by('-created_at')
    serializer_class = FullTourCitySerializer

# class FulltourBrandViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = FulltourBrand.objects.all()
    # # serializer_class = FulltourBrandSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

# class FulltourFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = FulltourFuelType.objects.all()
    # serializer_class = FulltourFuelTypeSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

# class FulltourTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = FulltourTransmission.objects.all()
    # serializer_class = FulltourTransmissionSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]