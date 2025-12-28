def campervan_image_upload_path(instance, filename):
    """Generate upload path for campervan images"""
    return f'campervans/{instance.campervan.id}/{filename}'