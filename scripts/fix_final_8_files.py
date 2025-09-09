#!/usr/bin/env python3
"""
Final fix for the remaining 8 files with regex escape issues.
This script uses a different approach - it extracts and directly replaces content
without using regex operations that could fail on escape sequences.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

# The 8 remaining problematic files
PROBLEMATIC_FILES = [
    'homework_php_calculator.html',
    'homework_php_create_contact_form_validation.html', 
    'homework_php_create_library_custom_functions.html',
    'homework_php_grades.html',
    'php_form_validation_techniques.html',
    'php_inheritance.html',
    'php_namespaces.html',
    'review_php_setup.html'
]

def extract_content_from_old_file(old_file_path):
    """Extract content from old file without regex operations."""
    try:
        with open(old_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title using string operations
        title = "Untitled"
        if '<title>' in content and '</title>' in content:
            start = content.index('<title>') + 7
            end = content.index('</title>', start)
            title = content[start:end].strip()
        
        # Extract main content using string operations
        main_content = ""
        if '<main>' in content and '</main>' in content:
            start = content.index('<main>') + 6
            end = content.index('</main>', start)
            main_content = content[start:end].strip()
            
            # Remove header if present
            if '<header>' in main_content and '</header>' in main_content:
                header_start = main_content.index('<header>')
                header_end = main_content.index('</header>') + 9
                main_content = main_content[:header_start] + main_content[header_end:]
        
        # Check for mermaid
        has_mermaid = 'mermaid' in content.lower()
        
        return {
            'title': title,
            'content': main_content,
            'has_mermaid': has_mermaid
        }
    except Exception as e:
        print(f"Error extracting: {e}")
        return None

def fix_class_names(content):
    """Fix underscore to hyphen in class names without regex."""
    # This is a simple approach that handles most cases
    replacements = [
        ('class="best_practice"', 'class="best-practice"'),
        ('class="important_note"', 'class="important-note"'),
        ('class="real_world_example"', 'class="real-world-example"'),
        ('class="code_example"', 'class="code-example"'),
        ('class="exercise_section"', 'class="exercise-section"'),
        ('class="homework_assignment"', 'class="homework-assignment"'),
        ('class="comparison_table"', 'class="comparison-table"'),
        ('class="mermaid_diagram"', 'class="mermaid-diagram"'),
        ('class="output_example"', 'class="output-example"'),
        ("class='best_practice'", 'class="best-practice"'),
        ("class='important_note'", 'class="important-note"'),
        ("class='real_world_example'", 'class="real-world-example"'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    return content

def update_file_safely(new_file_path, old_content):
    """Update file using string operations instead of regex."""
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_html = f.read()
        
        # Clean title
        clean_title = old_content['title']
        for suffix in [' - PHP WordPress Course', ' - PHP Course', ' - Course']:
            clean_title = clean_title.replace(suffix, '')
        
        # Update title
        if '<title>' in new_html and '</title>' in new_html:
            start = new_html.index('<title>')
            end = new_html.index('</title>') + 8
            new_html = new_html[:start] + f'<title>{clean_title} - PHP WordPress Course</title>' + new_html[end:]
        
        # Update meta description
        desc_text = clean_title.replace(':', '.').replace(' - ', '. ')
        if 'name="description"' in new_html:
            # Find the meta description tag
            meta_start = new_html.find('<meta content="')
            if meta_start > -1 and 'name="description"' in new_html[meta_start:meta_start+200]:
                meta_end = new_html.index('/>', meta_start) + 2
                new_html = (new_html[:meta_start] + 
                          f'<meta content="{desc_text}" name="description"/>' + 
                          new_html[meta_end:])
        
        # Update lesson header h1
        if '<header class="lesson-header">' in new_html:
            header_pos = new_html.index('<header class="lesson-header">')
            h1_start = new_html.index('<h1>', header_pos) + 4
            h1_end = new_html.index('</h1>', h1_start)
            new_html = new_html[:h1_start] + clean_title + new_html[h1_end:]
        
        # Fix class names in old content
        fixed_content = fix_class_names(old_content['content'])
        
        # Replace lesson body content
        if '<div class="lesson-body">' in new_html:
            body_start = new_html.index('<div class="lesson-body">') + 26
            
            # Find the closing div before Lesson Navigation
            nav_marker = '<!-- Lesson Navigation -->'
            if nav_marker in new_html:
                nav_pos = new_html.index(nav_marker)
                
                # Find the last </div> before the navigation marker
                search_text = new_html[body_start:nav_pos]
                last_div_pos = search_text.rfind('</div>')
                
                if last_div_pos > -1:
                    actual_end = body_start + last_div_pos
                    new_html = (new_html[:body_start] + '\n' + 
                              fixed_content + '\n            ' + 
                              new_html[actual_end:])
        
        # Add mermaid fix if needed
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
        print(f"Error: {e}")
        return False

def create_backup(directory):
    """Create a backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = directory.parent / f"{directory.name}_final_fix_backup_{timestamp}"
    
    try:
        shutil.copytree(str(directory), str(backup_dir))
        return backup_dir
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def main():
    """Main function to fix the remaining 8 files."""
    
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    old_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    
    # Check if directories exist
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        
        if not module_dir.exists():
            print("Error: Directories not found")
            return
    
    print("=" * 70)
    print(" Final Fix for Remaining 8 Files")
    print(" Using safe string operations instead of regex")
    print("=" * 70)
    print(f"Target: {module_dir}")
    print(f"Source: {old_module_dir}\n")
    
    # Optional backup
    response = input("Create backup? (y/n): ")
    if response.lower() == 'y':
        backup_dir = create_backup(module_dir)
        if backup_dir:
            print(f"✓ Backup created: {backup_dir.name}\n")
    
    print(f"Processing {len(PROBLEMATIC_FILES)} remaining files...")
    print("-" * 70)
    
    fixed = 0
    failed = 0
    
    for filename in PROBLEMATIC_FILES:
        new_file = module_dir / filename
        old_file = old_module_dir / filename
        
        print(f"  {filename:<55}", end=" ")
        
        if not new_file.exists():
            print("⚠️ New file not found")
            failed += 1
            continue
        
        if not old_file.exists():
            print("⚠️ Source file not found")
            failed += 1
            continue
        
        # Extract content from old file
        old_content = extract_content_from_old_file(old_file)
        
        if not old_content:
            print("✗ Could not extract content")
            failed += 1
            continue
        
        # Update new file
        if update_file_safely(new_file, old_content):
            print("✓ Fixed")
            fixed += 1
        else:
            print("✗ Failed to update")
            failed += 1
    
    print("\n" + "=" * 70)
    print("Final Summary:")
    print(f"  ✓ Successfully fixed: {fixed} files")
    if failed > 0:
        print(f"  ✗ Failed: {failed} files")
    
    if fixed > 0:
        print("\n✨ Files have been fixed using safe string operations!")
        print("   All content should now be properly populated.")

def create_manual_fix_script():
    """Create a script that manually fixes each file one by one."""
    
    script_content = '''#!/usr/bin/env python3
"""
Manual fix script that processes each problematic file individually.
This gives us maximum control over each file's specific issues.
"""

from pathlib import Path
import shutil
from datetime import datetime

def fix_file_manually(module_dir, old_module_dir, filename):
    """Manually fix a single file by direct copy and modification."""
    try:
        new_file = module_dir / filename
        old_file = old_module_dir / filename
        
        if not old_file.exists():
            return False, "Source file not found"
        
        # Read the old file
        with open(old_file, 'r', encoding='utf-8', errors='ignore') as f:
            old_content = f.read()
        
        # Read the new file structure
        with open(new_file, 'r', encoding='utf-8', errors='ignore') as f:
            new_structure = f.read()
        
        # Extract main content from old file
        main_start = old_content.find('<main>')
        main_end = old_content.find('</main>')
        
        if main_start == -1 or main_end == -1:
            return False, "Could not find main section"
        
        main_content = old_content[main_start + 6:main_end]
        
        # Remove header from main content
        if '<header>' in main_content:
            header_start = main_content.find('<header>')
            header_end = main_content.find('</header>')
            if header_end != -1:
                main_content = main_content[:header_start] + main_content[header_end + 9:]
        
        # Extract title
        title_start = old_content.find('<title>')
        title_end = old_content.find('</title>')
        title = "Untitled"
        if title_start != -1 and title_end != -1:
            title = old_content[title_start + 7:title_end]
            title = title.replace(' - PHP WordPress Course', '').strip()
        
        # Build new content
        result = new_structure
        
        # Replace title
        if '<title>' in result:
            t_start = result.find('<title>')
            t_end = result.find('</title>') + 8
            result = result[:t_start] + f'<title>{title} - PHP WordPress Course</title>' + result[t_end:]
        
        # Replace lesson header h1
        if '<header class="lesson-header">' in result:
            h_pos = result.find('<header class="lesson-header">')
            h1_start = result.find('<h1>', h_pos) + 4
            h1_end = result.find('</h1>', h1_start)
            result = result[:h1_start] + title + result[h1_end:]
        
        # Replace lesson body
        if '<div class="lesson-body">' in result:
            body_start = result.find('<div class="lesson-body">') + 26
            nav_pos = result.find('<!-- Lesson Navigation -->')
            
            if nav_pos != -1:
                # Find last </div> before navigation
                check_area = result[body_start:nav_pos]
                last_div = check_area.rfind('</div>')
                if last_div != -1:
                    actual_end = body_start + last_div
                    
                    # Fix class names
                    main_content = main_content.replace('_', '-')
                    
                    result = result[:body_start] + '\\n' + main_content + '\\n            ' + result[actual_end:]
        
        # Write result
        with open(new_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(result)
        
        return True, "Fixed"
        
    except Exception as e:
        return False, str(e)

def main():
    """Process each file individually."""
    
    files_to_fix = [
        'homework_php_calculator.html',
        'homework_php_create_contact_form_validation.html',
        'homework_php_create_library_custom_functions.html',
        'homework_php_grades.html',
        'php_form_validation_techniques.html',
        'php_inheritance.html',
        'php_namespaces.html',
        'review_php_setup.html'
    ]
    
    module_dir = Path(r"\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module")
    old_module_dir = Path(r"\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module_old")
    
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
    
    print("=" * 70)
    print(" Manual Fix for Remaining Files")
    print("=" * 70)
    
    fixed = 0
    failed = 0
    
    for filename in files_to_fix:
        print(f"Fixing {filename}...", end=" ")
        success, message = fix_file_manually(module_dir, old_module_dir, filename)
        
        if success:
            print(f"✓ {message}")
            fixed += 1
        else:
            print(f"✗ {message}")
            failed += 1
    
    print(f"\\nResults: {fixed} fixed, {failed} failed")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\manual_fix_final_8.py")
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\nAlso created manual fix script: {script_path.name}")
    print("You can run: python manual_fix_final_8.py")

if __name__ == "__main__":
    try:
        main()
        print("\n" + "-" * 70)
        create_manual_fix_script()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        input("\nPress Enter to exit...")
