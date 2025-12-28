from django.urls import path
from . import views

urlpatterns = [
   path('', views.UserstoriesListView.as_view(), name='story-list'),
    path('create/', views.UserstoriesCreateView.as_view(), name='story-create'),
    path('<int:pk>/', views.UserstoriesDetailView.as_view(), name='story-detail'),
]