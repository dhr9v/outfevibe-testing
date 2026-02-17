import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
    
    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_file_size(file):
    """
    Check if file size is within limits
    
    Args:
        file: FileStorage object
    
    Returns:
        bool: True if size is acceptable
    """
    # Seek to end to get size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset pointer
    
    return size <= Config.MAX_FILE_SIZE

def sanitize_filename(filename):
    """
    Create a safe filename
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename with timestamp
    """
    from datetime import datetime
    
    secure_name = secure_filename(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(secure_name)
    
    return f"{name}_{timestamp}{ext}"
