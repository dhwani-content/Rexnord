import os
import glob

parts_dir = r"c:\Users\krupe\Downloads\rexnord.co.in\rexnord.co.in\parts"
html_files = glob.glob(os.path.join(parts_dir, "*.html"))

missing_banner = []
missing_details = []

for file_path in html_files:
    basename = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    if "Authorised India Partner: Jinharsh" not in content:
        missing_banner.append(basename)
        
        # Check some details to see if it's Kop-Flex or Rexnord Thomas
        category = "Unknown"
        if "kop-flex" in content.lower() or "kop-flex" in basename.lower() or "kd" in basename.lower():
            category = "Kop-Flex"
        elif "thomas" in content.lower() or "thomas" in basename.lower():
            category = "Rexnord Thomas"
        elif "morse" in content.lower():
            category = "Morse"
        elif "bareflex" in content.lower() or "barflex" in content.lower():
            category = "Bareflex"
            
        missing_details.append((basename, category))

print(f"Total HTML files: {len(html_files)}")
print(f"Files missing banner: {len(missing_banner)}")
for name, cat in missing_details[:20]:
    print(f"  {name} ({cat})")
if len(missing_details) > 20:
    print("  ...")
