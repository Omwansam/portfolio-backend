from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Skill, User, CategoryStatus

skills_bp = Blueprint('skills', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


@skills_bp.route('/skills', methods=['GET'])
def get_skills():
    """Get all skills with optional filtering"""
    category = request.args.get('category')
    
    query = Skill.query
    
    if category:
        try:
            category_enum = CategoryStatus(category)
            query = query.filter_by(category=category_enum)
        except ValueError:
            return jsonify({"error": "Invalid category value"}), 400
    
    skills = query.order_by(Skill.name.asc()).all()
    
    skills_data = []
    for skill in skills:
        skill_data = {
            "id": skill.id,
            "name": skill.name,
            "category": skill.category.value,
            "proficiency_level": skill.proficiency_level,
            "icon_url": skill.icon_url,
            "created_at": skill.created_at.isoformat() if skill.created_at else None,
            "updated_at": skill.updated_at.isoformat() if skill.updated_at else None
        }
        skills_data.append(skill_data)
    
    return jsonify(skills_data), 200


@skills_bp.route('/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    """Get a specific skill by ID"""
    skill = Skill.query.get_or_404(skill_id)
    
    skill_data = {
        "id": skill.id,
        "name": skill.name,
        "category": skill.category.value,
        "proficiency_level": skill.proficiency_level,
        "icon_url": skill.icon_url,
        "created_at": skill.created_at.isoformat() if skill.created_at else None,
        "updated_at": skill.updated_at.isoformat() if skill.updated_at else None
    }
    
    return jsonify(skill_data), 200


@skills_bp.route('/skills', methods=['POST'])
@jwt_required()
def create_skill():
    """Create a new skill (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name') or not data.get('proficiency_level'):
        return jsonify({"error": "Name and proficiency level are required"}), 400
    
    # Validate category if provided
    category = CategoryStatus.LANGUAGE
    if 'category' in data:
        try:
            category = CategoryStatus(data['category'])
        except ValueError:
            return jsonify({"error": "Invalid category value"}), 400
    
    # Check if skill already exists
    existing_skill = Skill.query.filter_by(name=data['name']).first()
    if existing_skill:
        return jsonify({"error": "Skill with this name already exists"}), 400
    
    # Create skill
    skill = Skill(
        name=data['name'],
        category=category,
        proficiency_level=data['proficiency_level'],
        icon_url=data.get('icon_url')
    )
    
    try:
        db.session.add(skill)
        db.session.commit()
        return jsonify({"message": "Skill created successfully", "id": skill.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the skill", "details": str(e)}), 500


@skills_bp.route('/skills/<int:skill_id>', methods=['PUT'])
@jwt_required()
def update_skill(skill_id):
    """Update a skill (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        # Check if new name conflicts with existing skill
        existing_skill = Skill.query.filter_by(name=data['name']).first()
        if existing_skill and existing_skill.id != skill_id:
            return jsonify({"error": "Skill with this name already exists"}), 400
        skill.name = data['name']
    
    if 'category' in data:
        try:
            skill.category = CategoryStatus(data['category'])
        except ValueError:
            return jsonify({"error": "Invalid category value"}), 400
    
    if 'proficiency_level' in data:
        skill.proficiency_level = data['proficiency_level']
    
    if 'icon_url' in data:
        skill.icon_url = data['icon_url']
    
    try:
        db.session.commit()
        return jsonify({"message": "Skill updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the skill", "details": str(e)}), 500


@skills_bp.route('/skills/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    """Delete a skill (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    skill = Skill.query.get_or_404(skill_id)
    
    try:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({"message": "Skill deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the skill", "details": str(e)}), 500


@skills_bp.route('/skills/categories', methods=['GET'])
def get_categories():
    """Get all available skill categories"""
    categories = [category.value for category in CategoryStatus]
    return jsonify(categories), 200
