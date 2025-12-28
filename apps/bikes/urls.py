from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register filter viewsets
filter_router = DefaultRouter()
filter_router.register(r'cities', views.BikeCityViewSet, basename='bike-cities')
filter_router.register(r'brands', views.BikeBrandViewSet, basename='bike-brands')
filter_router.register(r'fuel-types', views.BikeFuelTypeViewSet, basename='bike-fuel-types')
filter_router.register(r'transmissions', views.BikeTransmissionViewSet, basename='bike-transmissions')

urlpatterns = [
    # Main bike viewset at root level
    path('', views.BikeViewSet.as_view({'get': 'list', 'post': 'create'}), name='bike-list'),
    path('<int:pk>/', views.BikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='bike-detail'),
    
    # Filter endpoints
    path('', include(filter_router.urls)),
    
    # Legacy endpoints (keep for backward compatibility)
    path('rent/', views.BikeRentView.as_view(), name='bike_rent'),
    path('available/', views.AvailableBikesView.as_view(), name='available_bikes'),
    path('book/', views.BookBikeView.as_view(), name='book_bike'),
    path('details/<int:pk>/', views.BikeDetailView.as_view(), name='bike_detail'),
    path('filters/', views.BikeFilterView.as_view(), name='bike_filters'),
    path('filter-options/', views.BikeFilterOptionsView.as_view(), name='bike_filter_options'),
    path('nearby/', views.NearbyBikesView.as_view(), name='nearby_bikes'),
    path('model-years/', views.BikeModelYearViewSet.as_view({'get': 'list'}), name='bike_model_years'),
    path('pickup-locations/', views.PickupLocationViewSet.as_view({'get': 'list'}), name='pickup_locations'),
]