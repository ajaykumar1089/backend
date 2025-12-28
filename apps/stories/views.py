from rest_framework import viewsets
from .models import Userstories
from rest_framework import generics
from .serializers import UserstoriesSerializer

class UserstoriesViewSet(viewsets.ModelViewSet):
    queryset = Userstories.objects.all()
    serializer_class = UserstoriesSerializer

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed

    def perform_update(self, serializer):
        serializer.save()  # You can add additional logic here if needed

    def perform_destroy(self, instance):
        instance.delete()  # You can add additional logic here if needed
		
class UserstoriesListView(generics.ListCreateAPIView):
    """
    API view to list all stories or create a new one.
    """
    queryset = Userstories.objects.all()
    serializer_class = UserstoriesSerializer


class UserstoriesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific story.
    """
    queryset = Userstories.objects.all()
    serializer_class = UserstoriesSerializer
	
class UserstoriesCreateView(generics.CreateAPIView):
    queryset = Userstories.objects.all()
    serializer_class = UserstoriesSerializer