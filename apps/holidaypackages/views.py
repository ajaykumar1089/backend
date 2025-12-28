from rest_framework import generics, viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Holidaypackage, HolidayPackageCity, PickupLocation, Itinerary, ItineraryImage
 # HolidaypackageFuelType, HolidaypackageTransmission, HolidaypackageModelYear,  
from .serializers import ItinerarySerializer, ItineraryImageSerializer, HolidaypackageSerializer, HolidaypackageCreateSerializer, HolidayPackageCitySerializer, PickupLocationSerializer
# HolidaypackageFuelTypeSerializer, HolidaypackageTransmissionSerializer, HolidaypackageModelYearSerializer, 
from .location_utils import haversine_distance

class ItineraryViewSet(viewsets.ModelViewSet):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'holidaypackage']
    search_fields = ['name', 'description', 'city']
    ordering_fields = ['created_at', 'id']
    ordering = ['id']

    def get_queryset(self):
        queryset = Itinerary.objects.all().order_by('id')

        # ✅ Filter by ?holidaypackage=10
        holidaypackage_id = self.request.query_params.get('holidaypackage')
        if holidaypackage_id:
            queryset = queryset.filter(holidaypackage=holidaypackage_id)

        # ✅ Filter by ?holidaypackage__in=1,3,5 (optional)
        holidaypackage_in = self.request.query_params.get('holidaypackage__in')
        if holidaypackage_in:
            ids = [int(x) for x in holidaypackage_in.split(',') if x.isdigit()]
            queryset = queryset.filter(holidaypackage__in=ids)

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

class HolidaypackageViewSet(viewsets.ModelViewSet):
    queryset = Holidaypackage.objects.all()
    serializer_class = HolidaypackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [ 'city', 'available']
    search_fields = ['title', 'model', 'description', 'city__name']
    ordering_fields = ['price_per_person', 'price_per_day', 'rating', 'created_at']		
    ordering = ['-created_at']

# class HolidaypackageRentView(generics.ListAPIView):
    # serializer_class = HolidaypackageSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    # def get_queryset(self):
        # return Holidaypackage.objects.filter(available=True)

class AvailableHolidaypackagesView(generics.ListAPIView):
    serializer_class = HolidaypackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city']
    search_fields = ['title', 'model', 'description']
    
    def get_queryset(self):
        queryset = Holidaypackage.objects.filter(available=True)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)	
            
        return queryset.order_by('-rating')

class BookHolidaypackageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # This would integrate with the bookings app
        # For now, just return success response
        return Response({"message": "Booking request submitted"}, status=status.HTTP_201_CREATED)

class HolidaypackageDetailView(generics.RetrieveAPIView):
    queryset = Holidaypackage.objects.all()
    serializer_class = HolidaypackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class HolidaypackageFilterView(generics.ListAPIView):
    serializer_class = HolidaypackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Holidaypackage.objects.filter(available=True)
        
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

class HolidaypackageFilterOptionsView(generics.GenericAPIView):
    """View to provide filter options for the frontend"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        # Import related models
        from .models import HolidaypackageTransmission, HolidaypackageFuelType, HolidaypackageRentalType
        
        # Get all unique filter options from the database
        # brands = list(HolidaypackageBrand.objects.values_list('name', flat=True).distinct())
        cities = list(HolidayPackageCity.objects.values_list('name', flat=True).distinct())
        #model_years = list(HolidaypackageModelYear.objects.values_list('year', flat=True).order_by('-year'))
        # transmissions = list(HolidaypackageTransmission.objects.values_list('type', flat=True).distinct())
        # fuel_types = list(HolidaypackageFuelType.objects.values_list('type', flat=True).distinct())
        # rental_types = list(HolidaypackageRentalType.objects.values_list('type', flat=True).distinct())
        
        return Response({
            # 'brands': brands,
            'cities': cities,
            # 'model_years': model_years,
            # 'transmissions': transmissions,
            # 'fuel_types': fuel_types,
            # 'rental_types': rental_types,
        })

class NearbyHolidaypackagesView(generics.ListAPIView):
    """View to get holidaypackages near a specific location, sorted by distance"""
    serializer_class = HolidaypackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = Holidaypackage.objects.filter(available=True)
        
        # Get user coordinates from query parameters
        user_lat = self.request.query_params.get('lat')
        user_lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)  # Default 10km radius
        
        if not user_lat or not user_lng:
            # Return all holidaypackages if no coordinates provided
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            radius = float(radius)
        except ValueError:
            # Return all holidaypackages if invalid coordinates
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        # Calculate distances for all holidaypackages and filter by radius
        holidaypackages_with_distance = []
        
        for holidaypackage in queryset:
            closest_distance = float('inf')
            closest_pickup_location = None
            
            # Find the closest pickup location for each holidaypackage
            for pickup_location in holidaypackage.pickup_locations.all():
                if pickup_location.latitude and pickup_location.longitude:
                    distance = haversine_distance(
                        user_lat, user_lng,
                        float(pickup_location.latitude),
                        float(pickup_location.longitude)
                    )
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_pickup_location = pickup_location
            
            # Add holidaypackage to results if within radius
            if closest_distance <= radius and closest_pickup_location:
                holidaypackages_with_distance.append({
                    'holidaypackage': holidaypackage,
                    'distance': round(closest_distance, 2),
                    'closest_pickup': closest_pickup_location
                })
        
        # Sort by distance (ascending - nearest first)
        holidaypackages_with_distance.sort(key=lambda x: x['distance'])
        
        # Serialize holidaypackages and add distance information
        result_data = []
        for item in holidaypackages_with_distance:
            holidaypackage_data = self.get_serializer(item['holidaypackage']).data
            holidaypackage_data['distance_km'] = item['distance']
            holidaypackage_data['closest_pickup_location'] = {
                'id': item['closest_pickup'].id,
                'name': item['closest_pickup'].name,
                'address': item['closest_pickup'].address,
                'latitude': str(item['closest_pickup'].latitude),
                'longitude': str(item['closest_pickup'].longitude),
            }
            result_data.append(holidaypackage_data)
        
        return Response(result_data)

# class HolidaypackageModelYearViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = HolidaypackageModelYear.objects.all()
    # serializer_class = HolidaypackageModelYearSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class PickupLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupLocation.objects.all()
    serializer_class = PickupLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']  # Allow filtering by city

class HolidayPackageCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HolidayPackageCity.objects.all()
    serializer_class = HolidayPackageCitySerializer
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
	
class HolidayPackageCityListCreateView(generics.ListCreateAPIView):
    queryset = HolidayPackageCity.objects.all().order_by('-created_at')
    serializer_class = HolidayPackageCitySerializer

# class HolidaypackageBrandViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = HolidaypackageBrand.objects.all()
    # # serializer_class = HolidaypackageBrandSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

# class HolidaypackageFuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = HolidaypackageFuelType.objects.all()
    # serializer_class = HolidaypackageFuelTypeSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

# class HolidaypackageTransmissionViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = HolidaypackageTransmission.objects.all()
    # serializer_class = HolidaypackageTransmissionSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]