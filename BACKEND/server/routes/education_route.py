from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Education, User
from datetime import datetime

education_bp = Blueprint('education', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


@education_bp.route('/education', methods=['GET'])
def get_education():
    """Get all education entries"""
    education_entries = Education.query.order_by(Education.start_date.desc()).all()
    
    education_data = []
    for edu in education_entries:
        edu_data = {
            "id": edu.id,
            "institution": edu.institution,
            "degree": edu.degree,
            "field_of_study": edu.field_of_study,
            "description": edu.description,
            "start_date": edu.start_date.isoformat() if edu.start_date else None,
            "end_date": edu.end_date.isoformat() if edu.end_date else None,
            "current": edu.current,
            "gpa": edu.gpa,
            "location": edu.location,
            "institution_logo": edu.institution_logo,
            "created_at": edu.created_at.isoformat() if edu.created_at else None,
            "updated_at": edu.updated_at.isoformat() if edu.updated_at else None
        }
        education_data.append(edu_data)
    
    return jsonify(education_data), 200


@education_bp.route('/education/<int:edu_id>', methods=['GET'])
def get_education_by_id(edu_id):
    """Get a specific education entry by ID"""
    edu = Education.query.get_or_404(edu_id)
    
    edu_data = {
        "id": edu.id,
        "institution": edu.institution,
        "degree": edu.degree,
        "field_of_study": edu.field_of_study,
        "description": edu.description,
        "start_date": edu.start_date.isoformat() if edu.start_date else None,
        "end_date": edu.end_date.isoformat() if edu.end_date else None,
        "current": edu.current,
        "gpa": edu.gpa,
        "location": edu.location,
        "institution_logo": edu.institution_logo,
        "created_at": edu.created_at.isoformat() if edu.created_at else None,
        "updated_at": edu.updated_at.isoformat() if edu.updated_at else None
    }
    
    return jsonify(edu_data), 200


@education_bp.route('/education', methods=['POST'])
@jwt_required()
def create_education():
    """Create a new education entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('institution') or not data.get('degree') or not data.get('field_of_study') or not data.get('start_date'):
        return jsonify({"error": "Institution, degree, field_of_study, and start_date are required"}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = None
        if data.get('end_date'):
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Create education
    edu = Education(
        institution=data['institution'],
        degree=data['degree'],
        field_of_study=data['field_of_study'],
        description=data.get('description'),
        start_date=start_date,
        end_date=end_date,
        current=data.get('current', False),
        gpa=data.get('gpa'),
        location=data.get('location'),
        institution_logo=data.get('institution_logo')
    )
    
    try:
        db.session.add(edu)
        db.session.commit()
        return jsonify({"message": "Education created successfully", "id": edu.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the education", "details": str(e)}), 500


@education_bp.route('/education/<int:edu_id>', methods=['PUT'])
@jwt_required()
def update_education(edu_id):
    """Update an education entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    edu = Education.query.get_or_404(edu_id)
    data = request.get_json()
    
    # Update fields
    if 'institution' in data:
        edu.institution = data['institution']
    if 'degree' in data:
        edu.degree = data['degree']
    if 'field_of_study' in data:
        edu.field_of_study = data['field_of_study']
    if 'description' in data:
        edu.description = data['description']
    if 'start_date' in data:
        try:
            edu.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    if 'end_date' in data:
        if data['end_date']:
            try:
                edu.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        else:
            edu.end_date = None
    if 'current' in data:
        edu.current = data['current']
    if 'gpa' in data:
        edu.gpa = data['gpa']
    if 'location' in data:
        edu.location = data['location']
    if 'institution_logo' in data:
        edu.institution_logo = data['institution_logo']
    
    try:
        db.session.commit()
        return jsonify({"message": "Education updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the education", "details": str(e)}), 500


@education_bp.route('/education/<int:edu_id>', methods=['DELETE'])
@jwt_required()
def delete_education(edu_id):
    """Delete an education entry (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    edu = Education.query.get_or_404(edu_id)
    
    try:
        db.session.delete(edu)
        db.session.commit()
        return jsonify({"message": "Education deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the education", "details": str(e)}), 500
