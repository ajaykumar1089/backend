def car_image_upload_path(instance, filename):
    """Generate upload path for car images"""
    return f'cars/{instance.car.id}/{filename}'