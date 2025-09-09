#!/usr/bin/env python3
"""
Fixed Windows-compatible script to populate 02module files with content from 02module_old files.
This version has corrected path handling for Windows accessing WSL files.
"""

import os
import re
from pathlib import Path, WindowsPath
from datetime import datetime
import shutil
import sys

def get_base_path():
    """
    Get the base path for the project, with proper Windows/WSL path handling.
    """
    print("Detecting project path...")
    
    # Convert string paths to Path objects properly
    possible_paths = [
        # WSL paths from Windows - using raw strings and Path
        Path(r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress'),
        Path('//wsl$/Ubuntu/home/practicalace/projects/php_wordpress'),
        Path(r'\\wsl.localhost\Ubuntu\home\practicalace\projects\php_wordpress'),
        Path('//wsl.localhost/Ubuntu/home/practicalace/projects/php_wordpress'),
    ]
    
    # Add current directory if script is in project folder
    current_dir = Path.cwd()
    if (current_dir / '02module').exists():
        possible_paths.insert(0, current_dir)
    
    for path in possible_paths:
        try:
            if path.exists():
                module_02 = path / '02module'
                module_02_old = path / '02module_old'
                
                if module_02.exists() and module_02_old.exists():
                    # Verify there are HTML files
                    files_new = list(module_02.glob('*.html'))
                    files_old = list(module_02_old.glob('*.html'))
                    
                    if files_new and files_old:
                        print(f"✅ Found project at: {path}")
                        print(f"   - 02module has {len(files_new)} HTML files")
                        print(f"   - 02module_old has {len(files_old)} HTML files")
                        return path
        except Exception as e:
            continue
    
    # If not found automatically, ask user
    print("\n❌ Could not automatically find the project directory.")
    print("\nPlease enter the full path to the php_wordpress folder.")
    print("Examples:")
    print("  - For WSL: \\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress")
    print("  - For Windows: C:\\Users\\YourName\\projects\\php_wordpress")
    
    while True:
        user_path = input("\nPath (or 'quit' to exit): ").strip().strip('"').strip("'")
        
        if user_path.lower() == 'quit':
            sys.exit(0)
        
        if user_path:
            path = Path(user_path)
            if path.exists():
                module_02 = path / '02module'
                module_02_old = path / '02module_old'
                
                if module_02.exists() and module_02_old.exists():
                    print(f"✅ Valid project path: {path}")
                    return path
                else:
                    print(f"❌ Path exists but missing 02module or 02module_old directories")
            else:
                print(f"❌ Path does not exist: {path}")
        else:
            print("❌ Please enter a valid path")

def extract_old_content(old_file_path):
    """
    Extract the main content from an old module file.
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
            # Try to find sections directly if no main tag
            sections = re.findall(r'<section[^>]*>.*?</section>', content, re.DOTALL | re.IGNORECASE)
            if sections:
                return '\n\n'.join(sections)
            else:
                print(f"  Warning: No <main> tag or <section> tags found")
                return None
            
    except Exception as e:
        print(f"  Error reading file: {e}")
        return None

def update_new_file(new_file_path, old_content):
    """
    Update the new module file with content from the old file.
    """
    try:
        with open(new_file_path, 'r', encoding='utf-8') as f:
            new_file_content = f.read()
        
        # Find the lesson-body div content - try multiple patterns
        patterns = [
            r'(<div class="lesson-body">)(.*?)(</div>\s*<!-- Lesson Navigation -->)',
            r'(<div class="lesson-body">)(.*?)(</div>\s*<div class="lesson-navigation">)',
            r'(<div class="lesson-body">)(.*?)(</div>\s*</article>)',
            r'(<div class="lesson-body">)(.*?)(</div>)(?=\s*</)'  # More general pattern
        ]
        
        match = None
        for pattern in patterns:
            match = re.search(pattern, new_file_content, re.DOTALL)
            if match:
                break
        
        if match:
            # Replace the content between the lesson-body tags
            updated_content = (
                new_file_content[:match.start(2)] + 
                '\n' + old_content + '\n' + 
                new_file_content[match.end(2):]
            )
            
            # Write the updated content back to the file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True
        else:
            print(f"  Warning: Could not find lesson-body div")
            return False
            
    except Exception as e:
        print(f"  Error updating file: {e}")
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
            
            # Clean the title
            main_title = old_title
            for suffix in [' - PHP WordPress Course', ' - PHP Course', ' - Course']:
                main_title = main_title.replace(suffix, '')
            main_title = main_title.strip()
            
            # Update the page title
            new_content = re.sub(
                r'<title>.*?</title>',
                f'<title>{main_title} - PHP WordPress Course</title>',
                new_content,
                count=1
            )
            
            # Update the lesson header h1
            new_content = re.sub(
                r'(<header class="lesson-header">\s*<h1>)(.*?)(</h1>)',
                rf'\1{main_title}\3',
                new_content,
                count=1
            )
            
            # Write back
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    except Exception as e:
        # Silent fail - title update is not critical
        pass

def backup_current_files(base_path):
    """
    Create a backup of current 02module files before modification.
    """
    module_path = base_path / '02module'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = base_path / f'02module_backup_{timestamp}'
    
    print(f"\n📁 Creating backup at: {backup_path.name}")
    try:
        shutil.copytree(str(module_path), str(backup_path))
        print("✅ Backup created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def process_modules(base_path):
    """
    Process all module files, copying content from old to new.
    """
    old_module_path = base_path / '02module_old'
    new_module_path = base_path / '02module'
    
    # Get list of HTML files in old module directory
    old_files = list(old_module_path.glob('*.html'))
    
    print(f"\n📊 Found {len(old_files)} HTML files to process")
    print("=" * 60)
    
    successful = 0
    failed = 0
    skipped = 0
    
    for i, old_file in enumerate(sorted(old_files), 1):
        filename = old_file.name
        new_file = new_module_path / filename
        
        print(f"\n[{i}/{len(old_files)}] Processing: {filename}")
        
        # Check if corresponding new file exists
        if not new_file.exists():
            print(f"  ⏩ Skipping: No corresponding file in 02module")
            skipped += 1
            continue
        
        # Extract content from old file
        old_content = extract_old_content(old_file)
        
        if old_content is None:
            print(f"  ❌ Failed: Could not extract content")
            failed += 1
            continue
        
        # Update new file with old content
        if update_new_file(new_file, old_content):
            # Also update title and meta
            update_lesson_title_and_meta(new_file, old_file)
            print(f"  ✅ Success: Content populated")
            successful += 1
        else:
            print(f"  ❌ Failed: Could not update file")
            failed += 1
    
    return successful, failed, skipped

def fix_mermaid_diagrams(base_path):
    """
    Fix any Mermaid diagram issues in the populated files.
    """
    module_path = base_path / '02module'
    
    print("\n🔍 Checking for Mermaid diagrams...")
    
    files_with_mermaid = 0
    files_fixed = 0
    
    for html_file in module_path.glob('*.html'):
        try:
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
                    
                    files_fixed += 1
                    print(f"  🔧 Fixed Mermaid in: {html_file.name}")
        except Exception as e:
            pass
    
    if files_with_mermaid > 0:
        print(f"  📊 Found {files_with_mermaid} files with Mermaid diagrams")
        if files_fixed > 0:
            print(f"  ✅ Fixed {files_fixed} files")
    else:
        print("  ℹ️ No Mermaid diagrams found")

def main():
    """
    Main function to orchestrate the content population process.
    """
    print("\n" + "=" * 60)
    print("  PHP WordPress Module Content Population Script")
    print("  Windows Version - Fixed Path Handling")
    print("=" * 60)
    
    # Get the base path
    try:
        base_path = get_base_path()
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled by user")
        return
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        return
    
    # Create backup
    print("\n📦 Step 1: Creating backup...")
    if not backup_current_files(base_path):
        response = input("\n⚠️ Backup failed. Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("❌ Exiting...")
            return
    
    # Process files
    print("\n📝 Step 2: Populating content...")
    successful, failed, skipped = process_modules(base_path)
    
    # Fix Mermaid if needed
    if successful > 0:
        print("\n🎨 Step 3: Post-processing...")
        fix_mermaid_diagrams(base_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("  📊 SUMMARY")
    print("=" * 60)
    
    if successful > 0:
        print(f"  ✅ Successfully populated: {successful} files")
    if failed > 0:
        print(f"  ❌ Failed to populate: {failed} files")
    if skipped > 0:
        print(f"  ⏩ Skipped (no match): {skipped} files")
    
    print(f"\n  📁 Total processed: {successful + failed + skipped} files")
    
    if successful > 0:
        print("\n✨ SUCCESS! Your files have been populated.")
        print("\n📋 Next steps:")
        print("  1. Open a browser and check the populated content")
        print("  2. Verify code blocks and special characters display correctly")
        print("  3. Test navigation links between lessons")
        print("  4. Check any Mermaid diagrams render properly")
    
    if failed > 0:
        print("\n⚠️ Some files failed. You may need to manually copy their content.")
    
    print(f"\n💾 Backup saved - you can restore if needed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
    finally:
        print("\n")
        input("Press Enter to exit...")
