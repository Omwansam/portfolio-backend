from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Project, User, ProjectStatus
import json

projects_bp = Blueprint('projects', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects with optional filtering"""
    status = request.args.get('status')
    featured = request.args.get('featured')
    
    query = Project.query
    
    if status:
        try:
            status_enum = ProjectStatus(status)
            query = query.filter_by(status=status_enum)
        except ValueError:
            return jsonify({"error": "Invalid status value"}), 400
    
    if featured is not None:
        featured_bool = featured.lower() == 'true'
        query = query.filter_by(featured=featured_bool)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    projects_data = []
    for project in projects:
        project_data = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "short_description": project.short_description,
            "image_url": project.image_url,
            "github_url": project.github_url,
            "live_url": project.live_url,
            "status": project.status.value,
            "featured": project.featured,
            "technologies": json.loads(project.technologies) if project.technologies else [],
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
        projects_data.append(project_data)
    
    return jsonify(projects_data), 200


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project by ID"""
    project = Project.query.get_or_404(project_id)
    
    project_data = {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "short_description": project.short_description,
        "image_url": project.image_url,
        "github_url": project.github_url,
        "live_url": project.live_url,
        "status": project.status.value,
        "featured": project.featured,
        "technologies": json.loads(project.technologies) if project.technologies else [],
        "created_at": project.created_at.isoformat() if project.created_at else None,
        "updated_at": project.updated_at.isoformat() if project.updated_at else None
    }
    
    return jsonify(project_data), 200


@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """Create a new project (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('description'):
        return jsonify({"error": "Title and description are required"}), 400
    
    # Validate status if provided
    status = ProjectStatus.COMPLETED
    if 'status' in data:
        try:
            status = ProjectStatus(data['status'])
        except ValueError:
            return jsonify({"error": "Invalid status value"}), 400
    
    # Create project
    project = Project(
        title=data['title'],
        description=data['description'],
        short_description=data.get('short_description'),
        image_url=data.get('image_url'),
        github_url=data.get('github_url'),
        live_url=data.get('live_url'),
        status=status,
        featured=data.get('featured', False),
        technologies=json.dumps(data.get('technologies', []))
    )
    
    try:
        db.session.add(project)
        db.session.commit()
        return jsonify({"message": "Project created successfully", "id": project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the project", "details": str(e)}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update a project (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        project.title = data['title']
    if 'description' in data:
        project.description = data['description']
    if 'short_description' in data:
        project.short_description = data['short_description']
    if 'image_url' in data:
        project.image_url = data['image_url']
    if 'github_url' in data:
        project.github_url = data['github_url']
    if 'live_url' in data:
        project.live_url = data['live_url']
    if 'status' in data:
        try:
            project.status = ProjectStatus(data['status'])
        except ValueError:
            return jsonify({"error": "Invalid status value"}), 400
    if 'featured' in data:
        project.featured = data['featured']
    if 'technologies' in data:
        project.technologies = json.dumps(data['technologies'])
    
    try:
        db.session.commit()
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the project", "details": str(e)}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Delete a project (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    project = Project.query.get_or_404(project_id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the project", "details": str(e)}), 500
