from flask import Flask, request, render_template, jsonify, send_file, send_from_directory
import pdfplumber
import PyPDF2
import re
import json
import io
import os
import csv
import time
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
import tempfile

# Environment configuration
ENV = os.environ.get('FLASK_ENV', 'development').lower()
IS_PRODUCTION = ENV == 'production' or os.environ.get('PORT') is not None

# Configure logging based on environment
if IS_PRODUCTION:
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

logger = logging.getLogger(__name__)
logger.info(f"Starting application in {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'} mode")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DEBUG'] = not IS_PRODUCTION

# Create upload directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ensure static directories exist for production
static_dir = os.path.join(os.path.dirname(__file__), 'static')
examples_dir = os.path.join(static_dir, 'examples')

if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    if not IS_PRODUCTION:
        logger.info(f"Created static directory: {static_dir}")

if not os.path.exists(examples_dir):
    os.makedirs(examples_dir)
    if not IS_PRODUCTION:
        logger.info(f"Created examples directory: {examples_dir}")

# Always ensure example PDFs are available in production
example_files_exist = any(f.endswith('.pdf') for f in os.listdir(examples_dir) if os.path.isfile(os.path.join(examples_dir, f)))

if not example_files_exist:
    # Try to copy from various possible locations
    possible_sources = [
        os.path.join(os.path.dirname(__file__), 'test_pdfs'),
        os.path.join(os.path.dirname(__file__), 'static', 'examples'),
        'test_pdfs'
    ]
    
    import shutil
    copied_files = 0
    
    for source_dir in possible_sources:
        if os.path.exists(source_dir) and source_dir != examples_dir:
            for filename in os.listdir(source_dir):
                if filename.endswith('.pdf'):
                    try:
                        shutil.copy2(os.path.join(source_dir, filename), 
                                   os.path.join(examples_dir, filename))
                        copied_files += 1
                        if not IS_PRODUCTION:
                            logger.info(f"Copied example PDF: {filename}")
                    except Exception as e:
                        if not IS_PRODUCTION:
                            logger.warning(f"Failed to copy {filename}: {e}")
            if copied_files > 0:
                break
    
    # If no files found, create minimal example PDFs programmatically
    if copied_files == 0 and IS_PRODUCTION:
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            # Create a simple sample resume PDF
            sample_path = os.path.join(examples_dir, 'sample_resume.pdf')
            c = canvas.Canvas(sample_path, pagesize=letter)
            c.drawString(100, 750, "JOHN DOE")
            c.drawString(100, 730, "Software Engineer")
            c.drawString(100, 700, "Email: john.doe@email.com")
            c.drawString(100, 680, "Phone: (555) 123-4567")
            c.drawString(100, 660, "Address: 123 Main St, City, ST 12345")
            c.save()
            
            print("Created sample PDF for production")
        except ImportError:
            print("ReportLab not available - example PDFs may be missing")

# Add static file serving route for production
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, filename)

class PDFDataExtractor:
    def __init__(self):
        # Enhanced regex patterns for better extraction
        self.patterns = {
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}'
            ],
            'phone': [
                r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
                r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
                r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
                r'\+\d{1,3}\s?\d{3,4}\s?\d{3,4}\s?\d{3,4}'
            ],
            'address': [
                r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl|Way|Circle|Cir)(?:\s+[A-Za-z0-9\s,.-]*)?',
                r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl|Way|Circle|Cir)',
                r'P\.?O\.?\s+Box\s+\d+',
                r'\d+\s+[A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}'
            ]
        }
        
        # Common name prefixes and suffixes
        self.name_prefixes = {'mr', 'mrs', 'ms', 'dr', 'prof', 'sir', 'madam'}
        self.name_suffixes = {'jr', 'sr', 'ii', 'iii', 'iv', 'phd', 'md', 'esq'}
        
        # Words to exclude from names
        self.name_exclusions = {
            'resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary', 'objective',
            'experience', 'education', 'skills', 'references', 'contact', 'information',
            'phone', 'email', 'address', 'linkedin', 'github', 'portfolio', 'website'
        }
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using pdfplumber for better accuracy"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Fallback to PyPDF2 if pdfplumber fails
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                print(f"Error extracting text: {e2}")
        return text
    
    def clean_and_validate_email(self, email):
        """Clean and validate email addresses"""
        email = re.sub(r'\s+', '', email)  # Remove spaces
        if '@' in email and '.' in email.split('@')[1]:
            return email.lower()
        return None
    
    def clean_and_validate_phone(self, phone):
        """Clean and validate phone numbers"""
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Must have at least 10 digits
        digits_only = re.sub(r'[^\d]', '', cleaned)
        if len(digits_only) >= 10:
            return phone.strip()
        return None
    
    def clean_and_validate_address(self, address):
        """Clean and validate addresses"""
        address = address.strip()
        
        # Remove common noise patterns
        address = re.sub(r'\n[A-Z\s]+$', '', address)  # Remove trailing headers
        address = re.sub(r'^[A-Z\s]+\n', '', address)  # Remove leading headers
        address = re.sub(r'\n+', ' ', address)  # Replace newlines with spaces
        address = address.strip()
        
        # Must have at least a number and some text, and reasonable length
        if (len(address) > 10 and len(address) < 200 and 
            any(char.isdigit() for char in address) and
            not address.isdigit()):  # Not just a number
            return address
        return None
    
    def extract_names(self, text):
        """Extract multiple potential names using enhanced heuristics"""
        lines = text.split('\n')
        potential_names = []
        
        # Look for name patterns throughout the document
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 3:
                continue
                
            # Skip lines with exclusion words (but allow some context)
            exclusion_count = sum(1 for exclusion in self.name_exclusions if exclusion in line.lower())
            if exclusion_count > 1:  # Allow single exclusion words in context
                continue
                
            # Handle lines with emails differently - extract names before email
            if '@' in line:
                # Try to extract names from the beginning of the line before the email
                parts = line.split()
                potential_name_parts = []
                
                for part in parts:
                    if '@' in part:  # Stop when we hit the email
                        break
                    # Check if this part looks like a name component
                    clean_part = re.sub(r'[^\w]', '', part)
                    if (len(clean_part) > 1 and 
                        clean_part[0].isupper() and 
                        clean_part[1:].islower() and 
                        clean_part.isalpha()):
                        potential_name_parts.append(clean_part)
                    else:
                        # Stop at first non-name part (like department)
                        break
                
                # Limit to first 2 parts for proper names (First Last)
                if len(potential_name_parts) > 2:
                    potential_name_parts = potential_name_parts[:2]
                
                # If we found 2+ name parts, consider it a name
                if len(potential_name_parts) >= 2:
                    name = ' '.join(potential_name_parts)
                    if name not in potential_names and len(name) <= 50:
                        potential_names.append(name)
                continue
                
            # Special handling for tabular data - look for name-like patterns
            # Handle table rows with multiple fields (Name Department Email Phone Office)
            if (re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+\s+\w+\s+[\w@.-]+@[\w.-]+\s+\(\d{3}\)', line) or
                re.search(r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\s+[\w@.-]+@', line)):
                # Extract first two words as potential name
                parts = line.split()
                if len(parts) >= 2:
                    first_word = parts[0].strip()
                    second_word = parts[1].strip()
                    
                    # Check if they look like names (capitalized, alphabetic)
                    if (len(first_word) > 1 and len(second_word) > 1 and
                        first_word[0].isupper() and first_word[1:].islower() and
                        second_word[0].isupper() and second_word[1:].islower() and
                        first_word.isalpha() and second_word.isalpha()):
                        name = f"{first_word} {second_word}"
                        if name not in potential_names:
                            potential_names.append(name)
                continue
            
            words = line.split()
            
            # Look for 2-4 capitalized words that could be names
            if 2 <= len(words) <= 6:  # Increased range for table data
                # Check if first few words are properly capitalized names
                valid_words = []
                for j, word in enumerate(words[:4]):  # Only check first 4 words
                    # Remove common punctuation
                    clean_word = re.sub(r'[^\w]', '', word)
                    if (len(clean_word) > 1 and 
                        clean_word[0].isupper() and 
                        clean_word[1:].islower() and 
                        clean_word.isalpha()):
                        valid_words.append(clean_word)
                    else:
                        break  # Stop at first non-name word
                
                # If we have 2+ valid name words, consider it a potential name
                if len(valid_words) >= 2:
                    name = ' '.join(valid_words)
                    if name not in potential_names and len(name) <= 50:
                        potential_names.append(name)
        
        return potential_names
    
    def extract_multiple_values(self, text, field_type):
        """Extract multiple instances of a field type"""
        all_matches = []
        
        if field_type not in self.patterns:
            return []
            
        patterns = self.patterns[field_type]
        if not isinstance(patterns, list):
            patterns = [patterns]
            
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            all_matches.extend(matches)
        
        # Clean and validate matches
        cleaned_matches = []
        for match in all_matches:
            if field_type == 'email':
                cleaned = self.clean_and_validate_email(match)
            elif field_type == 'phone':
                cleaned = self.clean_and_validate_phone(match)
            elif field_type == 'address':
                cleaned = self.clean_and_validate_address(match)
            else:
                cleaned = match.strip() if match else None
                
            if cleaned and cleaned not in cleaned_matches:
                cleaned_matches.append(cleaned)
        
        return cleaned_matches
    
    def extract_structured_data(self, text):
        """Extract structured data from PDF text with multiple instances"""
        extracted_data = {
            'names': [],
            'emails': [],
            'phones': [],
            'addresses': []
        }
        
        # Extract multiple names
        extracted_data['names'] = self.extract_names(text)
        
        # Extract multiple emails
        extracted_data['emails'] = self.extract_multiple_values(text, 'email')
        
        # Extract multiple phone numbers
        extracted_data['phones'] = self.extract_multiple_values(text, 'phone')
        
        # Extract multiple addresses
        extracted_data['addresses'] = self.extract_multiple_values(text, 'address')
        
        return extracted_data

extractor = PDFDataExtractor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/examples')
def list_examples():
    """List available example PDF files"""
    examples_dir = os.path.join(os.path.dirname(__file__), 'static', 'examples')
    examples = []
    
    if not os.path.exists(examples_dir):
        logger.warning(f"Examples directory not found: {examples_dir}")
        return jsonify({'examples': []})
    
    for filename in os.listdir(examples_dir):
        if filename.lower().endswith('.pdf'):
            examples.append({
                'name': filename,
                'display_name': filename.replace('_', ' ').replace('.pdf', '').title(),
                'url': f'/examples/{filename}'
            })
    
    logger.info(f"Found {len(examples)} example files in {examples_dir}")
    return jsonify({'examples': examples})

@app.route('/examples/<filename>')
def serve_example(filename):
    """Serve example PDF files"""
    try:
        examples_dir = os.path.join(os.path.dirname(__file__), 'static', 'examples')
        filepath = os.path.join(examples_dir, filename)
        
        if not os.path.exists(filepath):
            logger.error(f"Example file not found: {filepath}")
            return jsonify({'error': 'File not found'}), 404
            
        return send_from_directory(examples_dir, filename)
    except Exception as e:
        logger.error(f"Error serving example file {filename}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/preview/<filename>')
def preview_example(filename):
    """Get text preview of example PDF files"""
    try:
        examples_dir = os.path.join(os.path.dirname(__file__), 'static', 'examples')
        filepath = os.path.join(examples_dir, filename)
        
        if not os.path.exists(filepath):
            logger.error(f"Preview file not found: {filepath}")
            return jsonify({'error': 'File not found'}), 404
        
        # Extract text from PDF for preview
        text = extractor.extract_text_from_pdf(filepath)
        
        # Limit preview to first 500 characters
        preview_text = text[:500] + '...' if len(text) > 500 else text
        
        return jsonify({
            'success': True,
            'preview': preview_text,
            'filename': filename
        })
    except Exception as e:
        logger.error(f"Error previewing file {filename}: {str(e)}")
        return jsonify({'error': 'Preview not available'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Enhanced security validation
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
    
    # Check file size (16MB limit)
    if file.content_length and file.content_length > 16 * 1024 * 1024:
        return jsonify({'error': 'File size exceeds 16MB limit.'}), 400
    
    # Validate file content by reading first few bytes (PDF magic number)
    file.seek(0)
    file_header = file.read(4)
    file.seek(0)  # Reset file pointer
    
    if file_header != b'%PDF':
        return jsonify({'error': 'Invalid PDF file. File may be corrupted or not a valid PDF.'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        
        # Additional filename validation
        if not filename or filename == '.pdf':
            filename = f"upload_{int(time.time())}.pdf"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            start_time = time.time()
            
            # Extract text from PDF
            text = extractor.extract_text_from_pdf(filepath)
            
            # Extract structured data
            extracted_data = extractor.extract_structured_data(text)
            
            # Log extraction metrics
            processing_time = time.time() - start_time
            total_fields = sum(len(values) if isinstance(values, list) else 1 for values in extracted_data.values())
            
            logger.info(f"PDF processed: {filename}, Fields extracted: {total_fields}, Time: {processing_time:.2f}s")
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'data': extracted_data,
                'raw_text': text[:500] + '...' if len(text) > 500 else text,
                'processing_time': round(processing_time, 2),
                'total_fields_extracted': total_fields
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400

@app.route('/export/json', methods=['POST'])
def export_json():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Create JSON file in memory
    json_data = json.dumps(data, indent=2)
    
    # Create a file-like object
    json_file = io.BytesIO()
    json_file.write(json_data.encode('utf-8'))
    json_file.seek(0)
    
    return send_file(
        json_file,
        as_attachment=True,
        download_name='extracted_data.json',
        mimetype='application/json'
    )

@app.route('/export/csv', methods=['POST'])
def export_csv():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Create CSV in memory with proper handling
    output = io.StringIO()
    csv_writer = csv.writer(output)
    
    # Get all field types and find the maximum number of entries
    field_types = ['names', 'emails', 'phones', 'addresses']
    max_length = max(len(data.get(field, [])) for field in field_types) if any(data.get(field, []) for field in field_types) else 0
    
    # Write headers (column-wise for better usability)
    headers = ['Names', 'Email Addresses', 'Phone Numbers', 'Addresses']
    csv_writer.writerow(headers)
    
    # Write data in columns (each row contains one item from each category)
    for i in range(max_length):
        row = []
        for field in field_types:
            values = data.get(field, [])
            if i < len(values):
                row.append(values[i])
            else:
                row.append('')  # Empty cell if no more data in this category
        csv_writer.writerow(row)
    
    # Convert to bytes
    csv_content = output.getvalue()
    csv_bytes = io.BytesIO(csv_content.encode('utf-8'))
    csv_bytes.seek(0)
    
    return send_file(
        csv_bytes,
        as_attachment=True,
        download_name='extracted_data.csv',
        mimetype='text/csv'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    if IS_PRODUCTION:
        # Production mode: Use WSGI server
        try:
            from waitress import serve
            print(f"Starting production server on port {port}")
            serve(app, host='0.0.0.0', port=port)
        except ImportError:
            logger.error("Waitress not available for production deployment!")
            app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development mode: Use Flask dev server with debug
        logger.info(f"Starting development server on port {port}")
        logger.info("Debug mode enabled - code changes will auto-reload")
        app.run(host='0.0.0.0', port=port, debug=True)
