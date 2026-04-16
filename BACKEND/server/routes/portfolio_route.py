from flask import Blueprint, jsonify
from ..extensions import db
from ..models import User, Project, Skill, Experience, Education, Blog, Contact, ProjectStatus
from sqlalchemy import func
from datetime import datetime, timedelta

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/portfolio/overview', methods=['GET'])
def get_portfolio_overview():
    """Get portfolio overview and statistics"""
    try:
        # Get user profile information
        user = User.query.filter_by(is_admin=True).first()
        if not user:
            return jsonify({"error": "Portfolio owner not found"}), 404
        
        # Count statistics
        total_projects = Project.query.count()
        completed_projects = Project.query.filter_by(status=ProjectStatus.COMPLETED).count()
        total_skills = Skill.query.count()
        total_experience = Experience.query.count()
        total_education = Education.query.count()
        total_blogs = Blog.query.filter_by(published=True).count()
        total_contact_messages = Contact.query.count()
        unread_messages = Contact.query.filter_by(read=False).count()
        
        # Get recent projects
        recent_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
        recent_projects_data = []
        for project in recent_projects:
            project_data = {
                "id": project.id,
                "title": project.title,
                "short_description": project.short_description,
                "image_url": project.image_url,
                "status": project.status.value,
                "featured": project.featured
            }
            recent_projects_data.append(project_data)
        
        # Get featured projects
        featured_projects = Project.query.filter_by(featured=True).limit(3).all()
        featured_projects_data = []
        for project in featured_projects:
            project_data = {
                "id": project.id,
                "title": project.title,
                "short_description": project.short_description,
                "image_url": project.image_url,
                "status": project.status.value
            }
            featured_projects_data.append(project_data)
        
        # Get skills by category
        skills_by_category = {}
        skills = Skill.query.all()
        for skill in skills:
            category = skill.category.value
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append({
                "id": skill.id,
                "name": skill.name,
                "proficiency_level": skill.proficiency_level,
                "icon_url": skill.icon_url
            })
        
        # Get recent blog posts
        recent_blogs = Blog.query.filter_by(published=True).order_by(Blog.published_at.desc()).limit(3).all()
        recent_blogs_data = []
        for blog in recent_blogs:
            blog_data = {
                "id": blog.id,
                "title": blog.title,
                "slug": blog.slug,
                "excerpt": blog.excerpt,
                "published_at": blog.published_at.isoformat() if blog.published_at else None
            }
            recent_blogs_data.append(blog_data)
        
        # Get monthly project statistics for the last 6 months
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        try:
            # Try PostgreSQL/SQLite date_trunc
            monthly_project_stats = db.session.query(
                func.date_trunc('month', Project.created_at).label('month'),
                func.count(Project.id).label('count')
            ).filter(Project.created_at >= six_months_ago).group_by(
                func.date_trunc('month', Project.created_at)
            ).order_by(func.date_trunc('month', Project.created_at)).all()
        except:
            # Fallback for SQLite - use strftime
            monthly_project_stats = db.session.query(
                func.strftime('%Y-%m', Project.created_at).label('month'),
                func.count(Project.id).label('count')
            ).filter(Project.created_at >= six_months_ago).group_by(
                func.strftime('%Y-%m', Project.created_at)
            ).order_by(func.strftime('%Y-%m', Project.created_at)).all()
        
        monthly_project_data = []
        for month, count in monthly_project_stats:
            monthly_project_data.append({
                "month": month if isinstance(month, str) else (month.strftime('%Y-%m') if month else None),
                "count": count
            })
        
        overview_data = {
            "profile": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "avatar_url": user.avatar_url,
                "github_url": user.github_url,
                "linkedin_url": user.linkedin_url,
                "twitter_url": user.twitter_url,
                "website_url": user.website_url
            },
            "statistics": {
                "total_projects": total_projects,
                "completed_projects": completed_projects,
                "total_skills": total_skills,
                "total_experience": total_experience,
                "total_education": total_education,
                "total_blogs": total_blogs,
                "total_contact_messages": total_contact_messages,
                "unread_messages": unread_messages
            },
            "recent_projects": recent_projects_data,
            "featured_projects": featured_projects_data,
            "skills_by_category": skills_by_category,
            "recent_blogs": recent_blogs_data,
            "monthly_project_stats": monthly_project_data
        }
        
        return jsonify(overview_data), 200
        
    except Exception as e:
        return jsonify({"error": "An error occurred while getting portfolio overview", "details": str(e)}), 500


@portfolio_bp.route('/portfolio/stats', methods=['GET'])
def get_portfolio_stats():
    """Get detailed portfolio statistics"""
    try:
        # Project statistics
        total_projects = Project.query.count()
        completed_projects = Project.query.filter_by(status=ProjectStatus.COMPLETED).count()
        in_progress_projects = Project.query.filter_by(status=ProjectStatus.IN_PROGRESS).count()
        planned_projects = Project.query.filter_by(status=ProjectStatus.PLANNED).count()
        featured_projects = Project.query.filter_by(featured=True).count()
        
        # Skill statistics
        total_skills = Skill.query.count()
        skills_by_category = db.session.query(
            Skill.category,
            func.count(Skill.id)
        ).group_by(Skill.category).all()
        
        skills_category_data = {}
        for category, count in skills_by_category:
            skills_category_data[category.value] = count
        
        # Experience statistics
        total_experience = Experience.query.count()
        current_experience = Experience.query.filter_by(current=True).count()
        
        # Education statistics
        total_education = Education.query.count()
        current_education = Education.query.filter_by(current=True).count()
        
        # Blog statistics
        total_blogs = Blog.query.count()
        published_blogs = Blog.query.filter_by(published=True).count()
        draft_blogs = Blog.query.filter_by(published=False).count()
        total_views = db.session.query(func.sum(Blog.views)).scalar() or 0
        
        # Contact statistics
        total_contacts = Contact.query.count()
        read_contacts = Contact.query.filter_by(read=True).count()
        unread_contacts = Contact.query.filter_by(read=False).count()
        
        # Monthly statistics for the last 12 months
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        
        try:
            # Try PostgreSQL/SQLite date_trunc
            monthly_project_stats = db.session.query(
                func.date_trunc('month', Project.created_at).label('month'),
                func.count(Project.id).label('count')
            ).filter(Project.created_at >= twelve_months_ago).group_by(
                func.date_trunc('month', Project.created_at)
            ).order_by(func.date_trunc('month', Project.created_at)).all()
            
            monthly_blog_stats = db.session.query(
                func.date_trunc('month', Blog.published_at).label('month'),
                func.count(Blog.id).label('count')
            ).filter(
                Blog.published == True,
                Blog.published_at >= twelve_months_ago
            ).group_by(
                func.date_trunc('month', Blog.published_at)
            ).order_by(func.date_trunc('month', Blog.published_at)).all()
            
            monthly_contact_stats = db.session.query(
                func.date_trunc('month', Contact.created_at).label('month'),
                func.count(Contact.id).label('count')
            ).filter(Contact.created_at >= twelve_months_ago).group_by(
                func.date_trunc('month', Contact.created_at)
            ).order_by(func.date_trunc('month', Contact.created_at)).all()
        except:
            # Fallback for SQLite - use strftime
            monthly_project_stats = db.session.query(
                func.strftime('%Y-%m', Project.created_at).label('month'),
                func.count(Project.id).label('count')
            ).filter(Project.created_at >= twelve_months_ago).group_by(
                func.strftime('%Y-%m', Project.created_at)
            ).order_by(func.strftime('%Y-%m', Project.created_at)).all()
            
            monthly_blog_stats = db.session.query(
                func.strftime('%Y-%m', Blog.published_at).label('month'),
                func.count(Blog.id).label('count')
            ).filter(
                Blog.published == True,
                Blog.published_at >= twelve_months_ago
            ).group_by(
                func.strftime('%Y-%m', Blog.published_at)
            ).order_by(func.strftime('%Y-%m', Blog.published_at)).all()
            
            monthly_contact_stats = db.session.query(
                func.strftime('%Y-%m', Contact.created_at).label('month'),
                func.count(Contact.id).label('count')
            ).filter(Contact.created_at >= twelve_months_ago).group_by(
                func.strftime('%Y-%m', Contact.created_at)
            ).order_by(func.strftime('%Y-%m', Contact.created_at)).all()
        
        # Convert monthly stats to dictionaries
        monthly_project_data = []
        for month, count in monthly_project_stats:
            monthly_project_data.append({
                "month": month if isinstance(month, str) else (month.strftime('%Y-%m') if month else None),
                "count": count
            })
        
        monthly_blog_data = []
        for month, count in monthly_blog_stats:
            monthly_blog_data.append({
                "month": month if isinstance(month, str) else (month.strftime('%Y-%m') if month else None),
                "count": count
            })
        
        monthly_contact_data = []
        for month, count in monthly_contact_stats:
            monthly_contact_data.append({
                "month": month if isinstance(month, str) else (month.strftime('%Y-%m') if month else None),
                "count": count
            })
        
        stats_data = {
            "projects": {
                "total": total_projects,
                "completed": completed_projects,
                "in_progress": in_progress_projects,
                "planned": planned_projects,
                "featured": featured_projects
            },
            "skills": {
                "total": total_skills,
                "by_category": skills_category_data
            },
            "experience": {
                "total": total_experience,
                "current": current_experience
            },
            "education": {
                "total": total_education,
                "current": current_education
            },
            "blogs": {
                "total": total_blogs,
                "published": published_blogs,
                "drafts": draft_blogs,
                "total_views": total_views
            },
            "contacts": {
                "total": total_contacts,
                "read": read_contacts,
                "unread": unread_contacts
            },
            "monthly_stats": {
                "projects": monthly_project_data,
                "blogs": monthly_blog_data,
                "contacts": monthly_contact_data
            }
        }
        
        return jsonify(stats_data), 200
        
    except Exception as e:
        return jsonify({"error": "An error occurred while getting portfolio statistics", "details": str(e)}), 500


@portfolio_bp.route('/portfolio/sitemap', methods=['GET'])
def get_sitemap():
    """Get sitemap data for SEO"""
    try:
        # Get all published projects
        projects = Project.query.filter_by(status=ProjectStatus.COMPLETED).all()
        project_urls = []
        for project in projects:
            project_urls.append({
                "url": f"/projects/{project.id}",
                "title": project.title,
                "last_modified": project.updated_at.isoformat() if project.updated_at else None
            })
        
        # Get all published blogs
        blogs = Blog.query.filter_by(published=True).all()
        blog_urls = []
        for blog in blogs:
            blog_urls.append({
                "url": f"/blog/{blog.slug}",
                "title": blog.title,
                "last_modified": blog.updated_at.isoformat() if blog.updated_at else None
            })
        
        # Get all skills
        skills = Skill.query.all()
        skill_urls = []
        for skill in skills:
            skill_urls.append({
                "url": f"/skills/{skill.id}",
                "title": skill.name,
                "last_modified": skill.updated_at.isoformat() if skill.updated_at else None
            })
        
        sitemap_data = {
            "static_pages": [
                {"url": "/", "title": "Home"},
                {"url": "/about", "title": "About"},
                {"url": "/projects", "title": "Projects"},
                {"url": "/skills", "title": "Skills"},
                {"url": "/experience", "title": "Experience"},
                {"url": "/education", "title": "Education"},
                {"url": "/blog", "title": "Blog"},
                {"url": "/contact", "title": "Contact"}
            ],
            "projects": project_urls,
            "blogs": blog_urls,
            "skills": skill_urls,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        return jsonify(sitemap_data), 200
        
    except Exception as e:
        return jsonify({"error": "An error occurred while getting sitemap", "details": str(e)}), 500
