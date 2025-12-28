def trip_image_upload_path(instance, filename):
    """Generate upload path for trip images"""
    return f'trips/{instance.trip.id}/{filename}'