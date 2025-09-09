#!/usr/bin/env python3
"""
Preprocessor script to fix regex escape issues in 02module_old files.
This prepares the files so that fix_02module_missing_content.py can process them without errors.
The main issue is that backslashes in the content are being interpreted as regex escape sequences.
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

def fix_regex_escapes_in_content(content):
    """
    Fix problematic escape sequences in HTML content that cause regex errors.
    This function escapes backslashes properly to prevent regex interpretation issues.
    """
    # List of files that had errors and their specific escape sequences
    problematic_patterns = {
        # These are the escape sequences that caused errors
        r'\\x': r'\\\\x',  # Fix \x escapes
        r'\\s': r'\\\\s',  # Fix \s escapes  
        r'\\d': r'\\\\d',  # Fix \d escapes
        r'\\D': r'\\\\D',  # Fix \D escapes
        r'\\S': r'\\\\S',  # Fix \S escapes
        r'\\V': r'\\\\V',  # Fix \V escapes
        r'\\C': r'\\\\C',  # Fix \C escapes
        r'\\J': r'\\\\J',  # Fix \J escapes
        r'\\W': r'\\\\W',  # Fix \W escapes
    }
    
    # First, protect actual regex patterns in JavaScript/code blocks
    # by temporarily replacing them with placeholders
    code_blocks = []
    
    # Find and protect <code> blocks
    code_pattern = r'<code[^>]*>(.*?)</code>'
    def protect_code(match):
        code_blocks.append(match.group(0))
        return f'###CODE_BLOCK_{len(code_blocks)-1}###'
    
    content = re.sub(code_pattern, protect_code, content, flags=re.DOTALL)
    
    # Find and protect <pre> blocks
    pre_pattern = r'<pre[^>]*>(.*?)</pre>'
    def protect_pre(match):
        code_blocks.append(match.group(0))
        return f'###CODE_BLOCK_{len(code_blocks)-1}###'
    
    content = re.sub(pre_pattern, protect_pre, content, flags=re.DOTALL)
    
    # Now fix the escape sequences outside of code blocks
    # We need to escape backslashes that appear before regex metacharacters
    # But we must be careful not to double-escape already escaped backslashes
    
    # Replace single backslashes followed by regex metacharacters with double backslashes
    # This regex looks for a single backslash not preceded by another backslash
    # followed by common regex metacharacters
    
    # Fix specific problematic patterns that caused errors
    fixes = [
        (r'(?<!\\)\\x', r'\\\\x'),  # \x not preceded by \
        (r'(?<!\\)\\s', r'\\\\s'),  # \s not preceded by \
        (r'(?<!\\)\\d', r'\\\\d'),  # \d not preceded by \
        (r'(?<!\\)\\D', r'\\\\D'),  # \D not preceded by \
        (r'(?<!\\)\\S', r'\\\\S'),  # \S not preceded by \
        (r'(?<!\\)\\V', r'\\\\V'),  # \V not preceded by \
        (r'(?<!\\)\\C', r'\\\\C'),  # \C not preceded by \
        (r'(?<!\\)\\J', r'\\\\J'),  # \J not preceded by \
        (r'(?<!\\)\\W', r'\\\\W'),  # \W not preceded by \
        (r'(?<!\\)\\w', r'\\\\w'),  # \w not preceded by \
        (r'(?<!\\)\\b', r'\\\\b'),  # \b not preceded by \
        (r'(?<!\\)\\B', r'\\\\B'),  # \B not preceded by \
        (r'(?<!\\)\\A', r'\\\\A'),  # \A not preceded by \
        (r'(?<!\\)\\Z', r'\\\\Z'),  # \Z not preceded by \
    ]
    
    for pattern, replacement in fixes:
        try:
            content = re.sub(pattern, replacement, content)
        except:
            # If the pattern fails, try a simpler approach
            pass
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        content = content.replace(f'###CODE_BLOCK_{i}###', block)
    
    return content

def process_file(file_path):
    """
    Process a single file to fix regex escape issues.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this file likely has problematic escapes
        # Look for backslash followed by common regex metacharacters
        has_issues = any(seq in content for seq in [r'\x', r'\s', r'\d', r'\D', r'\S', r'\V', r'\C', r'\J', r'\W'])
        
        if not has_issues:
            return False, "No problematic escapes found"
        
        # Fix the content
        fixed_content = fix_regex_escapes_in_content(content)
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True, "Fixed regex escapes"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def create_backup(directory):
    """Create a backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = directory.parent / f"{directory.name}_preprocess_backup_{timestamp}"
    
    try:
        shutil.copytree(str(directory), str(backup_dir))
        return backup_dir
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def main():
    """Main function to preprocess files with regex issues."""
    
    # List of files that failed with regex errors
    failed_files = [
        'homework_php_calculator.html',
        'homework_php_create_contact_form_validation.html',
        'homework_php_create_library_custom_functions.html',
        'homework_php_grades.html',
        'php_abstract_classes.html',
        'php_access_modifiers.html',
        'php_accessing_form_data_get_post.html',
        'php_array_sorting.html',
        'php_built_in_php_functions_overview.html',
        'php_comments.html',
        'php_default_parameter_values.html',
        'php_form_validation_techniques.html',
        'php_html_forms_review.html',
        'php_implementing_user_input.html',
        'php_inheritance.html',
        'php_logical_operators.html',
        'php_multidimensional_arrays.html',
        'php_namespaces.html',
        'php_output_methods.html',
        'php_planning_php_application.html',
        'php_string_operators.html',
        'php_traits.html',
        'php_type_operators.html',
        'php_working_with_sessions_cookies.html',
        'review_php_setup.html'
    ]
    
    # Set up path
    old_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    
    # Check if directory exists
    if not old_module_dir.exists():
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        
        if not old_module_dir.exists():
            print("Error: 02module_old directory not found")
            return
    
    print("=" * 70)
    print(" Regex Escape Fix for Module 02 Old Files")
    print(" Preprocessing to fix regex escape issues")
    print("=" * 70)
    print(f"Directory: {old_module_dir}\n")
    
    # Create backup
    response = input("Create backup of 02module_old before preprocessing? (y/n): ")
    if response.lower() == 'y':
        backup_dir = create_backup(old_module_dir)
        if backup_dir:
            print(f"✓ Backup created: {backup_dir.name}\n")
        else:
            if input("Continue without backup? (y/n): ").lower() != 'y':
                return
    
    print(f"Processing {len(failed_files)} files that had regex errors...")
    print("-" * 70)
    
    fixed = 0
    already_ok = 0
    failed = 0
    
    for filename in failed_files:
        file_path = old_module_dir / filename
        
        if not file_path.exists():
            print(f"  {filename:<55} ⚠️ File not found")
            failed += 1
            continue
        
        print(f"  {filename:<55}", end=" ")
        
        success, message = process_file(file_path)
        
        if success:
            print(f"✓ {message}")
            fixed += 1
        elif "No problematic" in message:
            print(f"- {message}")
            already_ok += 1
        else:
            print(f"✗ {message}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("Preprocessing Summary:")
    print(f"  ✓ Fixed: {fixed} files")
    print(f"  - Already OK: {already_ok} files")
    if failed > 0:
        print(f"  ✗ Failed: {failed} files")
    
    if fixed > 0:
        print("\n✨ Files have been preprocessed to fix regex issues!")
        print("\nNext steps:")
        print("1. Run fix_02module_missing_content.py again")
        print("2. It should now be able to process all files without regex errors")
    
    return fixed > 0

def alternative_fix():
    """
    Alternative approach: Create a modified version of the main fix script
    that handles regex escapes better.
    """
    print("\nAlternative: Creating enhanced version of fix script...")
    
    script_content = '''#!/usr/bin/env python3
"""
Enhanced version of fix_02module_missing_content.py that handles regex escape issues.
This version properly escapes content before using it in regex replacements.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

def has_placeholder_content(file_path):
    """Check if a file has placeholder/generic content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
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
        
        placeholder_count = sum(1 for indicator in placeholder_indicators if indicator in content)
        
        if placeholder_count >= 3:
            return True
        
        lesson_body_match = re.search(r'<div class="lesson-body">(.*?)</div>\\s*<!-- Lesson Navigation -->', 
                                     content, re.DOTALL)
        if lesson_body_match:
            body_content = lesson_body_match.group(1)
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
        
        title_match = re.search(r'<title>(.*?)</title>', old_html, re.DOTALL)
        title = title_match.group(1) if title_match else "Untitled"
        
        main_match = re.search(r'<main>(.*?)</main>', old_html, re.DOTALL)
        main_content = main_match.group(1) if main_match else ""
        
        main_content = re.sub(r'<header>.*?</header>', '', main_content, flags=re.DOTALL)
        
        has_mermaid = 'mermaid' in old_html.lower()
        
        return {
            'title': title.strip(),
            'content': main_content.strip(),
            'has_mermaid': has_mermaid
        }
    except Exception as e:
        print(f"    Error extracting content: {e}")
        return None

def escape_for_regex_replacement(text):
    """Properly escape text for use in regex replacement."""
    # Escape backslashes and other special characters for regex replacement
    # This prevents interpretation of backslash sequences as regex escapes
    return text.replace('\\\\', '\\\\\\\\\\\\\\\\').replace('\\\\', '\\\\\\\\\\\\\\\\')

def update_file_content(new_file_path, old_content):
    """Update the new file with content from the old file."""
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_html = f.read()
        
        clean_title = old_content['title']
        for suffix in [' - PHP WordPress Course', ' - PHP Course', ' - Course']:
            clean_title = clean_title.replace(suffix, '')
        
        # Update title using string replacement instead of regex
        title_start = '<title>'
        title_end = '</title>'
        if title_start in new_html and title_end in new_html:
            start_idx = new_html.index(title_start) + len(title_start)
            end_idx = new_html.index(title_end, start_idx)
            new_html = new_html[:start_idx] + f'{clean_title} - PHP WordPress Course' + new_html[end_idx:]
        
        # Update lesson header h1 using string replacement
        header_marker = '<header class="lesson-header">'
        if header_marker in new_html:
            header_start = new_html.index(header_marker)
            h1_start = new_html.index('<h1>', header_start) + 4
            h1_end = new_html.index('</h1>', h1_start)
            new_html = new_html[:h1_start] + clean_title + new_html[h1_end:]
        
        # Fix class names in old content
        fixed_content = old_content['content']
        fixed_content = re.sub(r'class="([^"]*?)_([^"]*?)"', r'class="\\1-\\2"', fixed_content)
        fixed_content = re.sub(r"class='([^']*?)_([^']*?)'", r"class='\\1-\\2'", fixed_content)
        
        # Replace lesson body content using string operations instead of regex
        body_start_marker = '<div class="lesson-body">'
        body_end_marker = '</div>\\n<!-- Lesson Navigation -->'
        
        if body_start_marker in new_html:
            # Find the start and end positions
            body_start = new_html.index(body_start_marker) + len(body_start_marker)
            
            # Search for the end marker
            nav_comment = '<!-- Lesson Navigation -->'
            if nav_comment in new_html:
                # Find the </div> just before the navigation comment
                nav_pos = new_html.index(nav_comment)
                # Search backwards for the last </div> before the comment
                search_pos = nav_pos - 1
                while search_pos > body_start:
                    if new_html[search_pos:search_pos+6] == '</div>':
                        body_end = search_pos
                        break
                    search_pos -= 1
                
                # Replace the content
                new_html = new_html[:body_start] + '\\n' + fixed_content + '\\n            ' + new_html[body_end:]
        
        # Add mermaid fix script if needed
        if old_content['has_mermaid'] and 'mermaid-universal-fix.js' not in new_html:
            new_html = new_html.replace(
                '</body>',
                '<script src="/assets/js/mermaid-universal-fix.js"></script>\\n</body>'
            )
        
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
    
    module_dir = Path(r"\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module")
    old_module_dir = Path(r"\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module_old")
    
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        
        if not module_dir.exists():
            print("Error: 02module directory not found")
            return
    
    print("=" * 70)
    print(" Enhanced Content Fix for Module 02")
    print(" With improved regex escape handling")
    print("=" * 70)
    print(f"Checking: {module_dir}")
    print(f"Source: {old_module_dir}\\n")
    
    response = input("Create backup before proceeding? (y/n): ")
    if response.lower() == 'y':
        backup_dir = create_backup(module_dir)
        if backup_dir:
            print(f"✓ Backup created: {backup_dir.name}\\n")
        else:
            if input("Continue without backup? (y/n): ").lower() != 'y':
                return
    
    html_files = list(module_dir.glob("*.html"))
    print(f"Found {len(html_files)} HTML files\\n")
    
    print("Analyzing files for placeholder content...")
    print("-" * 70)
    
    files_needing_fix = []
    files_already_ok = []
    files_no_source = []
    
    for file_path in sorted(html_files):
        print(f"Checking: {file_path.name:<50}", end=" ")
        
        if has_placeholder_content(file_path):
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
    
    print("\\n" + "=" * 70)
    print("Analysis Results:")
    print(f"  ✓ Files with real content: {len(files_already_ok)}")
    print(f"  ❌ Files needing fix: {len(files_needing_fix)}")
    print(f"  ⚠️ Files with no source: {len(files_no_source)}")
    
    if files_needing_fix:
        print(f"\\nFiles that need fixing:")
        for file_path, _ in files_needing_fix:
            print(f"  - {file_path.name}")
        
        print("\\n" + "-" * 70)
        response = input(f"\\nFix {len(files_needing_fix)} files? (y/n): ")
        
        if response.lower() == 'y':
            print("\\nFixing files...")
            fixed = 0
            failed = 0
            
            for new_file, old_file in files_needing_fix:
                print(f"  Fixing: {new_file.name:<50}", end=" ")
                
                old_content = extract_old_content(old_file)
                
                if old_content:
                    if update_file_content(new_file, old_content):
                        print("✓ Fixed")
                        fixed += 1
                    else:
                        print("✗ Failed to update")
                        failed += 1
                else:
                    print("✗ Could not extract content")
                    failed += 1
            
            print("\\n" + "=" * 70)
            print("Fix Summary:")
            print(f"  ✓ Successfully fixed: {fixed} files")
            if failed > 0:
                print(f"  ✗ Failed to fix: {failed} files")
            
            if fixed > 0:
                print("\\n✨ Files have been populated with their actual content!")
                print("   Please review the changes in your browser.")
    else:
        print("\\n✨ Great news! All files already have real content.")
        print("   No fixes needed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\nProcess interrupted by user")
    except Exception as e:
        print(f"\\n\\nError: {e}")
    finally:
        input("\\nPress Enter to exit...")
'''
    
    # Write the enhanced script
    script_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\fix_02module_enhanced_regex.py")
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"✓ Created enhanced script: {script_path.name}")
        print("\nYou can now run: python fix_02module_enhanced_regex.py")
        return True
    except Exception as e:
        print(f"✗ Failed to create enhanced script: {e}")
        return False

if __name__ == "__main__":
    try:
        print("\nThis script will fix regex escape issues in 02module_old files")
        print("so that fix_02module_missing_content.py can process them.\n")
        
        success = main()
        
        if not success:
            print("\nTrying alternative approach...")
            alternative_fix()
            
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        input("\nPress Enter to exit...")
