from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking-delete'),
]