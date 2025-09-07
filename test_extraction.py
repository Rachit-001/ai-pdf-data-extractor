#!/usr/bin/env python3
"""
Test the enhanced PDF data extractor with the mixed format document.
"""

import sys
import os
sys.path.append('.')

from app import PDFDataExtractor
import json

def test_extraction():
    """Test the PDF extraction on mixed_format_document.pdf"""
    extractor = PDFDataExtractor()
    
    # Path to the test PDF
    pdf_path = "test_pdfs/mixed_format_document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        return
    
    print("Testing PDF Data Extraction...")
    print(f"Processing: {pdf_path}")
    print("-" * 50)
    
    try:
        # Extract text from PDF
        text = extractor.extract_text_from_pdf(pdf_path)
        print("Extracted Text Preview:")
        print(text[:500] + "..." if len(text) > 500 else text)
        print("-" * 50)
        
        # Extract structured data
        extracted_data = extractor.extract_structured_data(text)
        
        # Display results
        print("EXTRACTION RESULTS:")
        print("=" * 50)
        
        print(f"Names Found ({len(extracted_data['names'])}):")
        for i, name in enumerate(extracted_data['names'], 1):
            print(f"  {i}. {name}")
        
        print(f"\nEmails Found ({len(extracted_data['emails'])}):")
        for i, email in enumerate(extracted_data['emails'], 1):
            print(f"  {i}. {email}")
        
        print(f"\nPhones Found ({len(extracted_data['phones'])}):")
        for i, phone in enumerate(extracted_data['phones'], 1):
            print(f"  {i}. {phone}")
        
        print(f"\nAddresses Found ({len(extracted_data['addresses'])}):")
        for i, address in enumerate(extracted_data['addresses'], 1):
            print(f"  {i}. {address}")
        
        print("\n" + "=" * 50)
        print("JSON OUTPUT:")
        print(json.dumps(extracted_data, indent=2))
        
        return extracted_data
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

if __name__ == "__main__":
    test_extraction()
