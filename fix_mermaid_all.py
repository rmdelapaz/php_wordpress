#!/usr/bin/env python3
"""
Fix Mermaid diagrams in all HTML files
This script adds the universal Mermaid fix to all HTML files that contain Mermaid diagrams
"""

import os
import re
from pathlib import Path

def has_mermaid_content(content):
    """Check if HTML content has Mermaid diagrams"""
    return 'class="mermaid"' in content or 'pre class="mermaid"' in content

def has_mermaid_fix(content):
    """Check if the Mermaid fix is already applied"""
    return 'mermaid-universal-fix.js' in content

def add_mermaid_fix(content):
    """Add the Mermaid fix script to HTML content"""
    
    # The fix to add before closing body tag
    mermaid_fix = '''<!-- Universal Mermaid Fix -->
<script src="/assets/js/mermaid-universal-fix.js"></script>
</body>'''
    
    # Replace </body> with our fix + </body>
    if '</body>' in content:
        content = content.replace('</body>', mermaid_fix)
    
    return content

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file needs fixing
        if has_mermaid_content(content) and not has_mermaid_fix(content):
            print(f"Fixing: {filepath}")
            
            # Add the fix
            fixed_content = add_mermaid_fix(content)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True
        elif has_mermaid_content(content) and has_mermaid_fix(content):
            print(f"Already fixed: {filepath}")
            return False
        else:
            # Don't print for files without Mermaid content to reduce noise
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all HTML files"""
    
    # Get the current directory (where the script is located)
    if os.name == 'nt':  # Windows
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:  # Linux/Unix
        base_dir = os.getcwd()
    
    print(f"Base directory: {base_dir}")
    
    # Define the directories to search (relative paths)
    directories = [
        '01module',
        '02module',
        '03module',
        '04module',
        '05module',
        # Add more as needed
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
                        print(f"  Found Mermaid content in: {filename}")
                        
                        if process_file(filepath):
                            fixed_count += 1
                except Exception as e:
                    print(f"  Error reading {filename}: {e}")
        else:
            print(f"Directory not found: {directory}")
    
    # Also check root directory for HTML files with Mermaid
    print(f"\nProcessing root directory: {base_dir}")
    root_html_files = [f for f in os.listdir(base_dir) if f.endswith('.html')]
    
    for filename in root_html_files:
        filepath = os.path.join(base_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if has_mermaid_content(content):
                total_mermaid_files += 1
                print(f"  Found Mermaid content in: {filename}")
                
                if process_file(filepath):
                    fixed_count += 1
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Total files with Mermaid content: {total_mermaid_files}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files already fixed: {total_mermaid_files - fixed_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
