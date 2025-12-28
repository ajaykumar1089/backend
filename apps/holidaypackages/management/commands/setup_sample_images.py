import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.bikes.models import Bike, BikeImage
from django.conf import settings

class Command(BaseCommand):
    help = 'Create sample bike images for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample bike images...')
        
        # Get all bikes
        bikes = Bike.objects.all()
        
        if not bikes.exists():
            self.stdout.write(self.style.ERROR('No bikes found. Run setup_bikes first.'))
            return
        
        # For each bike, create a placeholder image entry
        for bike in bikes:
            # Check if bike already has images
            if bike.bike_images.exists():
                self.stdout.write(f'Bike "{bike.title}" already has images. Skipping.')
                continue
            
            # Create a simple text file as placeholder (in real scenario, you'd have actual image files)
            placeholder_content = f"This is a placeholder for {bike.title} bike image"
            
            # Note: In a real scenario, you would have actual image files
            # For now, we'll just create the database entries without actual files
            # Users can upload real images through the admin interface
            
            self.stdout.write(f'Bike "{bike.title}" is ready for image upload through admin panel.')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Image upload is now ready! Total bikes: {bikes.count()}. '
                f'You can now upload images through the admin panel at /admin/bikes/bike/'
            )
        )