import os
import urllib.parse
from bs4 import BeautifulSoup
import re

base_dir = r"c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in"
pdf_dir = os.path.join(base_dir, "Couplings part number flyers", "barrel couplings")
parts_dir = os.path.join(base_dir, "parts")

if not os.path.exists(parts_dir):
    os.makedirs(parts_dir)

# Template for dedicated part HTML page
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BARFLEX {part_number} Barrel Coupling | Rexnord India</title>
    <meta name="description" content="View and download the catalog for BARFLEX {part_number} Barrel Coupling.">
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .pdf-branding-banner {{
            background: linear-gradient(90deg, #0033A0 0%, #E21833 100%);
            color: white;
            text-align: center;
            padding: 15px;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .pdf-viewer-container {{
            height: 80vh;
            width: 100%;
            background: #e9ecef;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
</head>
<body style="display: flex; flex-direction: column; height: 100vh; overflow: hidden;">
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="top-bar-content">
                <span class="auth-badge"><i class="fas fa-certificate"></i> Authorized Channel Partner India</span>
                <div class="top-bar-contact">
                    <a href="mailto:mail@rexnord.co.in"><i class="fas fa-envelope"></i> mail@rexnord.co.in</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="navbar" style="border-bottom: 1px solid #ddd;">
        <div class="container nav-container">
            <a href="../index.html" class="logo">
                <span class="logo-text">Rexnord<span class="highlight"> in India.</span></span>
            </a>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../products.html">Products</a></li>
                <li><a href="../part-search.html" class="active">Part Search</a></li>
                <li><a href="../contact.html">Contact Us</a></li>
            </ul>
        </div>
    </nav>

    <!-- Branding Banner -->
    <div class="pdf-branding-banner">
        Authorised India Partner: Jinharsh Industrial Solutions Pvt. Ltd.
    </div>
    
    <!-- Header -->
    <div class="container" style="padding: 15px 0; display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <a href="../part-search.html" class="btn btn-outline btn-sm"><i class="fas fa-arrow-left"></i> Back to Search</a>
            <h1 style="font-size: 1.5rem; margin: 0; color: var(--secondary-color);">BARFLEX {part_number}</h1>
        </div>
        <a href="../{pdf_url}" download class="btn btn-primary"><i class="fas fa-download"></i> Download PDF</a>
    </div>

    <!-- PDF Viewer -->
    <div class="pdf-viewer-container" style="flex-grow: 1;">
        <iframe src="../{pdf_url}"></iframe>
    </div>
</body>
</html>"""

# HTML template for a row in part-search.html
row_template = """                        <tr>
                            <td class="fw-bold text-primary">{part_number}</td>
                            <td>Couplings</td>
                            <td>Barrel Coupling</td>
                            <td>BARFLEX</td>
                            <td>-</td>
                            <td>-</td>
                            <td>
                                <a href="parts/{safe_part_number}.html" class="btn btn-outline btn-sm">View Catalog</a>
                            </td>
                        </tr>"""

table_rows = []

files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
files.sort()

for file in files:
    # Example filename: "BARFLEX TCBR-0025 A00.pdf"
    name_no_ext = os.path.splitext(file)[0]
    
    # Extract part number, e.g. "TCBR-0025 A00"
    part_number = name_no_ext.replace("BARFLEX ", "").strip()
    safe_part_number = part_number.replace(" ", "_")
    
    pdf_rel_path = f"Couplings part number flyers/barrel couplings/{file}"
    # URL encode the path for use in HTML
    pdf_url = urllib.parse.quote(pdf_rel_path)
    
    # Generate dedicated page
    page_content = html_template.format(part_number=part_number, pdf_url=pdf_url)
    page_path = os.path.join(parts_dir, f"{safe_part_number}.html")
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
        
    # Add row to table
    row_content = row_template.format(part_number=part_number, safe_part_number=safe_part_number)
    table_rows.append(row_content)

# Update part-search.html
part_search_path = os.path.join(base_dir, "part-search.html")
with open(part_search_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace between <tbody id="catalogTableBody"> and </tbody>
import re
new_tbody = '<tbody id="catalogTableBody">\n' + '\n'.join(table_rows) + '\n                    </tbody>'
content = re.sub(r'<tbody id="catalogTableBody">.*?</tbody>', new_tbody, content, flags=re.DOTALL)

with open(part_search_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully generated {len(files)} pages and updated part-search.html")
