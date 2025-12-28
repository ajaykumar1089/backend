from django.urls import path
from . import views

urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel-list'),
    path('<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('create/', views.HotelCreateView.as_view(), name='hotel-create'),
    path('update/<int:pk>/', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('delete/<int:pk>/', views.HotelDeleteView.as_view(), name='hotel-delete'),
]