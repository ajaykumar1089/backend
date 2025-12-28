def pilgrim_image_upload_path(instance, filename):
    """Generate upload path for pilgrim tour and hotel images"""
    if hasattr(instance, 'tour'):
        return f'pilgrim/tours/{instance.tour.id}/{filename}'
    elif hasattr(instance, 'hotel'):
        return f'pilgrim/hotels/{instance.hotel.id}/{filename}'
    else:
        return f'pilgrim/{filename}'