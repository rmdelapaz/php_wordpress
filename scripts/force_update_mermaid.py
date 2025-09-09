#!/usr/bin/env python3
"""
Force update Mermaid fix in all HTML files
This script removes old fix and adds the new enhanced version
"""

import os
import re

def remove_old_mermaid_fix(content):
    """Remove any existing Mermaid fix script references"""
    # Remove the old fix script tag
    patterns = [
        r'<!-- Universal Mermaid Fix -->\s*<script src="/assets/js/mermaid-universal-fix.js"></script>',
        r'<script src="/assets/js/mermaid-universal-fix.js"></script>',
        r'<!-- Mermaid must load LAST to override any conflicting styles -->\s*<script src="/assets/js/mermaid-init.js"></script>',
        r'<script src="/assets/js/mermaid-init.js"[^>]*></script>',
        # Remove old inline Mermaid scripts
        r'<script src="https://cdn.jsdelivr.net/npm/mermaid@10[^"]*"[^>]*></script>',
        r'<script src="https://cdn.jsdelivr.net/npm/mermaid@9[^"]*"[^>]*></script>',
        # Remove module-based Mermaid
        r'<script type="module">[\s\S]*?import mermaid[\s\S]*?</script>'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def add_new_mermaid_fix(content):
    """Add the new enhanced Mermaid fix script"""
    # The new fix to add before closing body tag
    mermaid_fix = '''<!-- Universal Mermaid Fix (Enhanced) -->
<script src="/assets/js/mermaid-universal-fix.js"></script>
</body>'''
    
    # First remove any existing </body> with the fix
    content = content.replace('<!-- Universal Mermaid Fix -->\n<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>', '</body>')
    content = content.replace('<!-- Universal Mermaid Fix (Enhanced) -->\n<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>', '</body>')
    
    # Then add the new fix
    if '</body>' in content:
        content = content.replace('</body>', mermaid_fix)
    
    return content

def has_mermaid_content(content):
    """Check if HTML content has Mermaid diagrams"""
    return ('class="mermaid"' in content or 
            'pre class="mermaid"' in content or
            'class="mermaid-container"' in content or
            'class="mermaid-diagram"' in content)

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has Mermaid content
        if has_mermaid_content(content):
            # Remove old fix
            content = remove_old_mermaid_fix(content)
            
            # Add new fix
            content = add_new_mermaid_fix(content)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all HTML files"""
    
    # Get the current directory
    if os.name == 'nt':  # Windows
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:  # Linux/Unix
        base_dir = os.getcwd()
    
    print(f"Base directory: {base_dir}")
    print("Force updating all Mermaid fixes to enhanced version...")
    print("=" * 50)
    
    # Define the directories to search
    directories = [
        '01module',
        '02module',
        '03module',
        '04module',
        '05module',
    ]
    
    fixed_count = 0
    total_mermaid_files = 0
    
    for dir_name in directories:
        directory = os.path.join(base_dir, dir_name)
        if os.path.exists(directory):
            print(f"\nProcessing directory: {directory}")
            
            # Find all HTML files
            html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
            
            for filename in html_files:
                filepath = os.path.join(directory, filename)
                
                # Read file to check for Mermaid content
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if has_mermaid_content(content):
                        total_mermaid_files += 1
                        print(f"  Updating: {filename}")
                        
                        if process_file(filepath):
                            fixed_count += 1
                except Exception as e:
                    print(f"  Error reading {filename}: {e}")
        else:
            print(f"Directory not found: {directory}")
    
    # Also check root directory
    print(f"\nProcessing root directory: {base_dir}")
    root_html_files = [f for f in os.listdir(base_dir) if f.endswith('.html')]
    
    for filename in root_html_files:
        filepath = os.path.join(base_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if has_mermaid_content(content):
                total_mermaid_files += 1
                print(f"  Updating: {filename}")
                
                if process_file(filepath):
                    fixed_count += 1
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    # Special handling for responsive_design.html
    responsive_path = os.path.join(base_dir, '01module', 'responsive_design.html')
    if os.path.exists(responsive_path):
        print(f"\nSpecial handling for responsive_design.html...")
        if process_file(responsive_path):
            print("  Successfully updated responsive_design.html")
        else:
            print("  Failed to update responsive_design.html")
    
    print(f"\n{'='*50}")
    print(f"Total files with Mermaid content: {total_mermaid_files}")
    print(f"Files updated: {fixed_count}")
    print(f"{'='*50}")
    print("\nIMPORTANT: Clear your browser cache and reload pages to see the changes!")

if __name__ == "__main__":
    main()
