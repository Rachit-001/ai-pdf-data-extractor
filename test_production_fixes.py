#!/usr/bin/env python3
"""
Test script to verify production deployment fixes
"""

import requests
import os

def test_production_fixes():
    base_url = 'http://127.0.0.1:5000'
    
    print("=== Production Deployment Fixes Test ===")
    print()
    
    # Test 1: Favicon files
    print("1. Testing favicon files...")
    try:
        r = requests.get(f'{base_url}/static/favicon.svg')
        print(f"   Favicon SVG: {r.status_code}")
        
        r2 = requests.get(f'{base_url}/static/favicon.ico')
        print(f"   Favicon ICO: {r2.status_code}")
        
        if r.status_code == 200 and r2.status_code == 200:
            print("   PASS: Favicon files accessible")
        else:
            print("   FAIL: Favicon files not accessible")
    except Exception as e:
        print(f"   ERROR: {e}")
    print()
    
    # Test 2: Examples endpoint
    print("2. Testing examples endpoint...")
    try:
        r = requests.get(f'{base_url}/examples')
        print(f"   Examples endpoint: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            examples = data.get('examples', [])
            print(f"   Found {len(examples)} examples")
            for ex in examples:
                print(f"   - {ex['display_name']}")
            print("   PASS: Examples endpoint working")
        else:
            print(f"   FAIL: Examples endpoint error: {r.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    print()
    
    # Test 3: Sample PDF files
    print("3. Testing sample PDF access...")
    try:
        r = requests.get(f'{base_url}/examples/sample_resume.pdf')
        print(f"   Sample PDF: {r.status_code}")
        
        if r.status_code == 200:
            print(f"   File size: {len(r.content)} bytes")
            print("   PASS: Sample PDF accessible")
        else:
            print(f"   FAIL: Sample PDF not accessible: {r.text}")
    except Exception as e:
        print(f"   ERROR: {e}")
    print()
    
    # Test 4: Static file serving
    print("4. Testing static file serving...")
    try:
        # Test if we can access static files directly
        r = requests.get(f'{base_url}/static/favicon.svg')
        print(f"   Static route: {r.status_code}")
        
        if r.status_code == 200:
            print("   PASS: Static file serving working")
        else:
            print("   FAIL: Static file serving not working")
    except Exception as e:
        print(f"   ERROR: {e}")
    print()
    
    print("=== Production Fixes Test Complete ===")

if __name__ == '__main__':
    test_production_fixes()
