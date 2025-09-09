#!/usr/bin/env python3
"""
Script to populate 02module files with content from 02module_old files.
This script extracts the main content from old HTML files and inserts it
into the new template structure while preserving the layout.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

def extract_old_content(old_file_path):
    """
    Extract the main content from an old module file.
    Returns the content between <main> tags, excluding header and footer.
    """
    try:
        with open(old_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the main content area
        main_content = soup.find('main')
        if not main_content:
            print(f"  Warning: No <main> tag found in {old_file_path}")
            # Try to find content in body instead
            body = soup.find('body')
            if body:
                # Remove header and footer if they exist
                header = body.find('header')
                if header:
                    header.decompose()
                footer = body.find('footer')
                if footer:
                    footer.decompose()
                main_content = body
        
        if main_content:
            # Convert all sections to string format
            sections = main_content.find_all('section')
            
            # Build the content string
            content_parts = []
            for section in sections:
                # Convert section to string and clean up
                section_html = str(section)
                # Remove any existing indentation
                section_html = re.sub(r'^\s+', '', section_html, flags=re.MULTILINE)
                content_parts.append(section_html)
            
            return '\n\n'.join(content_parts)
        
        return None
    except Exception as e:
        print(f"  Error reading {old_file_path}: {e}")
        return None

def update_new_file(new_file_path, old_content):
    """
    Update the new module file with content from the old file.
    Preserves the new template structure and replaces the placeholder content.
    """
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_file_content = f.read()
        
        # Parse the new file
        soup = BeautifulSoup(new_file_content, 'html.parser')
        
        # Find the lesson-body div
        lesson_body = soup.find('div', class_='lesson-body')
        
        if not lesson_body:
            print(f"  Warning: No lesson-body div found in {new_file_path}")
            return False
        
        # Clear existing content in lesson-body
        lesson_body.clear()
        
        # Add the old content to lesson-body
        if old_content:
            # Parse the old content and add it to lesson-body
            old_soup = BeautifulSoup(old_content, 'html.parser')
            for element in old_soup:
                if element.name:  # Skip text nodes
                    lesson_body.append(element)
        
        # Convert back to string with proper formatting
        updated_html = str(soup.prettify())
        
        # Write the updated content back to the file
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        return True
    except Exception as e:
        print(f"  Error updating {new_file_path}: {e}")
        return False

def process_modules():
    """
    Process all module files, copying content from old to new.
    """
    base_path = Path(r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress')
    old_module_path = base_path / '02module_old'
    new_module_path = base_path / '02module'
    
    # Get list of HTML files in old module directory
    old_files = list(old_module_path.glob('*.html'))
    
    print(f"Found {len(old_files)} HTML files in 02module_old")
    print("=" * 60)
    
    successful = 0
    failed = 0
    skipped = 0
    
    for old_file in old_files:
        filename = old_file.name
        new_file = new_module_path / filename
        
        print(f"\nProcessing: {filename}")
        
        # Check if corresponding new file exists
        if not new_file.exists():
            print(f"  Skipping: No corresponding file in 02module")
            skipped += 1
            continue
        
        # Extract content from old file
        old_content = extract_old_content(old_file)
        
        if old_content is None:
            print(f"  Failed: Could not extract content from old file")
            failed += 1
            continue
        
        # Update new file with old content
        if update_new_file(new_file, old_content):
            print(f"  Success: Content populated")
            successful += 1
        else:
            print(f"  Failed: Could not update new file")
            failed += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {len(old_files)}")

def backup_current_files():
    """
    Create a backup of current 02module files before modification.
    """
    import shutil
    from datetime import datetime
    
    base_path = Path(r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress')
    module_path = base_path / '02module'
    backup_path = base_path / f'02module_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    print(f"Creating backup at: {backup_path}")
    try:
        shutil.copytree(module_path, backup_path)
        print("Backup created successfully")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def main():
    """
    Main function to orchestrate the content population process.
    """
    print("PHP WordPress Module Content Population Script")
    print("=" * 60)
    
    # Create backup first
    print("\nCreating backup of current 02module files...")
    if not backup_current_files():
        response = input("\nBackup failed. Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    print("\nStarting content population process...")
    process_modules()
    
    print("\n" + "=" * 60)
    print("Process complete!")
    print("\nNote: You may need to:")
    print("1. Check for any Mermaid diagrams that need the mermaid-universal-fix.js")
    print("2. Verify that all special characters and code blocks are properly formatted")
    print("3. Test the navigation links between lessons")

if __name__ == "__main__":
    # Check if BeautifulSoup is installed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Error: BeautifulSoup4 is required. Install it with:")
        print("  pip install beautifulsoup4")
        exit(1)
    
    main()
