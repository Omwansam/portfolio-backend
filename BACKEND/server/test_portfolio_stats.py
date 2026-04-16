#!/usr/bin/env python3
"""
Test script to verify portfolio stats endpoint works correctly
"""

import requests
import json

def test_portfolio_stats():
    """Test the portfolio stats endpoint"""
    try:
        # Test the endpoint
        response = requests.get('http://localhost:5000/api/portfolio/stats')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Portfolio stats endpoint working!")
            print(f"Response data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on port 5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_portfolio_stats()
