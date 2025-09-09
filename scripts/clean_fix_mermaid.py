#!/usr/bin/env python3
"""
Force update Mermaid fix in all HTML files - CLEAN VERSION
This script removes ALL old mermaid references and adds only the universal fix
"""

import os
import re

def clean_all_mermaid_references(content):
    """Remove ALL existing Mermaid-related scripts and fixes"""
    
    # List of patterns to remove
    patterns = [
        # Remove all universal fix references (old and new)
        r'<!-- Universal Mermaid Fix[^>]*-->\s*<script src="/assets/js/mermaid-universal-fix.js"></script>',
        r'<script src="/assets/js/mermaid-universal-fix.js"></script>',
        
        # Remove old mermaid-init.js
        r'<!-- Mermaid must load LAST[^>]*-->\s*<script src="/assets/js/mermaid-init.js"></script>',
        r'<script src="/assets/js/mermaid-init.js"[^>]*></script>',
        
        # Remove CDN Mermaid scripts
        r'<script src="https://cdn.jsdelivr.net/npm/mermaid@[^"]*"[^>]*></script>',
        
        # Remove module-based Mermaid
        r'<script type="module">[\s\S]*?import mermaid[\s\S]*?</script>',
        
        # Remove inline Mermaid initialization scripts
        r'<script>\s*//[^\n]*mermaid[^\n]*\n[\s\S]*?if \(typeof mermaid[\s\S]*?</script>',
        
        # Remove Mermaid fallback sections
        r'<!-- Mermaid fallback -->\s*',
        r'<!-- Mermaid for diagrams -->\s*',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content

def add_universal_fix_once(content):
    """Add the universal fix script only once before </body>"""
    
    # The fix to add
    mermaid_fix = '''<!-- Universal Mermaid Fix -->
<script src="/assets/js/mermaid-universal-fix.js"></script>
</body>'''
    
    # Make sure we only have one </body> tag with the fix
    content = content.replace('</body>', mermaid_fix)
    
    # Remove any duplicate fixes that might have been created
    fix_count = content.count('mermaid-universal-fix.js')
    if fix_count > 1:
        # Keep only the last one (before </body>)
        parts = content.split('<!-- Universal Mermaid Fix -->')
        if len(parts) > 2:
            # Reconstruct with only the last fix
            content = parts[0]
            for i in range(1, len(parts) - 1):
                # Skip the script line for middle parts
                part = parts[i]
                if '<script src="/assets/js/mermaid-universal-fix.js"></script>' in part:
                    part = part.replace('<script src="/assets/js/mermaid-universal-fix.js"></script>', '')
                content += part
            content += '<!-- Universal Mermaid Fix -->' + parts[-1]
    
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
            # Clean all old references
            content = clean_all_mermaid_references(content)
            
            # Add the universal fix once
            content = add_universal_fix_once(content)
            
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
    print("Cleaning and updating all Mermaid implementations...")
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
                        print(f"  Cleaning and updating: {filename}")
                        
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
                print(f"  Cleaning and updating: {filename}")
                
                if process_file(filepath):
                    fixed_count += 1
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Total files with Mermaid content: {total_mermaid_files}")
    print(f"Files cleaned and updated: {fixed_count}")
    print(f"{'='*50}")
    print("\nIMPORTANT:")
    print("1. Clear your browser cache (Ctrl+Shift+Delete)")
    print("2. Hard refresh pages (Ctrl+F5 or Cmd+Shift+R)")
    print("3. If issues persist, open console and run: window.reinitializeMermaid()")

if __name__ == "__main__":
    main()
