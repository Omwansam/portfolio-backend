from .extensions import db
from enum import Enum
from datetime import datetime


class ProjectStatus(Enum):
    COMPLETED = 'completed'
    IN_PROGRESS = 'in-progress'
    PLANNED = 'planned'

class CategoryStatus(Enum):
    LANGUAGE = 'language'
    FRAMEWORK = 'framework'
    TOOL = 'tool'
    DESIGN = 'design'
    OTHER = 'other'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    whatsapp_url = db.Column(db.String(255))
    email_url = db.Column(db.String(255))
    hero_image_url = db.Column(db.String(255))
    about_image_url = db.Column(db.String(255))
    cv_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(CategoryStatus, name='skill_status'), default=CategoryStatus.LANGUAGE, nullable=False)
    proficiency_level = db.Column(db.String(50), nullable=False)
    icon_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Skill {self.name}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    image_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    live_url = db.Column(db.String(255))
    status = db.Column(db.Enum(ProjectStatus, name='project_status'), default=ProjectStatus.COMPLETED, nullable=False)
    featured = db.Column(db.Boolean, default=False)
    technologies = db.Column(db.Text)  # JSON string of technology IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    company_logo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Experience {self.position} at {self.company}>'


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    current = db.Column(db.Boolean, default=False)
    gpa = db.Column(db.Float)
    location = db.Column(db.String(100))
    institution_logo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Education {self.degree} from {self.institution}>'


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact from {self.name}>'


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    featured_image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    tags = db.Column(db.Text)  # JSON string of tags
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User', backref='blogs')

    def __repr__(self):
        return f'<Blog {self.title}>'


class Image(db.Model):
    """Model for storing image metadata"""
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    image_type = db.Column(db.String(50), nullable=False)  # 'hero', 'about', 'avatar', 'project', 'blog', etc.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='images')
    project = db.relationship('Project', backref='images')
    blog = db.relationship('Blog', backref='images')

    def __repr__(self):
        return f'<Image {self.filename}>'