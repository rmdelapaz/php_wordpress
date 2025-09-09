#!/usr/bin/env python3
"""
Enhanced script to populate 02module files with content from 02module_old files.
This version better preserves formatting and handles special cases.
"""

import os
import re
from pathlib import Path
from datetime import datetime
import shutil

def extract_old_content(old_file_path):
    """
    Extract the main content from an old module file using simple string manipulation.
    This avoids issues with BeautifulSoup reformatting the HTML.
    """
    try:
        with open(old_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the main content area using regex
        main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL | re.IGNORECASE)
        
        if main_match:
            main_content = main_match.group(1).strip()
            
            # Remove the header section if it exists within main
            main_content = re.sub(r'<header>.*?</header>', '', main_content, flags=re.DOTALL | re.IGNORECASE)
            
            # Clean up extra whitespace
            main_content = re.sub(r'\n{3,}', '\n\n', main_content)
            
            return main_content
        else:
            print(f"  Warning: No <main> tag found in {old_file_path}")
            return None
            
    except Exception as e:
        print(f"  Error reading {old_file_path}: {e}")
        return None

def update_new_file(new_file_path, old_content):
    """
    Update the new module file with content from the old file.
    Preserves the new template structure and replaces only the lesson-body content.
    """
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_file_content = f.read()
        
        # Find the lesson-body div content
        lesson_body_pattern = r'(<div class="lesson-body">)(.*?)(</div>\s*<!-- Lesson Navigation -->)'
        
        match = re.search(lesson_body_pattern, new_file_content, re.DOTALL)
        
        if not match:
            # Try alternative pattern
            lesson_body_pattern = r'(<div class="lesson-body">)(.*?)(</div>\s*</article>)'
            match = re.search(lesson_body_pattern, new_file_content, re.DOTALL)
        
        if match:
            # Replace the content between the lesson-body tags
            updated_content = new_file_content[:match.start(2)] + '\n' + old_content + '\n' + new_file_content[match.end(2):]
            
            # Write the updated content back to the file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
        else:
            print(f"  Warning: Could not find lesson-body pattern in {new_file_path}")
            return False
            
    except Exception as e:
        print(f"  Error updating {new_file_path}: {e}")
        return False

def update_lesson_title_and_meta(new_file_path, old_file_path):
    """
    Update the title and meta information from the old file to the new file.
    """
    try:
        # Read old file to get title
        with open(old_file_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        # Extract title from old file
        title_match = re.search(r'<title>(.*?)</title>', old_content, re.IGNORECASE)
        if title_match:
            old_title = title_match.group(1).strip()
            
            # Read new file
            with open(new_file_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
            
            # Extract the main part of the title (remove course suffix)
            main_title = old_title.replace(' - PHP WordPress Course', '').strip()
            
            # Update the page title
            new_content = re.sub(
                r'<title>.*?</title>',
                f'<title>{main_title} - PHP WordPress Course</title>',
                new_content
            )
            
            # Update the lesson header h1
            new_content = re.sub(
                r'(<header class="lesson-header">\s*<h1>)(.*?)(</h1>)',
                rf'\1{main_title}\3',
                new_content
            )
            
            # Write back
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    except Exception as e:
        print(f"  Could not update title: {e}")

def backup_current_files():
    """
    Create a backup of current 02module files before modification.
    """
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
    
    for old_file in sorted(old_files):
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
            # Also update title and meta
            update_lesson_title_and_meta(new_file, old_file)
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
    
    return successful, failed, skipped

def fix_mermaid_diagrams(module_path):
    """
    Fix any Mermaid diagram issues in the populated files.
    """
    print("\nChecking for Mermaid diagrams...")
    
    files_with_mermaid = 0
    for html_file in module_path.glob('*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class="mermaid"' in content or '<div class="mermaid">' in content:
            files_with_mermaid += 1
            
            # Ensure mermaid-universal-fix.js is included
            if 'mermaid-universal-fix.js' not in content:
                # Add the script before closing body tag
                content = content.replace(
                    '</body>',
                    '<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>'
                )
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"  Fixed Mermaid in: {html_file.name}")
    
    if files_with_mermaid > 0:
        print(f"  Found {files_with_mermaid} files with Mermaid diagrams")
    else:
        print("  No Mermaid diagrams found")

def main():
    """
    Main function to orchestrate the content population process.
    """
    print("PHP WordPress Module Content Population Script (Enhanced)")
    print("=" * 60)
    
    base_path = Path(r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress')
    module_path = base_path / '02module'
    
    # Create backup first
    print("\nCreating backup of current 02module files...")
    if not backup_current_files():
        response = input("\nBackup failed. Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    print("\nStarting content population process...")
    successful, failed, skipped = process_modules()
    
    if successful > 0:
        # Fix Mermaid diagrams if needed
        fix_mermaid_diagrams(module_path)
    
    print("\n" + "=" * 60)
    print("Process complete!")
    
    if successful > 0:
        print(f"\n✅ Successfully populated {successful} files")
    if failed > 0:
        print(f"❌ Failed to populate {failed} files")
    if skipped > 0:
        print(f"⏩ Skipped {skipped} files (no matching new file)")
    
    print("\nNext steps:")
    print("1. Review the populated content in a browser")
    print("2. Check that code blocks and special characters display correctly")
    print("3. Verify navigation links work between lessons")
    print("4. Test any interactive elements (Mermaid diagrams, etc.)")
    
    if failed > 0:
        print("\n⚠️  Some files failed to populate. You may need to manually copy their content.")

if __name__ == "__main__":
    main()
