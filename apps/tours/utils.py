import os
from datetime import datetime

def Tour_image_upload_path(instance, filename):
    """
    Generate upload path for Tour images.
    This function ensures the directory exists and creates a unique filename.
    """
    # Create directory path
    upload_dir = 'Tours/images'
    
    # Get file extension
    _, ext = os.path.splitext(filename)
    
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{instance.Tour.id}_{timestamp}_{instance.Tour.title.replace(' ', '_').lower()}{ext}"
    
    return os.path.join(upload_dir, new_filename)