#!/usr/bin/env python3
"""
Initialize database with tables and seed data
"""
import os
import sys
from datetime import datetime, date
from werkzeug.security import generate_password_hash

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from extensions import db
from models import User, Skill, Project, Experience, Education, Contact, Blog, Image, ProjectStatus, CategoryStatus

def init_database():
    """Initialize database with tables and seed data"""
    print("🗄️  Initializing database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Tables created successfully")
            
            # Check if admin user already exists
            admin_exists = User.query.filter_by(is_admin=True).first()
            if admin_exists:
                print("✅ Admin user already exists")
                return
            
            # Create admin user
            admin_user = User(
                username='admin',
                email='omwansamarnold@gmail.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                first_name='Omwansa',
                last_name='Arnold',
                bio='Full-stack developer passionate about creating innovative web solutions.',
                title='Software Developer',
                location='Nairobi, Kenya',
                avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
                github_url='https://github.com/omwansa',
                linkedin_url='https://linkedin.com/in/omwansa-arnold',
                website_url='https://omwansa.dev'
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created successfully")
            
            # Create sample education data
            education_data = [
                {
                    'institution': 'University of Nairobi',
                    'degree': 'Bachelor of Science in Computer Science',
                    'field_of_study': 'Computer Science',
                    'description': 'Comprehensive study of computer science fundamentals including algorithms, data structures, software engineering, and database systems.',
                    'start_date': date(2018, 9, 1),
                    'end_date': date(2022, 6, 30),
                    'current': False,
                    'gpa': '3.8',
                    'location': 'Nairobi, Kenya'
                },
                {
                    'institution': 'Coursera',
                    'degree': 'Google Data Analytics Professional Certificate',
                    'field_of_study': 'Data Analytics',
                    'description': 'Comprehensive data analytics program covering data collection, processing, analysis, and visualization.',
                    'start_date': date(2023, 1, 15),
                    'end_date': date(2023, 6, 15),
                    'current': False,
                    'gpa': None,
                    'location': 'Online'
                }
            ]
            
            for edu_data in education_data:
                education = Education(**edu_data)
                db.session.add(education)
            
            db.session.commit()
            print("✅ Sample education data created")
            
            # Create sample projects
            project_data = [
                {
                    'title': 'Portfolio Website',
                    'description': 'A modern, responsive portfolio website built with React and Flask.',
                    'technologies': 'React, Flask, SQLite, Tailwind CSS',
                    'github_url': 'https://github.com/omwansa/portfolio',
                    'live_url': 'https://omwansa.dev',
                    'featured': True,
                    'status': ProjectStatus.ACTIVE,
                    'start_date': date(2024, 1, 1),
                    'end_date': None
                }
            ]
            
            for proj_data in project_data:
                project = Project(**proj_data)
                db.session.add(project)
            
            db.session.commit()
            print("✅ Sample project data created")
            
            print("🎉 Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during database initialization: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    init_database()
