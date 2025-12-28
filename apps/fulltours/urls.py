from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import ItineraryViewSet, ItineraryImageViewSet, FullTourCityListCreateView, FullTourCityViewSet
from django.conf.urls.static import static
from django.conf import settings

# Create a router and register filter viewsets
filter_router = DefaultRouter()
filter_router.register(r'cities', views.FullTourCityViewSet, basename='fulltour-cities')
# filter_router.register(r'brands', views.FulltourBrandViewSet, basename='fulltour-brands')
# filter_router.register(r'fuel-types', views.FulltourFuelTypeViewSet, basename='fulltour-fuel-types')
# filter_router.register(r'transmissions', views.FulltourTransmissionViewSet, basename='fulltour-transmissions')
filter_router.register(r'itineraries', ItineraryViewSet, basename='itineraries')
filter_router.register(r'itinerary-images', ItineraryImageViewSet, basename='itinerary-images')

urlpatterns = [
	path("cities/", FullTourCityListCreateView.as_view(), name="fulltour-cities"),
	path('api/', include(filter_router.urls)),
    # Main fulltour viewset at root level
    path('', views.FulltourViewSet.as_view({'get': 'list', 'post': 'create'}), name='fulltour-list'),
    path('<int:pk>/', views.FulltourViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='fulltour-detail'),
    
    # Filter endpoints
    path('', include(filter_router.urls)),
    
    # Legacy endpoints (keep for backward compatibility)
    # path('rent/', views.FulltourRentView.as_view(), name='fulltour_rent'),
    path('available/', views.AvailableFulltoursView.as_view(), name='available_fulltours'),
    path('book/', views.BookFulltourView.as_view(), name='book_fulltour'),
    path('details/<int:pk>/', views.FulltourDetailView.as_view(), name='fulltour_detail'),
    path('filters/', views.FulltourFilterView.as_view(), name='fulltour_filters'),
    path('filter-options/', views.FulltourFilterOptionsView.as_view(), name='fulltour_filter_options'),
    path('nearby/', views.NearbyFulltoursView.as_view(), name='nearby_fulltours'),
    # path('model-years/', views.FulltourModelYearViewSet.as_view({'get': 'list'}), name='fulltour_model_years'),
    path('pickup-locations/', views.PickupLocationViewSet.as_view({'get': 'list'}), name='pickup_locations'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)