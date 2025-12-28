def story_image_upload_path(instance, filename):
    """Generate upload path for story images"""
    return f'stories/{instance.story.id}/{filename}'