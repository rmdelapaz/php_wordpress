import os

# Read the file
file_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module\html_forms_inputs.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check what script is currently referenced
if 'mermaid-fix-v2.js' in content:
    # Replace mermaid-fix-v2.js with mermaid-universal-fix.js
    content = content.replace('/assets/js/mermaid-fix-v2.js', '/assets/js/mermaid-universal-fix.js')
    print("Replaced mermaid-fix-v2.js with mermaid-universal-fix.js")
elif 'mermaid-universal-fix.js' not in content:
    # Add the script before closing body tag if not present
    content = content.replace('</body>', '''<!-- Universal Mermaid Fix -->
<script src="/assets/js/mermaid-universal-fix.js"></script>
</body>''')
    print("Added mermaid-universal-fix.js script reference")
else:
    print("mermaid-universal-fix.js is already referenced")

# Write the updated content back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully!")
