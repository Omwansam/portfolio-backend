#!/usr/bin/env python3
"""
Projects Seed File (server-local)
Adds 10 additional projects to the database without clearing other data.
Skips duplicates based on exact project title match.
"""

import os
import sys
import json
from datetime import datetime

# Make imports robust whether run as a module or a script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

try:
    # When executed as a script (python server/seed_projects.py)
    from server.app import app
    from server.extensions import db
    from server.models import Project, ProjectStatus
except ImportError:
    # When executed as a module (python -m server.seed_projects)
    from .app import app
    from .extensions import db
    from .models import Project, ProjectStatus


def upsert_project(payload: dict) -> Project:
    """Insert project if title not existing; otherwise skip and return existing."""
    existing = Project.query.filter_by(title=payload.get("title")).first()
    if existing:
        return existing

    # Ensure technologies is JSON string per model expectation
    technologies = payload.get("technologies")
    if isinstance(technologies, (list, tuple)):
        payload["technologies"] = json.dumps(list(technologies))

    project = Project(**payload)
    db.session.add(project)
    return project


essential_projects = [
        {
            "title": "AI-Powered Chatbot Platform",
        "description": "An intelligent chatbot platform using ML with NLP, sentiment analysis, and multi-language support.",
        "short_description": "Smart chatbot with ML/NLP",
            "image_url": "",
            "github_url": "https://github.com/omwansa/ai-chatbot-platform",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
        "technologies": ["Python", "TensorFlow", "React", "FastAPI", "PostgreSQL", "Docker"],
        },
        {
            "title": "Mobile Banking App",
        "description": "Secure mobile banking with biometric authentication, real-time transactions, and analytics.",
        "short_description": "Secure mobile banking",
            "image_url": "",
            "github_url": "https://github.com/omwansa/mobile-banking-app",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
        "technologies": ["React Native", "Node.js", "MongoDB", "JWT", "Stripe"],
        },
        {
            "title": "Real Estate Management API",
        "description": "REST API for property listings, user management, and geospatial search with maps integration.",
        "short_description": "Property API with search",
            "image_url": "",
            "github_url": "https://github.com/omwansa/real-estate-api",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": False,
        "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        },
        {
            "title": "E-Learning Platform",
        "description": "Online learning with video streaming, quizzes, progress tracking, and payments.",
        "short_description": "Modern e-learning platform",
            "image_url": "",
            "github_url": "https://github.com/omwansa/elearning-platform",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
        "technologies": ["Next.js", "Node.js", "MongoDB", "Stripe", "WebRTC"],
        },
        {
            "title": "IoT Smart Home Dashboard",
        "description": "Real-time IoT device control, energy monitoring, and automation rules.",
        "short_description": "Smart home dashboard",
            "image_url": "",
            "github_url": "https://github.com/omwansa/iot-smart-home",
        "live_url": "",
            "status": ProjectStatus.IN_PROGRESS,
            "featured": False,
        "technologies": ["React", "Node.js", "MQTT", "WebSocket"],
        },
        {
            "title": "Blockchain Voting System",
        "description": "Transparent, immutable blockchain-based voting with audit trails.",
        "short_description": "Blockchain voting",
            "image_url": "",
            "github_url": "https://github.com/omwansa/blockchain-voting",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
        "technologies": ["Solidity", "Web3.js", "React", "Node.js"],
        },
        {
            "title": "Food Delivery Mobile App",
        "description": "Food delivery with real-time courier tracking and payments.",
        "short_description": "Food delivery app",
            "image_url": "",
            "github_url": "https://github.com/omwansa/food-delivery-app",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": False,
        "technologies": ["Flutter", "Firebase", "Google Maps", "Stripe"],
    },
    {
        "title": "ML Stock Predictor",
        "description": "AI-driven stock prediction using deep learning and technical indicators.",
        "short_description": "AI stock predictor",
            "image_url": "",
            "github_url": "https://github.com/omwansa/ml-stock-predictor",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": True,
        "technologies": ["Python", "TensorFlow", "Pandas", "Streamlit"],
        },
        {
            "title": "Social Media Analytics Dashboard",
        "description": "Sentiment analysis, engagement metrics, and content insights across platforms.",
        "short_description": "Social analytics",
            "image_url": "",
            "github_url": "https://github.com/omwansa/social-analytics",
        "live_url": "",
            "status": ProjectStatus.COMPLETED,
            "featured": False,
        "technologies": ["Vue.js", "Node.js", "MongoDB", "Chart.js"],
        },
        {
            "title": "Healthcare Management System",
        "description": "Patient records, appointments, prescriptions, and telemedicine modules.",
        "short_description": "Healthcare system",
            "image_url": "",
            "github_url": "https://github.com/omwansa/healthcare-system",
        "live_url": "",
            "status": ProjectStatus.PLANNED,
            "featured": False,
        "technologies": ["Angular", "Spring Boot", "PostgreSQL", "Docker"],
    },
    ]
    
    
def main():
    print("🌱 Seeding additional projects (10)...")
    with app.app_context():
        created_count = 0
        for payload in essential_projects:
            project_before = Project.query.filter_by(title=payload.get("title")).first()
            proj = upsert_project(payload)
            if not project_before and proj:
                created_count += 1
        try:
            db.session.commit()
            print(f"✅ Added {created_count} new projects (skipped duplicates)")
        except Exception as exc:
            db.session.rollback()
            print(f"❌ Error while adding projects: {exc}")
            raise


if __name__ == "__main__":
    main()
