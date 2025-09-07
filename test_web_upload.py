#!/usr/bin/env python3
"""
Test the web upload functionality to see what data is returned.
"""

import requests
import json

def test_web_upload():
    """Test uploading a PDF via the web interface"""
    url = "http://127.0.0.1:5000/upload"
    
    # Upload the mixed format document
    with open("test_pdfs/mixed_format_document.pdf", "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    print("Response Status Code:", response.status_code)
    print("Response Headers:", dict(response.headers))
    print("\nResponse Data:")
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if data.get('success') and 'data' in data:
            extracted = data['data']
            print(f"\nExtracted Data Structure:")
            for field, values in extracted.items():
                print(f"{field}: {type(values)} with {len(values) if isinstance(values, list) else 'N/A'} items")
                if isinstance(values, list):
                    for i, value in enumerate(values[:3]):  # Show first 3
                        print(f"  [{i}]: {value}")
                    if len(values) > 3:
                        print(f"  ... and {len(values) - 3} more")
                else:
                    print(f"  Value: {values}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response:", response.text)

if __name__ == "__main__":
    test_web_upload()
