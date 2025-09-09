#!/usr/bin/env python3
"""
Ultimate fix for the remaining 8 files.
This script directly copies content without using regex at all.
"""

from pathlib import Path
from datetime import datetime
import shutil

# The 8 files that need fixing
FILES_TO_FIX = [
    'homework_php_calculator.html',
    'homework_php_create_contact_form_validation.html',
    'homework_php_create_library_custom_functions.html',
    'homework_php_grades.html',
    'php_form_validation_techniques.html',
    'php_inheritance.html',
    'php_namespaces.html',
    'review_php_setup.html'
]

def extract_content_safely(old_file_path):
    """Extract content from old file using only string operations."""
    with open(old_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract title
    title = "Untitled"
    if '<title>' in content and '</title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>')
        if start < end:
            title = content[start:end].strip()
    
    # Extract main content  
    main_content = ""
    if '<main>' in content and '</main>' in content:
        start = content.find('<main>') + 6
        end = content.find('</main>')
        if start < end:
            main_content = content[start:end].strip()
            
            # Remove header section if present
            if '<header>' in main_content and '</header>' in main_content:
                h_start = main_content.find('<header>')
                h_end = main_content.find('</header>') + 9
                if h_start < h_end:
                    main_content = main_content[:h_start] + main_content[h_end:]
    
    # Check for mermaid
    has_mermaid = 'mermaid' in content.lower()
    
    # Fix class names using simple string replacement
    replacements = [
        ('class="best_practice"', 'class="best-practice"'),
        ('class="important_note"', 'class="important-note"'),
        ('class="real_world_example"', 'class="real-world-example"'),
        ('class="real_world"', 'class="real-world"'),
        ('class="code_example"', 'class="code-example"'),
        ('class="mermaid_diagram"', 'class="mermaid-diagram"'),
        ('class="output_example"', 'class="output-example"'),
        ('class="comparison_table"', 'class="comparison-table"'),
        ("class='best_practice'", 'class="best-practice"'),
        ("class='important_note'", 'class="important-note"'),
        ("class='real_world_example'", 'class="real-world-example"'),
    ]
    
    for old_str, new_str in replacements:
        main_content = main_content.replace(old_str, new_str)
    
    return {
        'title': title,
        'content': main_content,
        'has_mermaid': has_mermaid
    }

def rebuild_file(new_file_path, old_content):
    """Rebuild the file with new content."""
    # Read the template structure
    with open(new_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        template = f.read()
    
    # Clean the title
    title = old_content['title'].replace(' - PHP WordPress Course', '').strip()
    
    # Build the new file piece by piece
    result_parts = []
    current_pos = 0
    
    # Replace title
    if '<title>' in template:
        title_start = template.find('<title>')
        title_end = template.find('</title>') + 8
        result_parts.append(template[current_pos:title_start])
        result_parts.append(f'<title>{title} - PHP WordPress Course</title>')
        current_pos = title_end
    
    # Continue until we reach lesson header
    if '<header class="lesson-header">' in template:
        header_pos = template.find('<header class="lesson-header">', current_pos)
        result_parts.append(template[current_pos:header_pos])
        
        # Find and replace the h1
        h1_start = template.find('<h1>', header_pos) + 4
        h1_end = template.find('</h1>', h1_start)
        result_parts.append(template[header_pos:h1_start])
        result_parts.append(title)
        current_pos = h1_end
    
    # Continue until lesson body
    if '<div class="lesson-body">' in template:
        body_start = template.find('<div class="lesson-body">', current_pos)
        body_tag_end = body_start + 26
        result_parts.append(template[current_pos:body_tag_end])
        
        # Add the new content
        result_parts.append('\n')
        result_parts.append(old_content['content'])
        result_parts.append('\n            ')
        
        # Find where to continue from (after the old body content)
        nav_marker = '<!-- Lesson Navigation -->'
        if nav_marker in template:
            nav_pos = template.find(nav_marker, body_tag_end)
            # Find the last </div> before navigation
            search_area = template[body_tag_end:nav_pos]
            last_div = search_area.rfind('</div>')
            if last_div >= 0:
                current_pos = body_tag_end + last_div
    
    # Add the rest of the template
    result_parts.append(template[current_pos:])
    
    # Join all parts
    result = ''.join(result_parts)
    
    # Add mermaid fix if needed
    if old_content['has_mermaid'] and 'mermaid-universal-fix.js' not in result:
        result = result.replace(
            '</body>',
            '<script src="/assets/js/mermaid-universal-fix.js"></script>\n</body>'
        )
    
    # Write the result
    with open(new_file_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(result)
    
    return True

def main():
    """Main function."""
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    old_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    
    # Check directories
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        
        if not module_dir.exists():
            print("Error: Directories not found")
            return
    
    print("=" * 70)
    print(" Ultimate Fix for Remaining 8 Files")
    print(" Using direct string operations - no regex")
    print("=" * 70)
    print(f"Target: {module_dir}")
    print(f"Source: {old_module_dir}\n")
    
    # Optional backup
    response = input("Create backup? (y/n): ")
    if response.lower() == 'y':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = module_dir.parent / f"02module_ultimate_backup_{timestamp}"
        try:
            shutil.copytree(str(module_dir), str(backup_dir))
            print(f"✓ Backup created: {backup_dir.name}\n")
        except Exception as e:
            print(f"Backup failed: {e}")
            if input("Continue without backup? (y/n): ").lower() != 'y':
                return
    
    print(f"Processing {len(FILES_TO_FIX)} files...")
    print("-" * 70)
    
    fixed = 0
    failed = 0
    errors = []
    
    for filename in FILES_TO_FIX:
        new_file = module_dir / filename
        old_file = old_module_dir / filename
        
        print(f"  {filename:<55}", end=" ")
        
        try:
            if not new_file.exists():
                print("⚠️ Target file not found")
                failed += 1
                errors.append((filename, "Target file not found"))
                continue
            
            if not old_file.exists():
                print("⚠️ Source file not found")
                failed += 1
                errors.append((filename, "Source file not found"))
                continue
            
            # Extract content
            old_content = extract_content_safely(old_file)
            
            if not old_content or not old_content['content']:
                print("✗ No content extracted")
                failed += 1
                errors.append((filename, "Could not extract content"))
                continue
            
            # Rebuild file
            if rebuild_file(new_file, old_content):
                print("✓ Fixed")
                fixed += 1
            else:
                print("✗ Failed to rebuild")
                failed += 1
                errors.append((filename, "Rebuild failed"))
                
        except Exception as e:
            print(f"✗ Error: {str(e)[:30]}")
            failed += 1
            errors.append((filename, str(e)))
    
    print("\n" + "=" * 70)
    print("Final Results:")
    print(f"  ✓ Successfully fixed: {fixed} files")
    if failed > 0:
        print(f"  ✗ Failed: {failed} files")
        print("\nError details:")
        for filename, error in errors:
            print(f"    {filename}: {error}")
    
    if fixed > 0:
        print("\n✨ Files have been successfully fixed!")
        print("   The content has been populated without using regex operations.")
        print("   Please check the files in your browser to verify.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
    finally:
        input("\nPress Enter to exit...")
