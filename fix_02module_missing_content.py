#!/usr/bin/env python3
"""
Smart script to identify and fix 02module HTML files that are missing their actual content.
Only processes files with placeholder content, leaves properly populated files untouched.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

def has_placeholder_content(file_path):
    """
    Check if a file has placeholder/generic content.
    Returns True if the file needs to be populated with real content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Indicators of placeholder content
        placeholder_indicators = [
            "// Example PHP code",
            "// Tailored to the specific lesson topic",
            "// Practical example",
            "// Specific to lesson content",
            "<li>Master PHP programming concepts</li>",
            "<li>Write clean, maintainable code</li>",
            "<li>Apply best practices</li>",
            "<li>Build dynamic applications</li>"
        ]
        
        # Count how many placeholder indicators are present
        placeholder_count = sum(1 for indicator in placeholder_indicators if indicator in content)
        
        # If we have 3 or more placeholder indicators, it's likely generic content
        if placeholder_count >= 3:
            return True
        
        # Also check if the lesson-body section is suspiciously short
        lesson_body_match = re.search(r'<div class="lesson-body">(.*?)</div>\s*<!-- Lesson Navigation -->', 
                                     content, re.DOTALL)
        if lesson_body_match:
            body_content = lesson_body_match.group(1)
            # If body content is less than 500 characters, it's probably placeholder
            if len(body_content.strip()) < 500:
                return True
        
        return False
        
    except Exception as e:
        print(f"    Error checking file: {e}")
        return False

def extract_old_content(old_file_path):
    """Extract the main content from the old HTML file."""
    try:
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
    except Exception as e:
        print(f"    Error extracting content: {e}")
        return None

def update_file_content(new_file_path, old_content):
    """Update the new file with content from the old file."""
    try:
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
        
        # Update meta description (extract first meaningful sentence from content)
        desc_match = re.search(r'<p[^>]*>([^<]+)</p>', old_content['content'])
        if desc_match:
            desc_text = desc_match.group(1).strip()[:160]  # Max 160 chars for meta description
        else:
            desc_text = clean_title.replace(' - ', '. ').replace(':', '.')
        
        new_html = re.sub(
            r'<meta content="[^"]*" name="description"/>',
            f'<meta content="{desc_text}" name="description"/>',
            new_html
        )
        
        # Update the h1 in lesson header
        new_html = re.sub(
            r'(<header class="lesson-header">\s*<h1>)(.*?)(</h1>)',
            r'\1' + clean_title + r'\3',
            new_html,
            flags=re.DOTALL
        )
        
        # Update learning objectives if they're generic
        if "Master PHP programming concepts" in new_html:
            # Try to extract actual objectives from old content
            objectives_match = re.search(r'<h2>Learning Objectives</h2>(.*?)</section>', 
                                        old_content['content'], re.DOTALL)
            if objectives_match and '<ul>' in objectives_match.group(1):
                # Extract the ul content
                ul_match = re.search(r'<ul>(.*?)</ul>', objectives_match.group(1), re.DOTALL)
                if ul_match:
                    new_objectives = ul_match.group(0)
                    new_html = re.sub(
                        r'(<div class="lesson-objectives">.*?<h2>Learning Objectives</h2>\s*)<ul>.*?</ul>',
                        r'\1' + new_objectives,
                        new_html,
                        flags=re.DOTALL
                    )
        
        # Fix class names in old content (underscore to hyphen)
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
        
        # Add mermaid fix script if needed and not already present
        if old_content['has_mermaid'] and 'mermaid-universal-fix.js' not in new_html:
            new_html = new_html.replace(
                '</body>',
                '<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>'
            )
        
        # Write the updated content
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True
        
    except Exception as e:
        print(f"    Error updating file: {e}")
        return False

def create_backup(directory):
    """Create a backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = directory.parent / f"{directory.name}_fix_backup_{timestamp}"
    
    try:
        shutil.copytree(str(directory), str(backup_dir))
        return backup_dir
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def main():
    """Main function to identify and fix files with missing content."""
    
    # Set up paths
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    old_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    
    # Check if directories exist
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        
        if not module_dir.exists():
            print("Error: 02module directory not found")
            return
    
    print("=" * 70)
    print(" Smart Content Fix for Module 02")
    print(" Identifies and fixes only files with placeholder content")
    print("=" * 70)
    print(f"Checking: {module_dir}")
    print(f"Source: {old_module_dir}\n")
    
    # Create backup
    response = input("Create backup before proceeding? (y/n): ")
    if response.lower() == 'y':
        backup_dir = create_backup(module_dir)
        if backup_dir:
            print(f"✓ Backup created: {backup_dir.name}\n")
        else:
            if input("Continue without backup? (y/n): ").lower() != 'y':
                return
    
    # Get all HTML files
    html_files = list(module_dir.glob("*.html"))
    print(f"Found {len(html_files)} HTML files\n")
    
    # Analyze files
    print("Analyzing files for placeholder content...")
    print("-" * 70)
    
    files_needing_fix = []
    files_already_ok = []
    files_no_source = []
    
    for file_path in sorted(html_files):
        print(f"Checking: {file_path.name:<50}", end=" ")
        
        if has_placeholder_content(file_path):
            # Check if corresponding old file exists
            old_file = old_module_dir / file_path.name
            if old_file.exists():
                print("❌ Placeholder content found")
                files_needing_fix.append((file_path, old_file))
            else:
                print("⚠️ Placeholder content, but no source file")
                files_no_source.append(file_path)
        else:
            print("✓ Has real content")
            files_already_ok.append(file_path)
    
    # Report findings
    print("\n" + "=" * 70)
    print("Analysis Results:")
    print(f"  ✓ Files with real content: {len(files_already_ok)}")
    print(f"  ❌ Files needing fix: {len(files_needing_fix)}")
    print(f"  ⚠️ Files with no source: {len(files_no_source)}")
    
    if files_needing_fix:
        print(f"\nFiles that need fixing:")
        for file_path, _ in files_needing_fix:
            print(f"  - {file_path.name}")
        
        print("\n" + "-" * 70)
        response = input(f"\nFix {len(files_needing_fix)} files? (y/n): ")
        
        if response.lower() == 'y':
            print("\nFixing files...")
            fixed = 0
            failed = 0
            
            for new_file, old_file in files_needing_fix:
                print(f"  Fixing: {new_file.name:<50}", end=" ")
                
                # Extract content from old file
                old_content = extract_old_content(old_file)
                
                if old_content:
                    # Update new file
                    if update_file_content(new_file, old_content):
                        print("✓ Fixed")
                        fixed += 1
                    else:
                        print("✗ Failed to update")
                        failed += 1
                else:
                    print("✗ Could not extract content")
                    failed += 1
            
            print("\n" + "=" * 70)
            print("Fix Summary:")
            print(f"  ✓ Successfully fixed: {fixed} files")
            if failed > 0:
                print(f"  ✗ Failed to fix: {failed} files")
            
            if fixed > 0:
                print("\n✨ Files have been populated with their actual content!")
                print("   Please review the changes in your browser.")
    else:
        print("\n✨ Great news! All files already have real content.")
        print("   No fixes needed.")
    
    if files_no_source:
        print(f"\n⚠️ Warning: {len(files_no_source)} files have placeholder content but no source:")
        for file_path in files_no_source:
            print(f"  - {file_path.name}")
        print("   These files need manual attention.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        input("\nPress Enter to exit...")
