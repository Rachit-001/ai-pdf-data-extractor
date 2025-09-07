import requests
import json

# Test CSV export functionality
def test_csv_export():
    url = 'http://127.0.0.1:5000/export/csv'
    
    # Sample data structure
    test_data = {
        "names": ["John Doe", "Jane Smith", "Bob Johnson"],
        "emails": ["john@email.com", "jane@email.com", "bob@email.com", "extra@email.com"],
        "phones": ["(555) 123-4567", "(555) 987-6543"],
        "addresses": ["123 Main St", "456 Oak Ave", "789 Pine Rd", "321 Elm St", "654 Maple Dr"]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        
        if response.status_code == 200:
            # Save the CSV content to a file to inspect
            with open('test_output.csv', 'wb') as f:
                f.write(response.content)
            
            print("CSV export successful!")
            print("Saved to test_output.csv")
            
            # Also print the content
            csv_content = response.content.decode('utf-8')
            print("\nCSV Content:")
            print("-" * 50)
            print(csv_content)
            print("-" * 50)
            
        else:
            print(f"CSV export failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error testing CSV export: {e}")

if __name__ == "__main__":
    test_csv_export()
