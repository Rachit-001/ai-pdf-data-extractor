#!/usr/bin/env python3
"""
Generate example PDF files for testing the PDF data extractor.
Creates various document types with multiple instances of names, emails, phones, and addresses.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_sample_resume():
    """Create a sample resume with multiple contact methods and references"""
    filename = "sample_resume.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("SARAH JOHNSON", title_style))
    story.append(Paragraph("Senior Software Engineer", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    # Contact Information
    contact_info = """
    <b>Primary Contact:</b><br/>
    Email: sarah.johnson@email.com<br/>
    Phone: (555) 123-4567<br/>
    Address: 123 Main Street, San Francisco, CA 94102<br/>
    <br/>
    <b>Alternative Contact:</b><br/>
    Personal Email: s.johnson.dev@gmail.com<br/>
    Mobile: +1-555-987-6543<br/>
    LinkedIn: linkedin.com/in/sarahjohnson<br/>
    """
    story.append(Paragraph(contact_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles['Heading2']))
    summary = """
    Experienced software engineer with 8+ years developing scalable web applications.
    Expert in Python, JavaScript, and cloud technologies. Led teams of 5+ developers
    at multiple organizations.
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Experience
    story.append(Paragraph("WORK EXPERIENCE", styles['Heading2']))
    
    experience = """
    <b>Senior Software Engineer</b> - TechCorp Inc.<br/>
    San Francisco, CA | 2020 - Present<br/>
    Contact: hiring@techcorp.com | (415) 555-0123<br/>
    Office Address: 456 Technology Drive, San Francisco, CA 94105<br/>
    <br/>
    <b>Software Developer</b> - StartupXYZ<br/>
    Palo Alto, CA | 2018 - 2020<br/>
    HR Contact: hr@startupxyz.com | (650) 555-7890<br/>
    """
    story.append(Paragraph(experience, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # References
    story.append(Paragraph("REFERENCES", styles['Heading2']))
    
    references = """
    <b>John Smith</b> - Senior Manager, TechCorp Inc.<br/>
    Email: john.smith@techcorp.com<br/>
    Phone: (415) 555-0199<br/>
    <br/>
    <b>Emily Davis</b> - Lead Developer, StartupXYZ<br/>
    Email: emily.davis@startupxyz.com<br/>
    Phone: (650) 555-7891<br/>
    Address: 789 Innovation Way, Palo Alto, CA 94301<br/>
    <br/>
    <b>Michael Brown</b> - Technical Director<br/>
    Email: m.brown@consultant.com<br/>
    Mobile: +1 (555) 444-3333<br/>
    """
    story.append(Paragraph(references, styles['Normal']))
    
    doc.build(story)
    return filename

def create_business_cards_collection():
    """Create a PDF with multiple business cards"""
    filename = "business_cards_collection.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("BUSINESS CARD COLLECTION", styles['Title']))
    story.append(Spacer(1, 30))
    
    # Business Card 1
    card1 = """
    <b>ALEX MARTINEZ</b><br/>
    Marketing Director<br/>
    Digital Solutions Inc.<br/>
    <br/>
    📧 alex.martinez@digitalsolutions.com<br/>
    📱 (555) 111-2222<br/>
    🏢 100 Business Plaza, Suite 200<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;New York, NY 10001<br/>
    🌐 www.digitalsolutions.com
    """
    story.append(Paragraph(card1, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Business Card 2
    card2 = """
    <b>JENNIFER WONG</b><br/>
    Chief Technology Officer<br/>
    InnovateTech Corp<br/>
    <br/>
    Email: jennifer.wong@innovatetech.com<br/>
    Direct: (555) 333-4444<br/>
    Mobile: +1-555-333-4445<br/>
    Address: 250 Tech Center Drive<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Austin, TX 78701<br/>
    """
    story.append(Paragraph(card2, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Business Card 3
    card3 = """
    <b>ROBERT CHEN</b><br/>
    Senior Consultant<br/>
    Global Advisory Services<br/>
    <br/>
    r.chen@globaladvisory.com<br/>
    Office: (555) 777-8888<br/>
    Cell: (555) 777-8889<br/>
    Headquarters: 500 Financial District<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chicago, IL 60601<br/>
    Branch Office: 75 Market Street, San Francisco, CA 94103
    """
    story.append(Paragraph(card3, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Business Card 4
    card4 = """
    <b>LISA THOMPSON</b><br/>
    Operations Manager<br/>
    <br/>
    📧 lisa.thompson@operations.co<br/>
    📧 l.thompson.backup@gmail.com<br/>
    📞 Phone: (555) 999-0000<br/>
    📱 Mobile: +1 555 999 0001<br/>
    🏠 Home Office: 123 Residential Lane, Portland, OR 97201<br/>
    🏢 Corporate: 888 Corporate Blvd, Portland, OR 97205
    """
    story.append(Paragraph(card4, styles['Normal']))
    
    doc.build(story)
    return filename

def create_invoice_with_addresses():
    """Create an invoice with multiple addresses"""
    filename = "sample_invoice.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph("INVOICE #INV-2024-001", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Company Info
    company_info = """
    <b>ABC Services LLC</b><br/>
    Contact: Maria Rodriguez<br/>
    Email: maria.rodriguez@abcservices.com<br/>
    Phone: (555) 200-3000<br/>
    Business Address: 300 Commerce Street, Suite 150<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dallas, TX 75201<br/>
    <br/>
    Billing Inquiries: billing@abcservices.com<br/>
    Support: (555) 200-3001
    """
    story.append(Paragraph(company_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Bill To
    story.append(Paragraph("BILL TO:", styles['Heading3']))
    bill_to = """
    <b>XYZ Corporation</b><br/>
    Attn: David Kim<br/>
    Email: david.kim@xyzcorp.com<br/>
    Phone: (555) 400-5000<br/>
    Billing Address: 750 Enterprise Way<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Seattle, WA 98101<br/>
    """
    story.append(Paragraph(bill_to, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Ship To
    story.append(Paragraph("SHIP TO:", styles['Heading3']))
    ship_to = """
    <b>XYZ Corporation - Warehouse</b><br/>
    Attn: Susan Lee<br/>
    Email: susan.lee@xyzcorp.com<br/>
    Phone: (555) 400-5010<br/>
    Shipping Address: 1200 Industrial Parkway<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tacoma, WA 98402<br/>
    """
    story.append(Paragraph(ship_to, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Additional Contacts
    story.append(Paragraph("PROJECT CONTACTS:", styles['Heading3']))
    contacts = """
    <b>Project Manager:</b> James Wilson<br/>
    Email: james.wilson@xyzcorp.com | Phone: (555) 400-5020<br/>
    <br/>
    <b>Technical Lead:</b> Anna Foster<br/>
    Email: anna.foster@xyzcorp.com | Phone: (555) 400-5030<br/>
    Office: 750 Enterprise Way, Floor 5, Seattle, WA 98101<br/>
    """
    story.append(Paragraph(contacts, styles['Normal']))
    
    doc.build(story)
    return filename

def create_contact_form():
    """Create a contact form with multiple entries"""
    filename = "contact_form.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("EMERGENCY CONTACT FORM", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Primary Contact
    story.append(Paragraph("PRIMARY CONTACT", styles['Heading2']))
    primary = """
    Name: Thomas Anderson<br/>
    Email: thomas.anderson@matrix.com<br/>
    Phone: (555) 123-4567<br/>
    Address: 101 Main Street, Apartment 5B<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Los Angeles, CA 90210<br/>
    Relationship: Self
    """
    story.append(Paragraph(primary, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Emergency Contact 1
    story.append(Paragraph("EMERGENCY CONTACT #1", styles['Heading2']))
    emergency1 = """
    Name: Trinity Smith<br/>
    Email: trinity.smith@matrix.com<br/>
    Phone: (555) 234-5678<br/>
    Mobile: +1-555-234-5679<br/>
    Address: 202 Oak Avenue<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Los Angeles, CA 90211<br/>
    Relationship: Spouse
    """
    story.append(Paragraph(emergency1, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Emergency Contact 2
    story.append(Paragraph("EMERGENCY CONTACT #2", styles['Heading2']))
    emergency2 = """
    Name: Morpheus Johnson<br/>
    Email: morpheus.johnson@zion.org<br/>
    Phone: (555) 345-6789<br/>
    Work: (555) 345-6790<br/>
    Address: 303 Pine Street, Unit 12<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Beverly Hills, CA 90212<br/>
    Relationship: Friend
    """
    story.append(Paragraph(emergency2, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Medical Contact
    story.append(Paragraph("MEDICAL CONTACT", styles['Heading2']))
    medical = """
    Doctor: Dr. Sarah Connor<br/>
    Email: s.connor@medicalpractice.com<br/>
    Phone: (555) 456-7890<br/>
    Emergency: (555) 456-7891<br/>
    Clinic Address: 404 Health Plaza, Suite 200<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;West Hollywood, CA 90213<br/>
    """
    story.append(Paragraph(medical, styles['Normal']))
    
    doc.build(story)
    return filename

def create_mixed_format_document():
    """Create a document with tables and mixed formatting"""
    filename = "mixed_format_document.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("COMPANY DIRECTORY", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Text section
    intro = """
    This directory contains contact information for key personnel at TechStart Industries.
    For general inquiries, contact our main office at info@techstart.com or (555) 100-2000.
    Our headquarters is located at 1000 Innovation Drive, Silicon Valley, CA 94000.
    """
    story.append(Paragraph(intro, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Table with contacts
    story.append(Paragraph("DEPARTMENT CONTACTS", styles['Heading2']))
    
    data = [
        ['Name', 'Department', 'Email', 'Phone', 'Office'],
        ['Rachel Green', 'HR', 'rachel.green@techstart.com', '(555) 100-2001', 'Building A, Room 101'],
        ['Ross Geller', 'Engineering', 'ross.geller@techstart.com', '(555) 100-2002', 'Building B, Room 205'],
        ['Monica Bing', 'Finance', 'monica.bing@techstart.com', '(555) 100-2003', 'Building A, Room 150'],
        ['Chandler Tribbiani', 'Marketing', 'chandler.t@techstart.com', '(555) 100-2004', 'Building C, Room 300'],
        ['Joey Tribbiani', 'Sales', 'joey.tribbiani@techstart.com', '(555) 100-2005', 'Building C, Room 310'],
        ['Phoebe Buffay', 'Design', 'phoebe.buffay@techstart.com', '(555) 100-2006', 'Building B, Room 180']
    ]
    
    table = Table(data, colWidths=[1.2*inch, 1*inch, 2*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Additional contact info
    additional = """
    <b>ADDITIONAL CONTACTS:</b><br/>
    <br/>
    Security: security@techstart.com | (555) 100-2010<br/>
    IT Support: it.support@techstart.com | (555) 100-2020<br/>
    Facilities: facilities@techstart.com | (555) 100-2030<br/>
    <br/>
    <b>OFFICE LOCATIONS:</b><br/>
    Main Campus: 1000 Innovation Drive, Silicon Valley, CA 94000<br/>
    Research Lab: 2000 Science Park, Palo Alto, CA 94301<br/>
    Sales Office: 3000 Market Street, San Francisco, CA 94102<br/>
    """
    story.append(Paragraph(additional, styles['Normal']))
    
    doc.build(story)
    return filename

def main():
    """Generate all test PDF files"""
    print("Generating test PDF files...")
    
    # Create test_pdfs directory
    test_dir = "test_pdfs"
    os.makedirs(test_dir, exist_ok=True)
    os.chdir(test_dir)
    
    files_created = []
    
    try:
        # Generate each type of PDF
        files_created.append(create_sample_resume())
        print("+ Created sample resume")
        
        files_created.append(create_business_cards_collection())
        print("+ Created business cards collection")
        
        files_created.append(create_invoice_with_addresses())
        print("+ Created sample invoice")
        
        files_created.append(create_contact_form())
        print("+ Created contact form")
        
        files_created.append(create_mixed_format_document())
        print("+ Created mixed format document")
        
        print(f"\nSuccessfully created {len(files_created)} test PDF files in '{test_dir}' directory:")
        for file in files_created:
            print(f"  - {file}")
            
    except Exception as e:
        print(f"Error creating PDF files: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
