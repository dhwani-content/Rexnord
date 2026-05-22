import os
import re
import glob

parts_dir = r"c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in\parts"
html_files = glob.glob(os.path.join(parts_dir, "*.html"))

results = []

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if this file is for Disc Couplings by looking at the PDF folder reference
    # We look for "disc couplings" (case-insensitive) in the path
    is_disc = False
    pdf_match = re.search(r'href=["\']\.\./Couplings[^"\']*/disc couplings/([^"\']+)["\']', content, re.IGNORECASE)
    if not pdf_match:
        # Try checking iframe src
        pdf_match = re.search(r'src=["\']\.\./Couplings[^"\']*/disc couplings/([^"\']+)["\']', content, re.IGNORECASE)
        
    if pdf_match:
        is_disc = True
        pdf_name = pdf_match.group(1)
    else:
        # Also check if the content contains "disc coupling" text
        if "disc coupling" in content.lower():
            is_disc = True
            pdf_name = "Unknown"
        else:
            continue
            
    # Extract h1
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)
    h1 = h1_match.group(1).strip() if h1_match else "N/A"
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Extract part number / subtitle
    part_no_match = re.search(r'Part Number:\s*([A-Za-z0-9_-]+)', content, re.IGNORECASE)
    part_no = part_no_match.group(1).strip() if part_no_match else "N/A"
    
    results.append({
        "html_file": os.path.basename(file_path),
        "h1": h1,
        "title": title,
        "part_no": part_no,
        "pdf_name": pdf_name
    })

# Print top 5 and write all to a log file
print(f"Found {len(results)} disc coupling HTML files.")
with open(r"c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in\disc_couplings_info.txt", "w", encoding="utf-8") as out:
    for res in results:
        out.write(f"{res['html_file']}|{res['part_no']}|{res['h1']}|{res['pdf_name']}\n")
