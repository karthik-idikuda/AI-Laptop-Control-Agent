"""
Convert Markdown report to PDF using ReportLab (more reliable, pure Python)
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from pathlib import Path
import re

# Paths
md_file = r"C:\Users\idiku\.gemini\antigravity\brain\05072687-75bc-4da3-83f1-6e12fcf9bd32\OS_Agent_Complete_Report.md"
pdf_file = r"c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.pdf"

print(f"Reading markdown from: {md_file}")

# Read markdown
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

print("Creating PDF document...")

# Create PDF
doc = SimpleDocTemplate(
    pdf_file,
    pagesize=A4,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=36
)

# Container for PDF elements
story = []

# Create custom styles
styles = getSampleStyleSheet()

# Title style
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=12,
    spaceBefore=20,
    alignment=TA_LEFT,
    fontName='Helvetica-Bold'
)

# Heading 2 style
h2_style = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=colors.HexColor('#34495e'),
    spaceAfter=10,
    spaceBefore=16,
    fontName='Helvetica-Bold'
)

# Heading 3 style
h3_style = ParagraphStyle(
    'CustomH3',
    parent=styles['Heading3'],
    fontSize=14,
    textColor=colors.HexColor('#4a5f7f'),
    spaceAfter=8,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

# Heading 4 style
h4_style = ParagraphStyle(
    'CustomH4',
    parent=styles['Heading4'],
    fontSize=12,
    textColor=colors.HexColor('#5a6f8f'),
    spaceAfter=6,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

# Normal text
normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY
)

# Code style
code_style = ParagraphStyle(
    'CustomCode',
    parent=styles['Code'],
    fontSize=8,
    fontName='Courier',
    textColor=colors.HexColor('#c7254e'),
    backColor=colors.HexColor('#f4f4f4'),
    leftIndent=20,
    rightIndent=20
)

print("Processing markdown content...")

# Split into lines
lines = md_content.split('\n')
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Skip empty lines
    if not line:
        i += 1
        continue
    
    # Horizontal rule
    if line.startswith('---'):
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph('<hr/>', normal_style))
        story.append(Spacer(1, 0.2*inch))
        i += 1
        continue
    
    # Heading 1
    if line.startswith('# '):
        text = line[2:].strip()
        story.append(PageBreak())
        story.append(Paragraph(text, title_style))
        i += 1
        continue
    
    # Heading 2
    if line.startswith('## '):
        text = line[3:].strip()
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(text, h2_style))
        i += 1
        continue
    
    # Heading 3
    if line.startswith('### '):
        text = line[4:].strip()
        story.append(Paragraph(text, h3_style))
        i += 1
        continue
    
    # Heading 4
    if line.startswith('#### '):
        text = line[5:].strip()
        story.append(Paragraph(text, h4_style))
        i += 1
        continue
    
    # Code blocks
    if line.startswith('```'):
        code_lines = []
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            code_lines.append(lines[i])
            i += 1
        if code_lines:
            code_text = '\n'.join(code_lines)
            # Use Preformatted for code blocks
            story.append(Preformatted(code_text, code_style))
            story.append(Spacer(1, 0.1*inch))
        i += 1
        continue
    
    # Lists
    if line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\.', line):
        text = line[2:] if line.startswith(('- ', '* ')) else re.sub(r'^\d+\.\s*', '', line)
        text = f"• {text}"
        story.append(Paragraph(text, normal_style))
        i += 1
        continue
    
    # Blockquote
    if line.startswith('> '):
        text = line[2:]
        quote_style = ParagraphStyle('Quote', parent=normal_style, leftIndent=20, textColor=colors.HexColor('#555'))
        story.append(Paragraph(f"<i>{text}</i>", quote_style))
        i += 1
        continue
    
    # Tables (simple handling)
    if '|' in line:
        table_lines = []
        while i < len(lines) and '|' in lines[i]:
            table_lines.append(lines[i])
            i += 1
        
        if len(table_lines) > 2:  # Has header + separator + data
            # Parse table
            rows = []
            for tline in table_lines:
                if not tline.strip().replace('|', '').replace('-', '').strip():
                    continue  # Skip separator
                cells = [cell.strip() for cell in tline.split('|')[1:-1]]
                if cells:
                    rows.append(cells)
            
            if rows:
                # Create table
                t = Table(rows)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.2*inch))
        continue
    
    # Regular paragraph
    if line:
        # Convert markdown bold and italics
        text = line
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font face="courier" color="#c7254e">\1</font>', text)
        
        story.append(Paragraph(text, normal_style))
        story.append(Spacer(1, 0.05*inch))
    
    i += 1

print("Building PDF...")

# Build PDF
doc.build(story)

print(f"✅ PDF created successfully: {pdf_file}")
file_size = Path(pdf_file).stat().st_size / 1024
print(f"📄 File size: {file_size:.1f} KB")
print(f"📍 Location: {pdf_file}")
