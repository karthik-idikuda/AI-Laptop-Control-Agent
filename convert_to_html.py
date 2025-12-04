"""
Convert Markdown to beautiful HTML (can be printed to PDF from browser)
"""

import markdown
from pathlib import Path

# Paths
md_file = r"C:\Users\idiku\.gemini\antigravity\brain\05072687-75bc-4da3-83f1-6e12fcf9bd32\OS_Agent_Complete_Report.md"
html_file = r"c:\Users\idiku\Downloads\os agent\OS_Agent_Complete_Report.html"

print(f"Reading markdown from: {md_file}")

# Read markdown
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

print("Converting markdown to HTML...")

# Convert markdown to HTML
html_content = markdown.markdown(
    md_content,
    extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        'toc',
        'nl2br',
        'sane_lists'
    ]
)

# Professional CSS styling optimized for PDF printing
css = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OS Agent - Complete Technical Report</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        @media print {
            body {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
            }
            
            pre, blockquote, table {
                page-break-inside: avoid;
            }
            
            img {
                max-width: 100%;
                page-break-inside: avoid;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            background: white;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 28pt;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
            page-break-before: always;
        }
        
        h1:first-of-type {
            page-break-before: auto;
        }
        
        h2 {
            color: #34495e;
            font-size: 20pt;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #95a5a6;
        }
        
        h3 {
            color: #4a5f7f;
            font-size: 16pt;
            margin-top: 24px;
            margin-bottom: 12px;
        }
        
        h4 {
            color: #5a6f8f;
            font-size: 13pt;
            margin-top: 18px;
            margin-bottom: 10px;
        }
        
        h5, h6 {
            color: #6a7f9f;
            font-size: 12pt;
            margin-top: 15px;
            margin-bottom: 8px;
        }
        
        p {
            margin: 10px 0;
            text-align: justify;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        ul, ol {
            margin: 12px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 6px 0;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
            background: #f9f9f9;
            padding: 15px 20px;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            color: #c7254e;
        }
        
        pre {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }
        
        pre code {
            background-color: transparent;
            color: #ecf0f1;
            padding: 0;
            font-size: 9pt;
            display: block;
            line-height: 1.4;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 10pt;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        thead {
            background-color: #3498db;
            color: white;
        }
        
        th {
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #2980b9;
        }
        
        td {
            padding: 10px 12px;
            border: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f0f8ff;
        }
        
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }
        
        /* Checkmarks and special characters */
        .emoji {
            font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif;
        }
        
        /* Code highlighting */
        .codehilite {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        /* Table of contents styling */
        .toc {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc ul ul {
            padding-left: 20px;
        }
        
        .toc li {
            margin: 5px 0;
        }
        
        .toc a {
            color: #2c3e50;
        }
        
        /* Header/Footer for printing */
        @media print {
            @page {
                @top-right {
                    content: "OS Agent Technical Report | Page " counter(page);
                    font-size: 9pt;
                    color: #666;
                }
            }
        }
        
        /* Cover page styling  */
        .cover-page {
            text-align: center;
            padding: 100px 0;
            page-break-after: always;
        }
        
        .cover-title {
            font-size: 36pt;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .cover-subtitle {
            font-size: 18pt;
            color: #7f8c8d;
            margin-bottom: 40px;
        }
        
        .cover-info {
            font-size: 12pt;
            color: #95a5a6;
            line-height: 2;
        }
    </style>
</head>
<body>
    <div class="cover-page">
        <h1 class="cover-title">🤖 OS Agent</h1>
        <p class="cover-subtitle">Complete Technical Report A-Z</p>
        <div class="cover-info">
            <p><strong>AI-Powered Operating System Automation</strong></p>
            <p>Cross-Platform Computer Control via Natural Language</p>
            <p>Version 1.0 Alpha</p>
            <p>November 2025</p>
        </div>
    </div>
"""

# Create full HTML
full_html = css + html_content + """
</body>
</html>
"""

# Write HTML file
print(f"Writing HTML file...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"✅ HTML created successfully: {html_file}")
file_size = Path(html_file).stat().st_size / 1024
print(f"📄 File size: {file_size:.1f} KB")
print(f"📍 Location: {html_file}")
print("\n" + "="*70)
print("📖 TO CONVERT TO PDF:")
print("="*70)
print("1. Open the HTML file in your browser (Chrome/Edge)")
print(f"   File: {html_file}")
print("2. Press Ctrl+P (Print)")
print("3. Select 'Save as PDF' as the printer")
print("4. Optional: Adjust margins and settings")
print("5. Click 'Save' and choose destination")
print("="*70)
