import os
from werkzeug.utils import secure_filename
from flask import current_app
from pathlib import Path
import uuid
from datetime import datetime

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(filename, image_type, entity_id=None):
    """Generate a unique filename using UUID and image type."""
    basename = secure_filename(filename.rsplit('.',1)[0])
    extension = filename.rsplit('.',1)[1].lower()
    unique_id = str(uuid.uuid4())[:8]
    
    if entity_id:
        return f"{image_type}_{entity_id}_{unique_id}_{basename}.{extension}"
    else:
        return f"{image_type}_{unique_id}_{basename}.{extension}"


def save_portfolio_image(file, image_type, entity_id=None, user_id=None):
    """Save the uploaded image and return the relative path."""
    if not file or not allowed_file(file.filename):
        return None

    filename = generate_unique_filename(file.filename, image_type, entity_id)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(file_path)
        return f"uploads/{filename}"
    except Exception as e:
        current_app.logger.error(f"Error saving portfolio image: {str(e)}")
        return None


def get_file_size(file_path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


def get_mime_type(filename):
    """Get MIME type based on file extension."""
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return mime_types.get(extension, 'application/octet-stream')


def delete_image_file(image_url):
    """
    Safely delete an image file from the filesystem.
    
    Args:
        image_url (str): The URL or path of the image to delete
        
    Returns:
        bool: True if file was deleted successfully, False otherwise
    """
    try:
        if not image_url:
            current_app.logger.warning("Empty image URL provided for deletion")
            return False
            
        # Extract filename securely
        filename = secure_filename(os.path.basename(image_url))
        if not filename:
            current_app.logger.error(f"Invalid filename extracted from URL: {image_url}")
            return False
            
        # Build full path safely
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        if not upload_folder:
            current_app.logger.error("UPLOAD_FOLDER not configured")
            return False
            
        file_path = Path(upload_folder) / filename
        
        # Security check - ensure path is within upload folder
        try:
            file_path.resolve().relative_to(Path(upload_folder).resolve())
        except ValueError:
            current_app.logger.error(f"Attempted to delete file outside upload directory: {file_path}")
            return False
            
        # Delete the file
        if file_path.exists():
            file_path.unlink()
            current_app.logger.info(f"Successfully deleted image file: {file_path}")
            return True
            
        current_app.logger.warning(f"Image file not found: {file_path}")
        return False
        
    except Exception as e:
        current_app.logger.error(f"Error deleting image file {image_url}: {str(e)}", exc_info=True)
        return False    