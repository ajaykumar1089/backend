from django.urls import path
from . import views

urlpatterns = [
    path('tours/', views.PilgrimTourListView.as_view(), name='pilgrim_tour_list'),
    path('tours/<int:pk>/', views.PilgrimTourDetailView.as_view(), name='pilgrim_tour_detail'),
    path('hotels/', views.PilgrimHotelListView.as_view(), name='pilgrim_hotel_list'),
    path('hotels/<int:pk>/', views.PilgrimHotelDetailView.as_view(), name='pilgrim_hotel_detail'),
]