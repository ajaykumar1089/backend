def hotel_image_upload_path(instance, filename):
    """Generate upload path for hotel images"""
    return f'hotels/{instance.hotel.id}/{filename}'