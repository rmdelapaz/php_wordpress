#!/usr/bin/env python3
"""
Script to transfer content from 02module_old HTML files to 02module files
while preserving the new template structure.
Based on the working transfer_01module.py script.
"""

import os
import re
from pathlib import Path
from datetime import datetime
import shutil

def extract_main_content(old_file_path):
    """Extract the main content from the old HTML file."""
    with open(old_file_path, 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', old_html, re.DOTALL)
    title = title_match.group(1) if title_match else "Untitled"
    
    # Extract main content
    main_match = re.search(r'<main>(.*?)</main>', old_html, re.DOTALL)
    main_content = main_match.group(1) if main_match else ""
    
    # Remove header from main content if it exists
    main_content = re.sub(r'<header>.*?</header>', '', main_content, flags=re.DOTALL)
    
    # Check if mermaid is used
    has_mermaid = 'mermaid' in old_html.lower()
    
    return {
        'title': title.strip(),
        'content': main_content.strip(),
        'has_mermaid': has_mermaid
    }

def update_new_file(new_file_path, old_content):
    """Update the new file with content from the old file."""
    with open(new_file_path, 'r', encoding='utf-8') as f:
        new_html = f.read()
    
    # Clean title (remove course suffix if present)
    clean_title = old_content['title']
    for suffix in [' - PHP WordPress Course', ' - PHP Course', ' - Course']:
        clean_title = clean_title.replace(suffix, '')
    
    # Update title
    new_html = re.sub(
        r'<title>.*?</title>',
        f'<title>{clean_title} - PHP WordPress Course</title>',
        new_html
    )
    
    # Update meta description
    desc_text = clean_title.replace(' - ', '. ').replace(':', '.')
    new_html = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{desc_text}">',
        new_html
    )
    
    # Update the h1 in lesson header
    new_html = re.sub(
        r'(<header class="lesson-header">.*?<h1>)(.*?)(</h1>)',
        r'\1' + clean_title + r'\3',
        new_html,
        flags=re.DOTALL
    )
    
    # Replace lesson body content
    # First, fix class names in old content (underscore to hyphen)
    fixed_content = old_content['content']
    fixed_content = re.sub(r'class="([^"]*?)_([^"]*?)"', r'class="\1-\2"', fixed_content)
    fixed_content = re.sub(r"class='([^']*?)_([^']*?)'", r"class='\1-\2'", fixed_content)
    
    # Replace the lesson body content
    new_html = re.sub(
        r'(<div class="lesson-body">)(.*?)(</div>\s*<!-- Lesson Navigation -->)',
        r'\1\n' + fixed_content + '\n            \3',
        new_html,
        flags=re.DOTALL
    )
    
    # Add mermaid script if needed and not already present
    if old_content['has_mermaid'] and 'mermaid-universal-fix.js' not in new_html:
        # Add mermaid fix script before closing body
        new_html = new_html.replace(
            '</body>',
            '<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>'
        )
    
    return new_html

def process_file(filename, old_dir, new_dir):
    """Process a single file."""
    old_file = old_dir / filename
    new_file = new_dir / filename
    
    if not old_file.exists():
        return False, f"Old file doesn't exist: {filename}"
    
    if not new_file.exists():
        return False, f"New file doesn't exist: {filename}"
    
    try:
        # Extract content from old file
        old_content = extract_main_content(old_file)
        
        # Update new file with old content
        updated_html = update_new_file(new_file, old_content)
        
        # Write updated content
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        return True, f"Successfully updated {filename}"
        
    except Exception as e:
        return False, f"Error processing {filename}: {str(e)}"

def backup_directory(dir_path):
    """Create a backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = dir_path.parent / f"{dir_path.name}_backup_{timestamp}"
    
    print(f"Creating backup at: {backup_path.name}")
    try:
        shutil.copytree(str(dir_path), str(backup_path))
        print("✓ Backup created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating backup: {e}")
        return False

def main():
    """Main function to process all files."""
    
    # For Windows accessing WSL files, use the UNC path
    # For running within WSL, use the Linux path
    
    # Try Windows UNC path first
    old_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    new_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    
    # If Windows paths don't exist, try Linux paths (for running within WSL)
    if not old_dir.exists():
        old_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        new_dir = Path("/home/practicalace/projects/php_wordpress/02module")
    
    # Check if directories exist
    if not old_dir.exists():
        print(f"Error: Directory not found: {old_dir}")
        print("\nTrying alternative path formats...")
        
        # Try alternative Windows path
        old_dir = Path("//wsl$/Ubuntu/home/practicalace/projects/php_wordpress/02module_old")
        new_dir = Path("//wsl$/Ubuntu/home/practicalace/projects/php_wordpress/02module")
        
        if not old_dir.exists():
            print("Error: Could not find the project directories.")
            print("\nPlease make sure:")
            print("1. You're running this script from Windows")
            print("2. WSL is running")
            print("3. The path exists: \\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress")
            return
    
    if not new_dir.exists():
        print(f"Error: Directory not found: {new_dir}")
        return
    
    # Get all HTML files from 02module_old
    old_files = list(old_dir.glob("*.html"))
    if not old_files:
        print(f"Error: No HTML files found in {old_dir}")
        return
    
    print("=" * 60)
    print("PHP WordPress Module Content Transfer Script")
    print("=" * 60)
    print(f"Source: {old_dir}")
    print(f"Target: {new_dir}")
    print(f"Files to process: {len(old_files)}")
    print()
    
    # Create backup
    response = input("Create backup of 02module before proceeding? (y/n): ")
    if response.lower() == 'y':
        if not backup_directory(new_dir):
            response = input("Backup failed. Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Exiting...")
                return
    
    print("\nStarting content transfer...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    skipped = 0
    
    for old_file in sorted(old_files):
        filename = old_file.name
        new_file = new_dir / filename
        
        if not new_file.exists():
            print(f"⏩ Skipped {filename} (no matching file in 02module)")
            skipped += 1
            continue
        
        success, message = process_file(filename, old_dir, new_dir)
        
        if success:
            print(f"✓ {message}")
            successful += 1
        else:
            print(f"✗ {message}")
            failed += 1
    
    print("=" * 60)
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {len(old_files)}")
    
    if successful > 0:
        print("\n✨ Success! Your files have been populated.")
        print("\nNext steps:")
        print("1. Open a browser and check the populated content")
        print("2. Verify code blocks display correctly")
        print("3. Test navigation links")
        print("4. Check Mermaid diagrams if any")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    
    input("\nPress Enter to exit...")
