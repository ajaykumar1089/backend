from django.urls import path
from . import views

urlpatterns = [
    path('', views.GuidedTripListView.as_view(), name='guided_trip_list'),
    path('<int:pk>/', views.GuidedTripDetailView.as_view(), name='guided_trip_detail'),
    path('create/', views.GuidedTripCreateView.as_view(), name='guided_trip_create'),
    path('update/<int:pk>/', views.GuidedTripUpdateView.as_view(), name='guided_trip_update'),
    path('delete/<int:pk>/', views.GuidedTripDeleteView.as_view(), name='guided_trip_delete'),
]