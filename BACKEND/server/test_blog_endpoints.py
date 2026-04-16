#!/usr/bin/env python3
"""
Test script to verify blog endpoints work correctly
"""

import requests
import json

def test_blog_endpoints():
    """Test the blog endpoints"""
    base_url = 'http://localhost:5000/api'
    
    try:
        # Test 1: Get all blog posts (including drafts for admin)
        print("Testing GET /blog with published=all...")
        response = requests.get(f'{base_url}/blog?published=all')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Blog posts endpoint working!")
            print(f"Response structure: {list(data.keys())}")
            if 'blogs' in data:
                print(f"Number of blog posts: {len(data['blogs'])}")
                if data['blogs']:
                    print(f"Sample blog post: {json.dumps(data['blogs'][0], indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
        # Test 2: Get only published blog posts
        print("\nTesting GET /blog with published=true...")
        response = requests.get(f'{base_url}/blog?published=true')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Published blog posts endpoint working!")
            if 'blogs' in data:
                print(f"Number of published posts: {len(data['blogs'])}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
        # Test 3: Get only draft blog posts
        print("\nTesting GET /blog with published=false...")
        response = requests.get(f'{base_url}/blog?published=false')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Draft blog posts endpoint working!")
            if 'blogs' in data:
                print(f"Number of draft posts: {len(data['blogs'])}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on port 5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_blog_endpoints()
