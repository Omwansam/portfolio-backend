from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Experience, User
from datetime import datetime

experience_bp = Blueprint('experience', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


@experience_bp.route('/experience', methods=['GET'])
def get_experience():
    """Get all experience entries"""
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    
    experiences_data = []
    for exp in experiences:
        exp_data = {
            "id": exp.id,
            "company": exp.company,
            "position": exp.position,
            "description": exp.description,
            "start_date": exp.start_date.isoformat() if exp.start_date else None,
            "end_date": exp.end_date.isoformat() if exp.end_date else None,
            "current": exp.current,
            "location": exp.location,
            "company_logo": exp.company_logo,
            "created_at": exp.created_at.isoformat() if exp.created_at else None,
            "updated_at": exp.updated_at.isoformat() if exp.updated_at else None
        }
        experiences_data.append(exp_data)
    
    return jsonify(experiences_data), 200


@experience_bp.route('/experience/<int:exp_id>', methods=['GET'])
def get_experience_by_id(exp_id):
    """Get a specific experience entry by ID"""
    exp = Experience.query.get_or_404(exp_id)
    
    exp_data = {
        "id": exp.id,
        "company": exp.company,
        "position": exp.position,
        "description": exp.description,
        "start_date": exp.start_date.isoformat() if exp.start_date else None,
        "end_date": exp.end_date.isoformat() if exp.end_date else None,
        "current": exp.current,
        "location": exp.location,
        "company_logo": exp.company_logo,
        "created_at": exp.created_at.isoformat() if exp.created_at else None,
        "updated_at": exp.updated_at.isoformat() if exp.updated_at else None
    }
    
    return jsonify(exp_data), 200


@experience_bp.route('/experience', methods=['POST'])
@jwt_required()
def create_experience():
    """Create a new experience entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('company') or not data.get('position') or not data.get('description') or not data.get('start_date'):
        return jsonify({"error": "Company, position, description, and start_date are required"}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = None
        if data.get('end_date'):
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Create experience
    exp = Experience(
        company=data['company'],
        position=data['position'],
        description=data['description'],
        start_date=start_date,
        end_date=end_date,
        current=data.get('current', False),
        location=data.get('location'),
        company_logo=data.get('company_logo')
    )
    
    try:
        db.session.add(exp)
        db.session.commit()
        return jsonify({"message": "Experience created successfully", "id": exp.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the experience", "details": str(e)}), 500


@experience_bp.route('/experience/<int:exp_id>', methods=['PUT'])
@jwt_required()
def update_experience(exp_id):
    """Update an experience entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    exp = Experience.query.get_or_404(exp_id)
    data = request.get_json()
    
    # Update fields
    if 'company' in data:
        exp.company = data['company']
    if 'position' in data:
        exp.position = data['position']
    if 'description' in data:
        exp.description = data['description']
    if 'start_date' in data:
        try:
            exp.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    if 'end_date' in data:
        if data['end_date']:
            try:
                exp.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        else:
            exp.end_date = None
    if 'current' in data:
        exp.current = data['current']
    if 'location' in data:
        exp.location = data['location']
    if 'company_logo' in data:
        exp.company_logo = data['company_logo']
    
    try:
        db.session.commit()
        return jsonify({"message": "Experience updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the experience", "details": str(e)}), 500


@experience_bp.route('/experience/<int:exp_id>', methods=['DELETE'])
@jwt_required()
def delete_experience(exp_id):
    """Delete an experience entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    exp = Experience.query.get_or_404(exp_id)
    
    try:
        db.session.delete(exp)
        db.session.commit()
        return jsonify({"message": "Experience deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the experience", "details": str(e)}), 500
