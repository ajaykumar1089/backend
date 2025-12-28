from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import ItineraryViewSet, ItineraryImageViewSet, HolidayPackageCityListCreateView, HolidayPackageCityViewSet
from django.conf.urls.static import static
from django.conf import settings

# Create a router and register filter viewsets
filter_router = DefaultRouter()
filter_router.register(r'cities', views.HolidayPackageCityViewSet, basename='holidaypackage-cities')
# filter_router.register(r'brands', views.HolidaypackageBrandViewSet, basename='holidaypackage-brands')
# filter_router.register(r'fuel-types', views.HolidaypackageFuelTypeViewSet, basename='holidaypackage-fuel-types')
# filter_router.register(r'transmissions', views.HolidaypackageTransmissionViewSet, basename='holidaypackage-transmissions')
filter_router.register(r'itineraries', ItineraryViewSet, basename='itineraries')
filter_router.register(r'itinerary-images', ItineraryImageViewSet, basename='itinerary-images')

urlpatterns = [
	path("cities/", HolidayPackageCityListCreateView.as_view(), name="holidaypackage-cities"),
	path('api/', include(filter_router.urls)),
    # Main holidaypackage viewset at root level
    path('', views.HolidaypackageViewSet.as_view({'get': 'list', 'post': 'create'}), name='holidaypackage-list'),
    path('<int:pk>/', views.HolidaypackageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='holidaypackage-detail'),
    
    # Filter endpoints
    path('', include(filter_router.urls)),
    
    # Legacy endpoints (keep for backward compatibility)
    # path('rent/', views.HolidaypackageRentView.as_view(), name='holidaypackage_rent'),
    path('available/', views.AvailableHolidaypackagesView.as_view(), name='available_holidaypackages'),
    path('book/', views.BookHolidaypackageView.as_view(), name='book_holidaypackage'),
    path('details/<int:pk>/', views.HolidaypackageDetailView.as_view(), name='holidaypackage_detail'),
    path('filters/', views.HolidaypackageFilterView.as_view(), name='holidaypackage_filters'),
    path('filter-options/', views.HolidaypackageFilterOptionsView.as_view(), name='holidaypackage_filter_options'),
    path('nearby/', views.NearbyHolidaypackagesView.as_view(), name='nearby_holidaypackages'),
    # path('model-years/', views.HolidaypackageModelYearViewSet.as_view({'get': 'list'}), name='holidaypackage_model_years'),
    path('pickup-locations/', views.PickupLocationViewSet.as_view({'get': 'list'}), name='pickup_locations'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)