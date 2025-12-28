from django.urls import path
from . import views

urlpatterns = [
    path('', views.CampervanListView.as_view(), name='campervan-list'),
    path('<int:pk>/', views.CampervanDetailView.as_view(), name='campervan-detail'),
    path('create/', views.CampervanCreateView.as_view(), name='campervan-create'),
    path('update/<int:pk>/', views.CampervanUpdateView.as_view(), name='campervan-update'),
    path('delete/<int:pk>/', views.CampervanDeleteView.as_view(), name='campervan-delete'),
]