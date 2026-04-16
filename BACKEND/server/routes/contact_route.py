from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, mail
from flask_mail import Message
from ..models import Contact, User
import re

contact_bp = Blueprint('contact', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Submit a contact form message"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({"error": "Name, email, and message are required"}), 400
    
    name = data['name'].strip()
    email = data['email'].strip()
    subject = data.get('subject', '').strip()
    message = data['message'].strip()
    
    # Validate email format
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate name length
    if len(name) < 2 or len(name) > 100:
        return jsonify({"error": "Name must be between 2 and 100 characters"}), 400
    
    # Validate message length
    if len(message) < 10 or len(message) > 2000:
        return jsonify({"error": "Message must be between 10 and 2000 characters"}), 400
    
    # Create contact entry
    contact = Contact(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    
    try:
        db.session.add(contact)
        db.session.commit()

        # Send notification email to site owner
        notify_errors = None
        try:
            subject_line = f"New contact: {subject or 'No subject'} from {name}"
            body = (
                f"You have received a new contact message from your portfolio site.\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject or 'N/A'}\n\n"
                f"Message:\n{message}\n\n"
                f"Submitted via API /contact"
            )

            owner_email = mail.app.config.get('MAIL_USERNAME') or mail.app.config.get('MAIL_DEFAULT_SENDER')
            if isinstance(owner_email, (list, tuple)):
                owner_email = owner_email[-1]

            msg_owner = Message(subject=subject_line, recipients=[owner_email])
            msg_owner.body = body
            mail.send(msg_owner)
        except Exception as mail_err:
            notify_errors = str(mail_err)

        # Send acknowledgement to user
        ack_errors = None
        try:
            ack_subject = "Thanks for contacting me"
            ack_body = (
                f"Hi {name},\n\n"
                f"Thanks for reaching out! I have received your message and will get back to you shortly.\n\n"
                f"Your message:\n{message}\n\n"
                f"Regards,\nPortfolio"
            )
            msg_user = Message(subject=ack_subject, recipients=[email])
            msg_user.body = ack_body
            mail.send(msg_user)
        except Exception as ack_err:
            ack_errors = str(ack_err)

        resp = {"message": "Message sent successfully"}
        if notify_errors:
            resp["mail_notification_error"] = notify_errors
        if ack_errors:
            resp["mail_ack_error"] = ack_errors
        return jsonify(resp), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while sending the message", "details": str(e)}), 500


@contact_bp.route('/contact', methods=['GET'])
@jwt_required()
def get_contacts():
    """Get all contact messages (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    # Get query parameters for filtering
    read = request.args.get('read')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    query = Contact.query
    
    if read is not None:
        read_bool = read.lower() == 'true'
        query = query.filter_by(read=read_bool)
    
    # Order by created_at (newest first)
    query = query.order_by(Contact.created_at.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    contacts = pagination.items
    
    contacts_data = []
    for contact in contacts:
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "subject": contact.subject,
            "message": contact.message,
            "read": contact.read,
            "created_at": contact.created_at.isoformat() if contact.created_at else None
        }
        contacts_data.append(contact_data)
    
    return jsonify({
        "contacts": contacts_data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200


@contact_bp.route('/contact/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    """Get a specific contact message (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    contact = Contact.query.get_or_404(contact_id)
    
    contact_data = {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "subject": contact.subject,
        "message": contact.message,
        "read": contact.read,
        "created_at": contact.created_at.isoformat() if contact.created_at else None
    }
    
    return jsonify(contact_data), 200


@contact_bp.route('/contact/<int:contact_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(contact_id):
    """Mark a contact message as read (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    contact = Contact.query.get_or_404(contact_id)
    contact.read = True
    
    try:
        db.session.commit()
        return jsonify({"message": "Message marked as read"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the message", "details": str(e)}), 500


@contact_bp.route('/contact/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    """Delete a contact message (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    contact = Contact.query.get_or_404(contact_id)
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Message deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the message", "details": str(e)}), 500


@contact_bp.route('/contact/<int:contact_id>/reply', methods=['POST'])
@jwt_required()
def reply_contact(contact_id):
    """Reply to a contact message (admin only) - sends an email to the contact sender"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403

    contact = Contact.query.get_or_404(contact_id)

    data = request.get_json() or {}
    reply_subject = (data.get('subject') or '').strip()
    reply_message = (data.get('message') or '').strip()

    if not reply_message:
        return jsonify({"error": "Reply message is required"}), 400

    if not reply_subject:
        base = contact.subject or 'your message'
        reply_subject = f"Re: {base}"

    try:
        # Determine sender and reply-to
        default_sender = mail.app.config.get('MAIL_DEFAULT_SENDER')
        owner_email = mail.app.config.get('MAIL_USERNAME') or (default_sender[-1] if isinstance(default_sender, (list, tuple)) else default_sender)

        msg = Message(subject=reply_subject, recipients=[contact.email])
        msg.body = reply_message
        if owner_email:
            msg.reply_to = owner_email

        mail.send(msg)

        # Optionally mark as read after replying
        contact.read = True
        db.session.commit()

        return jsonify({"message": "Reply sent successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to send reply", "details": str(e)}), 500


@contact_bp.route('/contact/stats', methods=['GET'])
@jwt_required()
def get_contact_stats():
    """Get contact form statistics (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    try:
        total_messages = Contact.query.count()
        unread_messages = Contact.query.filter_by(read=False).count()
        read_messages = Contact.query.filter_by(read=True).count()
        
        # Get messages count by month for the last 6 months
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        monthly_stats = db.session.query(
            func.date_trunc('month', Contact.created_at).label('month'),
            func.count(Contact.id).label('count')
        ).filter(Contact.created_at >= six_months_ago).group_by(
            func.date_trunc('month', Contact.created_at)
        ).order_by(func.date_trunc('month', Contact.created_at)).all()
        
        monthly_data = []
        for month, count in monthly_stats:
            monthly_data.append({
                "month": month.strftime('%Y-%m') if month else None,
                "count": count
            })
        
        return jsonify({
            "total_messages": total_messages,
            "unread_messages": unread_messages,
            "read_messages": read_messages,
            "monthly_stats": monthly_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": "An error occurred while getting statistics", "details": str(e)}), 500
