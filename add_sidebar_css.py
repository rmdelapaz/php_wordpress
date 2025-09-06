#!/usr/bin/env python3
"""
Script to add the enhanced sidebar CSS to Module 1 HTML files.
This should be run AFTER fix_01module_navigation.py
"""

import os
from bs4 import BeautifulSoup

def add_css_to_file(filepath):
    """Add the enhanced sidebar CSS link to an HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if the CSS is already linked
        existing_link = soup.find('link', {'href': '/assets/css/sidebar-enhanced.css'})
        if existing_link:
            print(f"  ✓ CSS already linked in {os.path.basename(filepath)}")
            return True
        
        # Find the head tag
        head = soup.find('head')
        if not head:
            print(f"  ✗ No head tag found in {os.path.basename(filepath)}")
            return False
        
        # Create the new link tag
        new_link = soup.new_tag('link')
        new_link['rel'] = 'stylesheet'
        new_link['href'] = '/assets/css/sidebar-enhanced.css'
        
        # Add comment before the link
        comment = soup.new_string('Enhanced sidebar styling', soup.Comment)
        
        # Find the last CSS link or add after main.css
        main_css = soup.find('link', {'href': '/assets/css/main.css'})
        if main_css:
            # Add after main.css
            main_css.insert_after(new_link)
            new_link.insert_before(comment)
        else:
            # Add at the end of head
            head.append(comment)
            head.append(new_link)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  ✓ Added CSS link to {os.path.basename(filepath)}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def main():
    """Add enhanced CSS to all Module 1 files."""
    
    # Define paths - handle both Windows and WSL paths
    if os.path.exists(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module"):
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
    elif os.path.exists("/home/practicalace/projects/php_wordpress/01module"):
        base_path = "/home/practicalace/projects/php_wordpress"
    else:
        base_path = os.getcwd()
    
    module01_dir = os.path.join(base_path, "01module")
    
    print("=" * 60)
    print("Adding Enhanced Sidebar CSS to Module 1")
    print("=" * 60)
    
    # Check if CSS file exists
    css_file = os.path.join(base_path, "assets", "css", "sidebar-enhanced.css")
    if not os.path.exists(css_file):
        print(f"\n⚠ Warning: CSS file not found at {css_file}")
        print("Make sure sidebar-enhanced.css is in the assets/css directory")
        return
    
    print(f"\n✓ Found CSS file: {css_file}")
    
    # Get all HTML files
    if not os.path.exists(module01_dir):
        print(f"\n✗ Module 1 directory not found: {module01_dir}")
        return
    
    html_files = [f for f in os.listdir(module01_dir) if f.endswith('.html')]
    
    if not html_files:
        print(f"\n✗ No HTML files found in {module01_dir}")
        return
    
    print(f"\nProcessing {len(html_files)} HTML files...")
    print("-" * 60)
    
    success_count = 0
    for filename in html_files:
        filepath = os.path.join(module01_dir, filename)
        if add_css_to_file(filepath):
            success_count += 1
    
    print("-" * 60)
    print(f"\n✅ Successfully processed {success_count}/{len(html_files)} files")
    
    if success_count == len(html_files):
        print("\n✨ All files now have enhanced sidebar styling!")
    
    print("\nNote: Make sure to clear your browser cache to see the changes.")

if __name__ == "__main__":
    main()
