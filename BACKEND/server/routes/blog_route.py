from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Blog, User
import json
import re
from datetime import datetime

blog_bp = Blueprint('blog', __name__)


def get_current_user():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    return db.session.get(User, current_user_id)


def generate_slug(title):
    """Generate a URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


@blog_bp.route('/blog', methods=['GET'])
def get_blogs():
    """Get all published blogs with optional filtering"""
    published = request.args.get('published', 'true')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    tag = request.args.get('tag')
    
    query = Blog.query
    
    # Filter by published status
    if published.lower() == 'true':
        query = query.filter_by(published=True)
    elif published.lower() == 'false':
        query = query.filter_by(published=False)
    # If published='all', don't filter by published status
    
    # Filter by tag if provided
    if tag:
        query = query.filter(Blog.tags.contains(tag))
    
    # Order by published_at (newest first) for published blogs, created_at for drafts
    if published.lower() == 'true':
        query = query.order_by(Blog.published_at.desc())
    else:
        query = query.order_by(Blog.created_at.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    blogs = pagination.items
    
    blogs_data = []
    for blog in blogs:
        blog_data = {
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "excerpt": blog.excerpt,
            "featured_image": blog.featured_image,
            "author": {
                "id": blog.author.id,
                "username": blog.author.username,
                "first_name": blog.author.first_name,
                "last_name": blog.author.last_name
            } if blog.author else None,
            "published": blog.published,
            "published_at": blog.published_at.isoformat() if blog.published_at else None,
            "tags": json.loads(blog.tags) if blog.tags else [],
            "views": blog.views,
            "created_at": blog.created_at.isoformat() if blog.created_at else None
        }
        blogs_data.append(blog_data)
    
    return jsonify({
        "blogs": blogs_data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200


@blog_bp.route('/blog/<slug>', methods=['GET'])
def get_blog_by_slug(slug):
    """Get a specific blog by slug"""
    blog = Blog.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Increment view count
    blog.views += 1
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    blog_data = {
        "id": blog.id,
        "title": blog.title,
        "slug": blog.slug,
        "content": blog.content,
        "excerpt": blog.excerpt,
        "featured_image": blog.featured_image,
        "author": {
            "id": blog.author.id,
            "username": blog.author.username,
            "first_name": blog.author.first_name,
            "last_name": blog.author.last_name
        } if blog.author else None,
        "published": blog.published,
        "published_at": blog.published_at.isoformat() if blog.published_at else None,
        "tags": json.loads(blog.tags) if blog.tags else [],
        "views": blog.views,
        "created_at": blog.created_at.isoformat() if blog.created_at else None,
        "updated_at": blog.updated_at.isoformat() if blog.updated_at else None
    }
    
    return jsonify(blog_data), 200


@blog_bp.route('/blog', methods=['POST'])
@jwt_required()
def create_blog():
    """Create a new blog post (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400
    
    title = data['title'].strip()
    content = data['content'].strip()
    
    # Generate slug from title
    slug = generate_slug(title)
    
    # Check if slug already exists
    existing_blog = Blog.query.filter_by(slug=slug).first()
    if existing_blog:
        # Add a number to make it unique
        counter = 1
        while existing_blog:
            new_slug = f"{slug}-{counter}"
            existing_blog = Blog.query.filter_by(slug=new_slug).first()
            counter += 1
        slug = new_slug
    
    # Create blog
    blog = Blog(
        title=title,
        slug=slug,
        content=content,
        excerpt=data.get('excerpt', ''),
        featured_image=data.get('featured_image'),
        author_id=user.id,
        published=data.get('published', False),
        tags=json.dumps(data.get('tags', []))
    )
    
    # Set published_at if publishing
    if blog.published:
        blog.published_at = datetime.utcnow()
    
    try:
        db.session.add(blog)
        db.session.commit()
        return jsonify({"message": "Blog created successfully", "id": blog.id, "slug": blog.slug}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the blog", "details": str(e)}), 500


@blog_bp.route('/blog/<int:blog_id>', methods=['PUT'])
@jwt_required()
def update_blog(blog_id):
    """Update a blog post (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    blog = Blog.query.get_or_404(blog_id)
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        new_title = data['title'].strip()
        blog.title = new_title
        
        # Generate new slug if title changed
        new_slug = generate_slug(new_title)
        if new_slug != blog.slug:
            # Check if new slug exists
            existing_blog = Blog.query.filter_by(slug=new_slug).first()
            if existing_blog and existing_blog.id != blog_id:
                # Add a number to make it unique
                counter = 1
                while existing_blog:
                    new_slug = f"{generate_slug(new_title)}-{counter}"
                    existing_blog = Blog.query.filter_by(slug=new_slug).first()
                    counter += 1
            blog.slug = new_slug
    
    if 'content' in data:
        blog.content = data['content'].strip()
    if 'excerpt' in data:
        blog.excerpt = data['excerpt'].strip()
    if 'featured_image' in data:
        blog.featured_image = data['featured_image']
    if 'tags' in data:
        blog.tags = json.dumps(data['tags'])
    
    # Handle publishing
    if 'published' in data:
        was_published = blog.published
        blog.published = data['published']
        
        # Set published_at if publishing for the first time
        if blog.published and not was_published:
            blog.published_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({"message": "Blog updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the blog", "details": str(e)}), 500


@blog_bp.route('/blog/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog(blog_id):
    """Delete a blog post (admin only)"""
    user = get_current_user()
    if not user or not user.is_admin:
        return jsonify({"error": "Admin access required"}), 403
    
    blog = Blog.query.get_or_404(blog_id)
    
    try:
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"message": "Blog deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the blog", "details": str(e)}), 500


@blog_bp.route('/blog/tags', methods=['GET'])
def get_blog_tags():
    """Get all unique blog tags"""
    blogs = Blog.query.filter_by(published=True).all()
    all_tags = set()
    
    for blog in blogs:
        if blog.tags:
            tags = json.loads(blog.tags)
            all_tags.update(tags)
    
    return jsonify(list(all_tags)), 200


@blog_bp.route('/blog/search', methods=['GET'])
def search_blogs():
    """Search blogs by title, content, or tags"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    # Search in title, content, and tags
    blogs = Blog.query.filter(
        Blog.published == True,
        db.or_(
            Blog.title.ilike(f'%{query}%'),
            Blog.content.ilike(f'%{query}%'),
            Blog.tags.ilike(f'%{query}%')
        )
    ).order_by(Blog.published_at.desc()).all()
    
    blogs_data = []
    for blog in blogs:
        blog_data = {
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "excerpt": blog.excerpt,
            "featured_image": blog.featured_image,
            "published_at": blog.published_at.isoformat() if blog.published_at else None,
            "tags": json.loads(blog.tags) if blog.tags else []
        }
        blogs_data.append(blog_data)
    
    return jsonify({"blogs": blogs_data, "query": query}), 200
