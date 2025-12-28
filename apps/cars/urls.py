from django.urls import path
from . import views

urlpatterns = [
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('cars/create/', views.CarCreateView.as_view(), name='car-create'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car-update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car-delete'),
]