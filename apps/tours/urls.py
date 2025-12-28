from rest_framework.routers import DefaultRouter
from apps.tours import views

router = DefaultRouter()
router.register(r'packages', views.TourPackageViewSet, basename='tour-packages')
router.register(r'cities', views.TourCityViewSet, basename='tour-cities')

urlpatterns = router.urls
