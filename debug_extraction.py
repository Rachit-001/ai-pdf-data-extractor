#!/usr/bin/env python3
"""
Debug the name extraction for the mixed format document.
"""

import sys
import os
sys.path.append('.')

from app import PDFDataExtractor
import json
import re

def debug_name_extraction():
    """Debug name extraction step by step"""
    extractor = PDFDataExtractor()
    
    # Path to the test PDF
    pdf_path = "test_pdfs/mixed_format_document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        return
    
    # Extract text from PDF
    text = extractor.extract_text_from_pdf(pdf_path)
    lines = text.split('\n')
    
    print("DEBUG: Line-by-line analysis for name extraction")
    print("=" * 60)
    
    potential_names = []
    
    for i, line in enumerate(lines):
        line_orig = line
        line = line.strip()
        
        if not line or len(line) < 3:
            continue
            
        print(f"Line {i+1}: '{line}'")
        
        # Check for email patterns
        has_email = '@' in line
        print(f"  Has email: {has_email}")
        
        if has_email:
            print("  SKIPPED: Contains email")
            continue
            
        # Check exclusion words
        exclusion_count = sum(1 for exclusion in extractor.name_exclusions if exclusion in line.lower())
        print(f"  Exclusion count: {exclusion_count}")
        
        if exclusion_count > 1:
            print("  SKIPPED: Too many exclusion words")
            continue
            
        # Check for table pattern
        table_pattern1 = re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+\s+\w+\s+[\w@.-]+@[\w.-]+\s+\(\d{3}\)', line)
        table_pattern2 = re.search(r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\s+[\w@.-]+@', line)
        
        print(f"  Table pattern 1 match: {bool(table_pattern1)}")
        print(f"  Table pattern 2 match: {bool(table_pattern2)}")
        
        if table_pattern1 or table_pattern2:
            parts = line.split()
            print(f"  Line parts: {parts}")
            if len(parts) >= 2:
                first_word = parts[0].strip()
                second_word = parts[1].strip()
                print(f"  First word: '{first_word}', Second word: '{second_word}'")
                
                # Check name criteria
                valid_first = (len(first_word) > 1 and first_word[0].isupper() and 
                              first_word[1:].islower() and first_word.isalpha())
                valid_second = (len(second_word) > 1 and second_word[0].isupper() and 
                               second_word[1:].islower() and second_word.isalpha())
                
                print(f"  First word valid: {valid_first}")
                print(f"  Second word valid: {valid_second}")
                
                if valid_first and valid_second:
                    name = f"{first_word} {second_word}"
                    print(f"  EXTRACTED NAME: {name}")
                    if name not in potential_names:
                        potential_names.append(name)
            continue
            
        # Regular name pattern check
        words = line.split()
        if 2 <= len(words) <= 6:
            print(f"  Checking regular pattern with {len(words)} words: {words}")
            valid_words = []
            for j, word in enumerate(words[:4]):
                clean_word = re.sub(r'[^\w]', '', word)
                is_valid = (len(clean_word) > 1 and 
                           clean_word[0].isupper() and 
                           clean_word[1:].islower() and 
                           clean_word.isalpha())
                print(f"    Word {j+1} '{clean_word}': valid={is_valid}")
                if is_valid:
                    valid_words.append(clean_word)
                else:
                    break
                    
            if len(valid_words) >= 2:
                name = ' '.join(valid_words)
                print(f"  EXTRACTED NAME: {name}")
                if name not in potential_names and len(name) <= 50:
                    potential_names.append(name)
        
        print()
    
    print("FINAL EXTRACTED NAMES:")
    for name in potential_names:
        print(f"  - {name}")
    
    return potential_names

if __name__ == "__main__":
    debug_name_extraction()
