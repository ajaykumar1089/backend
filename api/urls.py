from django.urls import path, include
from rest_framework.routers import DefaultRouter

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('bikes/', include('apps.bikes.urls')),  # Include bikes app URLs
	path('fulltours/', include('apps.fulltours.urls')),  # Include bikes app URLs
	path('holidaypackages/', include('apps.holidaypackages.urls')),  # Include bikes app URLs
	path('tours/', include('apps.tours.urls')),  # Include tours app URLs
    path('accounts/', include('apps.accounts.urls')),  # Include accounts app URLs
    path('auth/', include('rest_framework.urls')),  # Add DRF auth endpoints
]