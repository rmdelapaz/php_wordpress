#!/usr/bin/env python3
"""
Script to consolidate session HTML files from 07module, 08module, and 09module 
into 06module folder and update breadcrumb paths in the moved files.
"""

import os
import re
import shutil
from pathlib import Path

def get_wsl_path():
    """Get the base WSL path for the project"""
    # For Windows WSL path
    return Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress")

def move_html_files(source_folder, dest_folder):
    """Move all HTML files from source to destination folder"""
    moved_files = []
    
    if not source_folder.exists():
        print(f"Source folder {source_folder} does not exist")
        return moved_files
    
    # Create destination if it doesn't exist
    dest_folder.mkdir(parents=True, exist_ok=True)
    
    # Find and move all HTML files
    for html_file in source_folder.glob("*.html"):
        dest_file = dest_folder / html_file.name
        
        # Check if file already exists in destination
        if dest_file.exists():
            print(f"  ⚠️  File {html_file.name} already exists in destination, skipping...")
            continue
            
        try:
            shutil.move(str(html_file), str(dest_file))
            moved_files.append((html_file.name, dest_file))
            print(f"  ✓ Moved: {html_file.name}")
        except Exception as e:
            print(f"  ✗ Error moving {html_file.name}: {e}")
    
    return moved_files

def update_breadcrumbs(file_path):
    """Update breadcrumb paths in HTML file"""
    updates_made = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update breadcrumb links from /07module/, /08module/, /09module/ to /06module/
        patterns = [
            (r'<a href="/07module/', '<a href="/06module/'),
            (r'<a href="/08module/', '<a href="/06module/'),
            (r'<a href="/09module/', '<a href="/06module/'),
        ]
        
        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                updates_made.append(f"Updated links: {old_pattern} -> {new_pattern}")
        
        # Update breadcrumb text that might reference module numbers
        # This is for breadcrumb items that show the current location
        breadcrumb_patterns = [
            (r'<li class="breadcrumb-item">Session 7:', '<li class="breadcrumb-item">Module 6 - Session 7:'),
            (r'<li class="breadcrumb-item">Session 8:', '<li class="breadcrumb-item">Module 6 - Session 8:'),
            (r'<li class="breadcrumb-item">Session 9:', '<li class="breadcrumb-item">Module 6 - Session 9:'),
        ]
        
        for old_text, new_text in breadcrumb_patterns:
            if old_text in content:
                content = content.replace(old_text, new_text)
                updates_made.append(f"Updated breadcrumb text: {old_text}")
        
        # Update sidebar links that reference other files in the same module
        sidebar_patterns = [
            (r'href="/07module/', 'href="/06module/'),
            (r'href="/08module/', 'href="/06module/'),
            (r'href="/09module/', 'href="/06module/'),
        ]
        
        for old_href, new_href in sidebar_patterns:
            if old_href in content:
                content = content.replace(old_href, new_href)
                updates_made.append(f"Updated sidebar links: {old_href} -> {new_href}")
        
        # Update navigation links (Previous/Next buttons)
        nav_patterns = [
            (r'href="/07module/', 'href="/06module/'),
            (r'href="/08module/', 'href="/06module/'),
            (r'href="/09module/', 'href="/06module/'),
        ]
        
        for old_nav, new_nav in nav_patterns:
            count = content.count(old_nav)
            if count > 0:
                content = content.replace(old_nav, new_nav)
                updates_made.append(f"Updated {count} navigation links: {old_nav} -> {new_nav}")
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return updates_made
        
    except Exception as e:
        print(f"    Error updating breadcrumbs in {file_path.name}: {e}")
        return []
    
    return []

def main():
    """Main function to coordinate the move and update operations"""
    print("=" * 60)
    print("HTML File Consolidation Script")
    print("=" * 60)
    
    base_path = get_wsl_path()
    
    # Define source and destination folders
    source_folders = ['07module', '08module', '09module']
    dest_folder = base_path / '06module'
    
    all_moved_files = []
    
    # Process each source folder
    for source_folder_name in source_folders:
        source_folder = base_path / source_folder_name
        print(f"\nProcessing {source_folder_name}:")
        print("-" * 40)
        
        # Move files
        moved_files = move_html_files(source_folder, dest_folder)
        all_moved_files.extend(moved_files)
        
        if moved_files:
            print(f"  Moved {len(moved_files)} files from {source_folder_name}")
        else:
            print(f"  No files to move from {source_folder_name}")
    
    # Update breadcrumbs in all moved files
    if all_moved_files:
        print("\n" + "=" * 60)
        print("Updating breadcrumbs and links in moved files:")
        print("-" * 40)
        
        for filename, file_path in all_moved_files:
            print(f"\n  Processing: {filename}")
            updates = update_breadcrumbs(file_path)
            
            if updates:
                for update in updates:
                    print(f"    • {update}")
            else:
                print(f"    • No updates needed")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files moved: {len(all_moved_files)}")
    print(f"Destination: {dest_folder}")
    print("\nFolders kept (now empty):")
    for folder in source_folders:
        folder_path = base_path / folder
        if folder_path.exists():
            file_count = len(list(folder_path.glob("*.html")))
            print(f"  • {folder} ({file_count} HTML files remaining)")
    
    print("\n✅ Script completed successfully!")
    
    # Offer to display moved files list
    if all_moved_files:
        print("\nMoved files:")
        for filename, _ in all_moved_files:
            print(f"  • {filename}")

if __name__ == "__main__":
    main()