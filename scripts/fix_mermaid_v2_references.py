#!/usr/bin/env python3
"""
Fix all references to mermaid-fix-v2.js in HTML files
"""

import os
import re

def fix_mermaid_reference(filepath):
    """Fix mermaid-fix-v2.js references in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace mermaid-fix-v2.js with mermaid-universal-fix.js
        content = content.replace('mermaid-fix-v2.js', 'mermaid-universal-fix.js')
        
        # Also clean up any duplicate comments
        content = re.sub(
            r'<!-- Universal Mermaid Fix \(Enhanced\) -->\s*<!-- Universal Mermaid Fix -->',
            '<!-- Universal Mermaid Fix -->',
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix all HTML files"""
    
    # Get the current directory
    if os.name == 'nt':  # Windows
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:  # Linux/Unix
        base_dir = os.getcwd()
    
    print("Fixing mermaid-fix-v2.js references...")
    print("=" * 50)
    
    # Define the directories to search
    directories = [
        '01module',
        '02module',
        '03module',
        '04module',
        '05module',
    ]
    
    fixed_files = []
    
    for dir_name in directories:
        directory = os.path.join(base_dir, dir_name)
        if os.path.exists(directory):
            print(f"\nChecking directory: {directory}")
            
            # Find all HTML files
            html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
            
            for filename in html_files:
                filepath = os.path.join(directory, filename)
                
                # Check if file contains the old reference
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'mermaid-fix-v2.js' in content:
                        print(f"  Fixing: {filename}")
                        if fix_mermaid_reference(filepath):
                            fixed_files.append(filepath)
                except Exception as e:
                    print(f"  Error reading {filename}: {e}")
        else:
            print(f"Directory not found: {directory}")
    
    # Also check root directory
    print(f"\nChecking root directory: {base_dir}")
    root_html_files = [f for f in os.listdir(base_dir) if f.endswith('.html')]
    
    for filename in root_html_files:
        filepath = os.path.join(base_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'mermaid-fix-v2.js' in content:
                print(f"  Fixing: {filename}")
                if fix_mermaid_reference(filepath):
                    fixed_files.append(filepath)
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    print(f"\n{'='*50}")
    if fixed_files:
        print(f"Fixed {len(fixed_files)} files:")
        for filepath in fixed_files:
            print(f"  - {os.path.basename(filepath)}")
    else:
        print("No files needed fixing!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
