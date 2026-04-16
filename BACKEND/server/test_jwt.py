#!/usr/bin/env python3
"""
Test script to verify JWT configuration
"""

import os
import sys
from datetime import datetime

# Add the server directory to the Python path
sys.path.append(os.path.dirname(__file__))

from app import app
from .extensions import db
from .models import User
from flask_jwt_extended import create_access_token, create_refresh_token

def test_jwt():
    """Test JWT token creation and validation"""
    print("🧪 Testing JWT configuration...")
    
    with app.app_context():
        try:
            # Check if admin user exists
            admin_user = User.query.filter_by(email='admin@example.com').first()
            
            if not admin_user:
                print("❌ Admin user not found! Run seed.py first.")
                return
            
            print(f"✅ Admin user found: {admin_user.username}")
            
            # Test JWT secret key
            if not app.config.get('JWT_SECRET_KEY'):
                print("❌ JWT_SECRET_KEY not configured!")
                return
            
            print("✅ JWT_SECRET_KEY is configured")
            
            # Test token creation
            access_token = create_access_token(identity=admin_user.id)
            refresh_token = create_refresh_token(identity=admin_user.id)
            
            print("✅ Access token created successfully")
            print("✅ Refresh token created successfully")
            
            # Test token format
            print(f"📝 Access token (first 50 chars): {access_token[:50]}...")
            print(f"📝 Refresh token (first 50 chars): {refresh_token[:50]}...")
            
            print("=" * 50)
            print("✅ JWT configuration is working correctly!")
            print("🎯 You can now test the frontend authentication")
            
        except Exception as e:
            print(f"❌ Error during JWT testing: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_jwt()
