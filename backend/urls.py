from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bikes/', include('apps.bikes.urls')),  # Direct bikes app URLs
	path('api/fulltours/', include('apps.fulltours.urls')),  # Direct full tours app 
	path('api/holidaypackages/', include('apps.holidaypackages.urls')),  # Direct full tours app 
	path('api/stories/', include('apps.stories.urls')),  # Direct stories app URLs
	path('api/tours/', include('apps.tours.urls')),  # Direct tours app URLs
    path('api/accounts/', include('apps.accounts.urls')),  # Direct accounts app URLs
	path('ckeditor/', include('ckeditor_uploader.urls')),
    # your other URLs

    # path('api/cars/', include('apps.cars.urls')),
    # path('api/campervans/', include('apps.campervans.urls')),
    # path('api/hotels/', include('apps.hotels.urls')),
    # path('api/guided-trips/', include('apps.guided_trips.urls')),
    # path('api/pilgrim/', include('apps.pilgrim.urls')),
    # path('api/stories/', include('apps.stories.urls')),
    # path('api/bookings/', include('apps.bookings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)