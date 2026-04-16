from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from ..extensions import db
from sqlalchemy import func
from ..models import User, Image
from werkzeug.security import generate_password_hash
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

# Blueprint Configuration
users_bp = Blueprint('auth', __name__)
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

def allowed_image(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_IMAGE_EXTENSIONS


# Utility function to get the current logged in user based on JWT token
def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


# A protected route to test user access tokens
@users_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"message": f"Welcome, {user.username}! You are authorized to access this route"})


@users_bp.route("/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    # Refresh token is required to generate new tokens
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_access_token}), 200


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if email and password are provided
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password are required"}), 400

    email = data['email'].strip().lower()
    password = data['password']

    # Fetch the user from the database (case-insensitive email match)
    user = User.query.filter(func.lower(User.email) == email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }), 200


@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    # Hash passwords before storing them in the database
    password_hash = generate_password_hash(password)

    # Create a new user
    user = User(username=username, email=email, password_hash=password_hash)
    try:    
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the user", "details": str(e)}), 500


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "title": user.title,
        "location": user.location,
        "phone": user.phone,
        "avatar_url": user.avatar_url,
        "github_url": user.github_url,
        "linkedin_url": user.linkedin_url,
        "twitter_url": user.twitter_url,
        "instagram_url": user.instagram_url,
        "whatsapp_url": user.whatsapp_url,
        "website_url": user.website_url,
        "email_url": user.email_url,
        "hero_image_url": user.hero_image_url,
        "about_image_url": user.about_image_url,
        "cv_url": user.cv_url,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200


@users_bp.route('/public-profile', methods=['GET'])
def get_public_profile():
    """Public endpoint to get portfolio owner's profile data without authentication"""
    # Get the first admin user (portfolio owner)
    user = User.query.filter_by(is_admin=True).first()
    # Fallback: if no admin user exists yet, return the first available user
    if not user:
        user = User.query.first()
    # If absolutely no users exist, return 404. Only data from the database is used.
    if not user:
        return jsonify({"message": "Portfolio owner not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "title": user.title,
        "location": user.location,
        "phone": user.phone,
        "avatar_url": user.avatar_url,
        "github_url": user.github_url,
        "linkedin_url": user.linkedin_url,
        "twitter_url": user.twitter_url,
        "instagram_url": user.instagram_url,
        "whatsapp_url": user.whatsapp_url,
        "website_url": user.website_url,
        "email_url": user.email_url,
        "hero_image_url": user.hero_image_url,
        "about_image_url": user.about_image_url,
        "cv_url": user.cv_url,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'bio' in data:
        user.bio = data['bio']
    if 'title' in data:
        user.title = data['title']
    if 'location' in data:
        user.location = data['location']
    if 'phone' in data:
        user.phone = data['phone']
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']
    if 'github_url' in data:
        user.github_url = data['github_url']
    if 'linkedin_url' in data:
        user.linkedin_url = data['linkedin_url']
    if 'twitter_url' in data:
        user.twitter_url = data['twitter_url']
    if 'instagram_url' in data:
        user.instagram_url = data['instagram_url']
    if 'whatsapp_url' in data:
        user.whatsapp_url = data['whatsapp_url']
    if 'website_url' in data:
        user.website_url = data['website_url']
    if 'email_url' in data:
        user.email_url = data['email_url']
    if 'hero_image_url' in data:
        user.hero_image_url = data['hero_image_url']
    if 'about_image_url' in data:
        user.about_image_url = data['about_image_url']
    if 'cv_url' in data:
        user.cv_url = data['cv_url']
    
    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the profile", "details": str(e)}), 500


@users_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({"error": "Current password and new password are required"}), 400
    
    # Verify current password
    if not check_password_hash(user.password_hash, data['current_password']):
        return jsonify({"error": "Current password is incorrect"}), 400
    
    # Hash new password
    user.password_hash = generate_password_hash(data['new_password'])
    
    try:
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while changing the password", "details": str(e)}), 500


# Image upload endpoints
@users_bp.route('/profile/upload/<image_type>', methods=['POST'])
@jwt_required()
def upload_profile_image(image_type):
    """Upload hero, about, or avatar image and store in database with metadata."""
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if image_type not in {'hero', 'about', 'avatar'}:
        return jsonify({"error": "Invalid image type"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_image(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    # Create upload directory
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads')
    upload_dir = os.path.normpath(upload_dir)
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename while preserving original name
    original_filename = secure_filename(file.filename)
    name_without_ext, file_ext = os.path.splitext(original_filename)
    unique_id = uuid.uuid4().hex[:8]  # Short unique ID
    unique_filename = f"{name_without_ext}_{unique_id}{file_ext}"
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    # Get file info
    file_size = os.path.getsize(file_path)
    mime_type = file.content_type or 'image/jpeg'
    
    # Public URL
    public_url = f"/static/uploads/{unique_filename}"

    try:
        # Deactivate previous images of this type for this user
        Image.query.filter_by(user_id=user.id, image_type=image_type, is_active=True).update({'is_active': False})
        
        # Create new image record
        new_image = Image(
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_url=public_url,
            file_size=file_size,
            mime_type=mime_type,
            image_type=image_type,
            user_id=user.id,
            is_active=True
        )
        
        db.session.add(new_image)
        
        # Update user profile with new image URL
        if image_type == 'hero':
            user.hero_image_url = public_url
        elif image_type == 'about':
            user.about_image_url = public_url
        elif image_type == 'avatar':
            user.avatar_url = public_url
            
        db.session.commit()
        
        return jsonify({
            "message": "Image uploaded successfully",
            "url": public_url,
            "image_id": new_image.id,
            "filename": unique_filename,
            "file_size": file_size
        }), 200
        
    except Exception as e:
        db.session.rollback()
        # Clean up uploaded file if database save fails
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": "Failed to save image", "details": str(e)}), 500


@users_bp.route('/profile/images', methods=['GET'])
@jwt_required()
def get_user_images():
    """Get all images for the current user."""
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    images = Image.query.filter_by(user_id=user.id, is_active=True).all()
    
    return jsonify({
        "images": [{
            "id": img.id,
            "filename": img.filename,
            "original_filename": img.original_filename,
            "file_url": img.file_url,
            "file_size": img.file_size,
            "mime_type": img.mime_type,
            "image_type": img.image_type,
            "created_at": img.created_at.isoformat()
        } for img in images]
    }), 200


@users_bp.route('/profile/images/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete_user_image(image_id):
    """Delete a specific image."""
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    image = Image.query.filter_by(id=image_id, user_id=user.id).first()
    if not image:
        return jsonify({"error": "Image not found"}), 404
    
    try:
        # Delete physical file
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        
        # Remove from database
        db.session.delete(image)
        
        # Update user profile if this was the active image
        if image.image_type == 'hero' and user.hero_image_url == image.file_url:
            user.hero_image_url = None
        elif image.image_type == 'about' and user.about_image_url == image.file_url:
            user.about_image_url = None
        elif image.image_type == 'avatar' and user.avatar_url == image.file_url:
            user.avatar_url = None
            
        db.session.commit()
        
        return jsonify({"message": "Image deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete image", "details": str(e)}), 500

