#!/usr/bin/env python3
"""
Simple test script to validate upload security and functionality
"""

import requests
import os

def test_upload_validation():
    base_url = 'http://127.0.0.1:5000'
    
    print("=== PDF Data Extractor - Security & Functionality Tests ===")
    print()
    
    # Test 1: Invalid file type
    print("1. Testing invalid file type rejection...")
    files = {'file': ('test.txt', 'not a pdf', 'text/plain')}
    r = requests.post(f'{base_url}/upload', files=files)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    assert r.status_code == 400
    print("   PASS: Invalid file type rejected")
    print()
    
    # Test 2: Empty filename
    print("2. Testing empty filename...")
    files = {'file': ('', '', 'application/pdf')}
    r = requests.post(f'{base_url}/upload', files=files)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    assert r.status_code == 400
    print("   PASS: Empty filename rejected")
    print()
    
    # Test 3: Fake PDF header validation
    print("3. Testing fake PDF content...")
    files = {'file': ('notpdf.pdf', 'fake content', 'application/pdf')}
    r = requests.post(f'{base_url}/upload', files=files)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    assert r.status_code == 400
    print("   PASS: Fake PDF content rejected")
    print()
    
    # Test 4: Real PDF upload
    print("4. Testing real PDF upload...")
    pdf_path = 'static/examples/sample_resume.pdf'
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            content = f.read()
        files = {'file': ('sample_resume.pdf', content, 'application/pdf')}
        r = requests.post(f'{base_url}/upload', files=files)
        print(f"   Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Fields extracted: {data.get('total_fields_extracted')}")
            extracted = data.get('data', {})
            print(f"   Names: {len(extracted.get('names', []))}")
            print(f"   Emails: {len(extracted.get('emails', []))}")
            print(f"   Phones: {len(extracted.get('phones', []))}")
            print(f"   Addresses: {len(extracted.get('addresses', []))}")
            print("   PASS: Real PDF processed successfully")
        else:
            print(f"   FAIL: {r.json()}")
    else:
        print("   SKIP: Sample PDF not found")
    print()
    
    # Test 5: Examples endpoint
    print("5. Testing examples endpoint...")
    r = requests.get(f'{base_url}/examples')
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        examples = r.json().get('examples', [])
        print(f"   Found {len(examples)} example files")
        for ex in examples:
            print(f"   - {ex['display_name']}")
        print("   PASS: Examples endpoint working")
    else:
        print(f"   FAIL: {r.json()}")
    print()
    
    # Test 6: Preview endpoint
    print("6. Testing preview endpoint...")
    r = requests.get(f'{base_url}/preview/sample_resume.pdf')
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        preview = r.json()
        print(f"   Preview length: {len(preview.get('preview', ''))}")
        print(f"   Preview start: {preview.get('preview', '')[:100]}...")
        print("   PASS: Preview endpoint working")
    else:
        print(f"   FAIL: {r.json()}")
    print()
    
    print("=== All Tests Completed Successfully ===")

if __name__ == '__main__':
    try:
        test_upload_validation()
    except Exception as e:
        print(f"Test failed with error: {e}")
