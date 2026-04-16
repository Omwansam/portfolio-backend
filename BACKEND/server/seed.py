#!/usr/bin/env python3
"""
Seed file for Omwansa Portfolio Database
This script will:
1. Delete all existing data
2. Recreate database tables
3. Populate with initial data
"""

import os
import sys
import json
from datetime import datetime, date
from werkzeug.security import generate_password_hash

# Make imports robust whether run as a module or a script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

try:
    # When executed as a script (python server/seed.py)
    from server.app import app
    from server.extensions import db
    from server.models import (
        User, Skill, Project, Experience, Education, Contact, Blog, Image,
        ProjectStatus, CategoryStatus
    )
except ImportError:
    # When executed as a module (python -m server.seed)
    from .app import app
    from .extensions import db
    from .models import (
        User, Skill, Project, Experience, Education, Contact, Blog, Image,
        ProjectStatus, CategoryStatus
    )

def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing existing data...")
    
    # Drop all tables
    db.drop_all()
    print("   ✅ All tables dropped")
    
    # Create all tables
    db.create_all()
    print("   ✅ All tables recreated")

def create_users():
    """Create initial users"""
    print("👤 Creating users...")
    
    # Admin user
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True,
        first_name='Omwansa',
        last_name='Arnold',
        bio='Full-stack developer passionate about creating innovative web solutions. I specialize in React, Node.js, and modern web technologies.',
        avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
        github_url='https://github.com/omwansa',
        linkedin_url='https://linkedin.com/in/omwansa-arnold',
        twitter_url='https://twitter.com/omwansa_arnold',
        website_url='https://omwansa.dev'
    )
    
    db.session.add(admin_user)
    db.session.commit()
    
    print(f"   ✅ Created admin user: {admin_user.username}")
    print(f"   📧 Email: {admin_user.email}")
    print(f"   🔑 Password: admin123")
    
    return admin_user


def create_skills():
    """Create initial skills from frontend data patterns"""
    print("🛠️  Creating skills...")

    skills_payload = [
        {"name": "React", "category": CategoryStatus.FRAMEWORK, "proficiency_level": "95", "icon_url": ""},
        {"name": "Node.js", "category": CategoryStatus.TOOL, "proficiency_level": "90", "icon_url": ""},
        {"name": "TypeScript", "category": CategoryStatus.LANGUAGE, "proficiency_level": "85", "icon_url": ""},
        {"name": "Python", "category": CategoryStatus.LANGUAGE, "proficiency_level": "80", "icon_url": ""},
        {"name": "Tailwind CSS", "category": CategoryStatus.TOOL, "proficiency_level": "88", "icon_url": ""},
        {"name": "PostgreSQL", "category": CategoryStatus.TOOL, "proficiency_level": "78", "icon_url": ""},
    ]

    created = []
    for payload in skills_payload:
        skill = Skill(**payload)
        db.session.add(skill)
        created.append(skill)
    db.session.commit()
    print(f"   ✅ Created {len(created)} skills")
    return created


def create_projects():
    """Create initial projects based on frontend mocks"""
    print("📦 Creating projects...")

    projects_payload = [
        {
            "title": "E-Commerce Platform",
            "description": "A comprehensive e-commerce solution with advanced features",
            "short_description": "Full-featured shop with payments",
            "image_url": "",
            "github_url": "",
            "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
            "technologies": '["Next.js","Node.js","PostgreSQL","Stripe"]',
        },
        {
            "title": "Restaurant Management System",
            "description": "Complete POS and restaurant management solution",
            "short_description": "POS + inventory + orders",
            "image_url": "",
            "github_url": "",
            "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": False,
            "technologies": '["React","Node.js","MongoDB","Socket.io"]',
        },
        {
            "title": "Task Management App",
            "description": "Mobile-first task management application",
            "short_description": "Tasks with realtime sync",
            "image_url": "",
            "github_url": "",
            "live_url": "",
            "status": ProjectStatus.IN_PROGRESS,
            "featured": False,
            "technologies": '["React Native","Firebase","Redux"]',
        },
    ]

    created = []
    for payload in projects_payload:
        # ensure technologies are JSON strings as expected by model
        techs = payload.get("technologies")
        if isinstance(techs, (list, tuple)):
            payload["technologies"] = json.dumps(list(techs))
        project = Project(**payload)
        db.session.add(project)
        created.append(project)
    db.session.commit()
    print(f"   ✅ Created {len(created)} projects")
    return created


def create_experiences(admin_user: User):
    """Create initial work experiences"""
    print("🧑‍💼 Creating experiences...")

    exp_payload = [
        {
            "company": "Tech Solutions Inc.",
            "position": "Senior Full Stack Developer",
            "location": "Nairobi, Kenya",
            "start_date": date(2022, 1, 1),
            "end_date": None,
            "current": True,
            "description": (
                "Led development of scalable web applications using React, Node.js, and cloud technologies. "
                "Mentored junior developers and implemented best practices."
            ),
        },
        {
            "company": "Digital Agency Pro",
            "position": "Full Stack Developer",
            "location": "Remote",
            "start_date": date(2020, 6, 1),
            "end_date": date(2021, 12, 31),
            "current": False,
            "description": (
                "Built responsive web applications and RESTful APIs for various clients. "
                "Collaborated with design teams to implement pixel-perfect UIs."
            ),
        },
    ]

    created = []
    for payload in exp_payload:
        exp = Experience(**payload)
        db.session.add(exp)
        created.append(exp)
    db.session.commit()
    print(f"   ✅ Created {len(created)} experiences")
    return created


def create_education(admin_user: User):
    """Create initial education records"""
    print("🎓 Creating education...")

    edu_payload = [
        {
            "institution": "University of Nairobi",
            "degree": "Bachelor of Science in Computer Science",
            "field_of_study": "Computer Science",
            "location": "Nairobi, Kenya",
            "start_date": date(2016, 9, 1),
            "end_date": date(2020, 6, 30),
            "gpa": 3.8,
            "description": (
                "Focused on software engineering, algorithms, and data structures. "
                "Achievements: Graduated Magna Cum Laude; Dean's List (3 years); "
                "President of CS Club; Best Final Year Project. "
                "Coursework: Data Structures, Algorithms, Database Systems, Software Engineering, Web Development."
            ),
        },
        {
            "institution": "FreeCodeCamp",
            "degree": "Full Stack Web Development Certification",
            "field_of_study": "Web Development",
            "location": "Online",
            "start_date": date(2019, 1, 1),
            "end_date": date(2019, 12, 31),
            "gpa": 0.0,
            "description": (
                "Comprehensive program covering front-end and back-end web development technologies. "
                "Coursework: HTML/CSS, JavaScript, React, Node.js, MongoDB, Git."
            ),
        },
    ]

    created = []
    for payload in edu_payload:
        edu = Education(**payload)
        db.session.add(edu)
        created.append(edu)
    db.session.commit()
    print(f"   ✅ Created {len(created)} education records")
    return created


def create_blog_posts(admin_user: User):
    """Create initial blog posts matching the frontend demo"""
    print("📝 Creating blog posts...")

    posts_payload = [
        {
            "title": "Building Scalable React Applications",
            "slug": "building-scalable-react-applications",
            "excerpt": "Learn how to structure and organize your React applications for scalability and maintainability.",
            "content": "Full blog post content here...",
            "tags": json.dumps(["React", "JavaScript", "Architecture"]),
            "published": True,
            "published_at": datetime(2024, 1, 25, 10, 0, 0),
            "views": 1250,
            "author_id": admin_user.id,
        },
        {
            "title": "Modern CSS Techniques for Better UX",
            "slug": "modern-css-techniques-better-ux",
            "excerpt": "Explore advanced CSS techniques that can significantly improve user experience and performance.",
            "content": "Full blog post content here...",
            "tags": json.dumps(["CSS", "UX", "Performance"]),
            "published": True,
            "published_at": datetime(2024, 1, 20, 14, 0, 0),
            "views": 890,
            "author_id": admin_user.id,
        },
        {
            "title": "Node.js Best Practices for Production",
            "slug": "nodejs-best-practices-production",
            "excerpt": "Essential practices and patterns for deploying Node.js applications in production environments.",
            "content": "Full blog post content here...",
            "tags": json.dumps(["Node.js", "Backend", "Production"]),
            "published": False,
            "views": 0,
            "author_id": admin_user.id,
        },
    ]

    created = []
    for payload in posts_payload:
        post = Blog(**payload)
        db.session.add(post)
        created.append(post)
    db.session.commit()
    print(f"   ✅ Created {len(created)} blog posts")
    return created


def create_contacts():
    """Create mock contact messages"""
    print("✉️  Creating contact messages...")

    contacts_payload = [
        {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "subject": "Project Inquiry",
            "message": "Hello, I'm interested in discussing a new web project. Could we schedule a call this week?",
            "read": False,
        },
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "subject": "Speaking Engagement",
            "message": "We'd love to invite you to speak at our tech meetup next month about React architecture.",
            "read": True,
        },
        {
            "name": "Acme Corp",
            "email": "hr@acmecorp.com",
            "subject": "Job Opportunity",
            "message": "We reviewed your portfolio and would like to discuss a Senior Full Stack role at Acme Corp.",
            "read": False,
        },
    ]

    created = []
    for payload in contacts_payload:
        contact = Contact(**payload)
        db.session.add(contact)
        created.append(contact)
    db.session.commit()
    print(f"   ✅ Created {len(created)} contact messages")
    return created

def main():
    """Main function to run the seed script"""
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Clear existing data
            clear_database()
            
            # Create users
            admin_user = create_users()

            # Portfolio data
            create_skills()
            create_projects()
            create_experiences(admin_user)
            create_education(admin_user)
            create_blog_posts(admin_user)
            create_contacts()
            
            print("=" * 50)
            print("✅ Database seeding completed successfully!")
            print(f"🎯 Admin credentials:")
            print(f"   Email: admin@example.com")
            print(f"   Password: admin123")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()
