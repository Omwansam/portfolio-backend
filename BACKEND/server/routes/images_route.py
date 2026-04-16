from flask import Blueprint, request, jsonify, url_for, current_app
from ..models import Image, User, Project, Blog
from ..utils.images import (
    save_portfolio_image, 
    delete_image_file, 
    allowed_file, 
    get_file_size, 
    get_mime_type
)
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

# Blueprint Configuration
images_bp = Blueprint('images', __name__)
MAX_IMAGES_PER_ENTITY = 20

@images_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    """Upload a new image for portfolio use."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        # Validate request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Allowed types: png, jpg, jpeg, gif'}), 400

        # Get image metadata from form
        image_type = request.form.get('image_type', 'general')
        entity_id = request.form.get('entity_id', type=int)
        project_id = request.form.get('project_id', type=int)
        blog_id = request.form.get('blog_id', type=int)

        # Validate image type
        valid_types = ['hero', 'about', 'avatar', 'project', 'blog', 'general', 'skill', 'experience', 'education']
        if image_type not in valid_types:
            return jsonify({'error': f'Invalid image type. Valid types: {", ".join(valid_types)}'}), 400

        # Check image limits for specific entities
        if entity_id and image_type in ['project', 'blog']:
            current_count = Image.query.filter_by(
                **{f'{image_type}_id': entity_id, 'is_active': True}
            ).count()
            if current_count >= MAX_IMAGES_PER_ENTITY:
                return jsonify({'error': f'Maximum {MAX_IMAGES_PER_ENTITY} images per {image_type} reached'}), 400

        # Save the image file
        image_path = save_portfolio_image(file, image_type, entity_id, current_user_id)
        if not image_path:
            return jsonify({'error': 'Image upload failed'}), 500

        # Get file metadata
        full_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(image_path))
        file_size = get_file_size(full_file_path)
        mime_type = get_mime_type(file.filename)

        # Create image record
        new_image = Image(
            filename=os.path.basename(image_path),
            original_filename=file.filename,
            file_path=image_path,
            file_url=url_for('static', filename=image_path, _external=True),
            file_size=file_size,
            mime_type=mime_type,
            image_type=image_type,
            user_id=current_user_id,
            project_id=project_id if image_type == 'project' else None,
            blog_id=blog_id if image_type == 'blog' else None
        )

        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            'message': 'Image uploaded successfully',
            'image_id': new_image.id,
            'filename': new_image.filename,
            'file_url': new_image.file_url,
            'image_type': new_image.image_type,
            'file_size': new_image.file_size,
            'mime_type': new_image.mime_type
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to upload image: {str(e)}")
        return jsonify({'error': 'Image upload failed'}), 500


@images_bp.route('/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """Get image details by ID."""
    try:
        image = Image.query.get_or_404(image_id)
        
        if not image.is_active:
            return jsonify({'error': 'Image not found'}), 404

        return jsonify({
            'image_id': image.id,
            'filename': image.filename,
            'original_filename': image.original_filename,
            'file_url': image.file_url,
            'file_size': image.file_size,
            'mime_type': image.mime_type,
            'image_type': image.image_type,
            'user_id': image.user_id,
            'project_id': image.project_id,
            'blog_id': image.blog_id,
            'created_at': image.created_at.isoformat(),
            'updated_at': image.updated_at.isoformat()
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to get image: {str(e)}")
        return jsonify({'error': 'Failed to retrieve image'}), 500


@images_bp.route('/type/<image_type>', methods=['GET'])
def get_images_by_type(image_type):
    """Get all images of a specific type."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate image type
        valid_types = ['hero', 'about', 'avatar', 'project', 'blog', 'general', 'skill', 'experience', 'education']
        if image_type not in valid_types:
            return jsonify({'error': f'Invalid image type. Valid types: {", ".join(valid_types)}'}), 400

        images = Image.query.filter_by(
            image_type=image_type, 
            is_active=True
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return jsonify({
            'images': [{
                'image_id': img.id,
                'filename': img.filename,
                'file_url': img.file_url,
                'file_size': img.file_size,
                'mime_type': img.mime_type,
                'created_at': img.created_at.isoformat()
            } for img in images.items],
            'total': images.total,
            'pages': images.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to get images by type: {str(e)}")
        return jsonify({'error': 'Failed to retrieve images'}), 500


@images_bp.route('/entity/<entity_type>/<int:entity_id>', methods=['GET'])
def get_entity_images(entity_type, entity_id):
    """Get all images for a specific entity (project, blog, etc.)."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate entity type
        valid_entity_types = ['project', 'blog', 'user']
        if entity_type not in valid_entity_types:
            return jsonify({'error': f'Invalid entity type. Valid types: {", ".join(valid_entity_types)}'}), 400

        # Build query based on entity type
        if entity_type == 'project':
            images = Image.query.filter_by(
                project_id=entity_id, 
                is_active=True
            ).paginate(page=page, per_page=per_page, error_out=False)
        elif entity_type == 'blog':
            images = Image.query.filter_by(
                blog_id=entity_id, 
                is_active=True
            ).paginate(page=page, per_page=per_page, error_out=False)
        elif entity_type == 'user':
            images = Image.query.filter_by(
                user_id=entity_id, 
                is_active=True
            ).paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'images': [{
                'image_id': img.id,
                'filename': img.filename,
                'file_url': img.file_url,
                'file_size': img.file_size,
                'mime_type': img.mime_type,
                'image_type': img.image_type,
                'created_at': img.created_at.isoformat()
            } for img in images.items],
            'total': images.total,
            'pages': images.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to get entity images: {str(e)}")
        return jsonify({'error': 'Failed to retrieve entity images'}), 500


@images_bp.route('/<int:image_id>', methods=['PUT'])
@jwt_required()
def update_image(image_id):
    """Update image metadata."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        image = Image.query.get_or_404(image_id)
        data = request.get_json()

        # Update allowed fields
        if 'image_type' in data:
            valid_types = ['hero', 'about', 'avatar', 'project', 'blog', 'general', 'skill', 'experience', 'education']
            if data['image_type'] not in valid_types:
                return jsonify({'error': f'Invalid image type. Valid types: {", ".join(valid_types)}'}), 400
            image.image_type = data['image_type']

        if 'project_id' in data:
            image.project_id = data['project_id']

        if 'blog_id' in data:
            image.blog_id = data['blog_id']

        db.session.commit()

        return jsonify({
            'message': 'Image updated successfully',
            'image_id': image.id,
            'image_type': image.image_type,
            'project_id': image.project_id,
            'blog_id': image.blog_id
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to update image: {str(e)}")
        return jsonify({'error': 'Failed to update image'}), 500


@images_bp.route('/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete_image(image_id):
    """Delete an image (soft delete)."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        image = Image.query.get_or_404(image_id)
        
        if not image.is_active:
            return jsonify({'error': 'Image not found'}), 404

        # Delete the physical file
        if not delete_image_file(image.file_path):
            current_app.logger.warning(f"Failed to delete image file: {image.file_path}")

        # Soft delete - mark as inactive
        image.is_active = False
        db.session.commit()

        return jsonify({
            'message': 'Image deleted successfully',
            'image_id': image.id
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to delete image: {str(e)}")
        return jsonify({'error': 'Failed to delete image'}), 500


@images_bp.route('/hard-delete/<int:image_id>', methods=['DELETE'])
@jwt_required()
def hard_delete_image(image_id):
    """Permanently delete an image from database and filesystem."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        image = Image.query.get_or_404(image_id)

        # Delete the physical file
        if not delete_image_file(image.file_path):
            current_app.logger.warning(f"Failed to delete image file: {image.file_path}")

        # Hard delete from database
        db.session.delete(image)
        db.session.commit()

        return jsonify({
            'message': 'Image permanently deleted',
            'image_id': image_id
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to hard delete image: {str(e)}")
        return jsonify({'error': 'Failed to delete image'}), 500


@images_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_image_stats():
    """Get image statistics for admin dashboard."""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        # Get statistics
        total_images = Image.query.filter_by(is_active=True).count()
        images_by_type = db.session.query(
            Image.image_type, 
            db.func.count(Image.id)
        ).filter_by(is_active=True).group_by(Image.image_type).all()

        total_size = db.session.query(db.func.sum(Image.file_size)).filter_by(is_active=True).scalar() or 0

        return jsonify({
            'total_images': total_images,
            'images_by_type': dict(images_by_type),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to get image stats: {str(e)}")
        return jsonify({'error': 'Failed to retrieve image statistics'}), 500
