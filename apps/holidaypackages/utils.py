import os
from datetime import datetime

def holidaypackage_image_upload_path(instance, filename):
    """
    Generate upload path for holidaypackage images.
    This function ensures the directory exists and creates a unique filename.
    """
    # Create directory path
    upload_dir = 'holidaypackages/images'
    
    # Get file extension
    _, ext = os.path.splitext(filename)
    
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{instance.holidaypackage.id}_{timestamp}_{instance.holidaypackage.title.replace(' ', '_').lower()}{ext}"
    
    return os.path.join(upload_dir, new_filename)