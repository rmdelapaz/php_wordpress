#!/usr/bin/env python3
"""
Script to fix the side navigation in 01module HTML files to match the consistent
functionality found in 02module and 03module files.
"""

import os
import re
from bs4 import BeautifulSoup
import sys

def get_module_files(module_dir):
    """Get all HTML files in a module directory."""
    files = []
    if os.path.exists(module_dir):
        for file in os.listdir(module_dir):
            if file.endswith('.html'):
                files.append(os.path.join(module_dir, file))
    return sorted(files)

def extract_navigation_from_reference(reference_file):
    """Extract the navigation structure from a reference file (02 or 03 module)."""
    try:
        with open(reference_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the sidebar navigation
        sidebar_nav = soup.find('div', class_='sidebar-nav')
        if sidebar_nav:
            return str(sidebar_nav)
        else:
            print(f"Warning: Could not find sidebar-nav in {reference_file}")
            return None
    except Exception as e:
        print(f"Error reading reference file {reference_file}: {e}")
        return None

def create_01module_navigation():
    """Create the proper navigation structure for Module 1."""
    navigation_html = '''<div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: Web Fundamentals</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Lessons</h4>
                                <ul class="sidebar-menu">
                                    <li><a href="/01module/course_introduction.html" class="sidebar-link">1.1 Course Introduction</a></li>
                                    <li><a href="/01module/first_html_page.html" class="sidebar-link">1.2 Your First HTML Page</a></li>
                                    <li><a href="/01module/introduction_to_css.html" class="sidebar-link">1.3 Introduction to CSS</a></li>
                                    <li><a href="/01module/js_intro.html" class="sidebar-link">1.4 JavaScript Introduction</a></li>
                                    <li><a href="/01module/php_and_wordpress.html" class="sidebar-link">1.5 PHP and WordPress Overview</a></li>
                                    <li><a href="/01module/php_header_footer.html" class="sidebar-link">1.6 PHP Headers and Footers</a></li>
                                    <li><a href="/01module/project_static_site.html" class="sidebar-link">1.7 Project: Static Website</a></li>
                                </ul>
                            </div>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Module Resources</h4>
                                <ul class="sidebar-menu">
                                    <li><a href="/module1.html" class="sidebar-link">Module Overview</a></li>
                                    <li><a href="/resources.html" class="sidebar-link">Additional Resources</a></li>
                                </ul>
                            </div>
                        </div>'''
    return navigation_html

def get_current_page_from_file(filepath):
    """Determine which page is current based on the filename."""
    filename = os.path.basename(filepath)
    page_map = {
        'course_introduction.html': '1.1 Course Introduction',
        'first_html_page.html': '1.2 Your First HTML Page',
        'introduction_to_css.html': '1.3 Introduction to CSS',
        'js_intro.html': '1.4 JavaScript Introduction',
        'php_and_wordpress.html': '1.5 PHP and WordPress Overview',
        'php_header_footer.html': '1.6 PHP Headers and Footers',
        'project_static_site.html': '1.7 Project: Static Website'
    }
    return page_map.get(filename, '')

def update_navigation_with_active(navigation_html, current_page):
    """Add the 'active' class to the current page in navigation."""
    if not current_page:
        return navigation_html
    
    # Parse the navigation HTML
    soup = BeautifulSoup(navigation_html, 'html.parser')
    
    # Find all sidebar links
    links = soup.find_all('a', class_='sidebar-link')
    for link in links:
        link_text = link.get_text(strip=True)
        if link_text == current_page:
            # Add active class
            current_classes = link.get('class', [])
            if 'active' not in current_classes:
                current_classes.append('active')
                link['class'] = current_classes
        else:
            # Remove active class if present
            current_classes = link.get('class', [])
            if 'active' in current_classes:
                current_classes.remove('active')
                link['class'] = current_classes
    
    return str(soup)

def fix_navigation_in_file(filepath, navigation_template):
    """Fix the navigation in a single HTML file."""
    try:
        print(f"Processing: {filepath}")
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the sidebar nav
        sidebar_nav = soup.find('div', class_='sidebar-nav')
        
        if not sidebar_nav:
            # Try to find the sidebar container
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                # Clear existing content and add new navigation
                sidebar.clear()
                new_nav = BeautifulSoup(navigation_template, 'html.parser')
                sidebar.append(new_nav)
                print(f"  ✓ Added navigation structure to sidebar")
            else:
                print(f"  ⚠ Warning: No sidebar found in {filepath}")
                return False
        else:
            # Replace existing navigation
            parent = sidebar_nav.parent
            sidebar_nav.decompose()
            new_nav = BeautifulSoup(navigation_template, 'html.parser')
            parent.append(new_nav)
            print(f"  ✓ Replaced existing navigation")
        
        # Get the current page and update active state
        current_page = get_current_page_from_file(filepath)
        if current_page:
            # Find the newly added sidebar-nav and update it
            sidebar_nav = soup.find('div', class_='sidebar-nav')
            if sidebar_nav:
                updated_nav = update_navigation_with_active(str(sidebar_nav), current_page)
                new_sidebar_nav = BeautifulSoup(updated_nav, 'html.parser').find('div', class_='sidebar-nav')
                sidebar_nav.replace_with(new_sidebar_nav)
                print(f"  ✓ Set active state for: {current_page}")
        
        # Write the updated content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  ✓ Successfully updated {os.path.basename(filepath)}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def analyze_current_navigation(module_dir):
    """Analyze the current state of navigation in module files."""
    print("\n=== Analyzing Current Navigation Structure ===\n")
    
    files = get_module_files(module_dir)
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"\n{filename}:")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for sidebar
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                print("  ✓ Has sidebar")
                
                # Check for sidebar-nav
                sidebar_nav = soup.find('div', class_='sidebar-nav')
                if sidebar_nav:
                    print("  ✓ Has sidebar-nav")
                    
                    # Check for proper structure
                    sidebar_title = sidebar_nav.find('h3', class_='sidebar-title')
                    if sidebar_title:
                        print(f"    Title: {sidebar_title.get_text(strip=True)}")
                    
                    # Count sidebar sections
                    sections = sidebar_nav.find_all('div', class_='sidebar-section')
                    print(f"    Sections: {len(sections)}")
                    
                    # Count links
                    links = sidebar_nav.find_all('a', class_='sidebar-link')
                    print(f"    Links: {len(links)}")
                    
                    # Check for active link
                    active_links = sidebar_nav.find_all('a', class_='sidebar-link active')
                    if active_links:
                        for link in active_links:
                            print(f"    Active: {link.get_text(strip=True)}")
                    else:
                        print("    ⚠ No active link")
                else:
                    print("  ⚠ Missing sidebar-nav structure")
            else:
                print("  ✗ No sidebar found")
                
        except Exception as e:
            print(f"  ✗ Error analyzing: {e}")

def main():
    """Main function to fix navigation in all 01module files."""
    
    # Define paths - handle both Windows and WSL paths
    if os.path.exists(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module"):
        # Windows path to WSL
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
        print(f"Using Windows WSL path: {base_path}")
    elif os.path.exists("/home/practicalace/projects/php_wordpress/01module"):
        # Direct WSL/Linux path
        base_path = "/home/practicalace/projects/php_wordpress"
        print(f"Using Linux path: {base_path}")
    else:
        # Try current directory
        base_path = os.getcwd()
        print(f"Using current directory: {base_path}")
        
    module01_dir = os.path.join(base_path, "01module")
    module02_dir = os.path.join(base_path, "02module")
    module03_dir = os.path.join(base_path, "03module")
    
    print(f"\nLooking for Module 1 files in: {module01_dir}")
    print(f"Directory exists: {os.path.exists(module01_dir)}")
    
    if os.path.exists(module01_dir):
        files_in_dir = os.listdir(module01_dir)
        print(f"Files found in directory: {len(files_in_dir)}")
        html_files = [f for f in files_in_dir if f.endswith('.html')]
        print(f"HTML files found: {len(html_files)}")
        if html_files:
            print(f"First few HTML files: {html_files[:3]}...")
    
    print("=" * 60)
    print("Module 1 Navigation Fixer")
    print("=" * 60)
    
    # First, analyze current state
    print("\nStep 1: Analyzing current Module 1 navigation...")
    analyze_current_navigation(str(module01_dir))
    
    # Create the proper navigation structure for Module 1
    print("\n" + "=" * 60)
    print("\nStep 2: Creating proper navigation structure for Module 1...")
    navigation_template = create_01module_navigation()
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nDo you want to proceed with fixing the navigation? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Process all Module 1 HTML files
    print("\n" + "=" * 60)
    print("\nStep 3: Updating Module 1 files...")
    print("=" * 60 + "\n")
    
    files = get_module_files(str(module01_dir))
    
    if not files:
        print(f"No HTML files found in {module01_dir}")
        return
    
    success_count = 0
    fail_count = 0
    
    for filepath in files:
        # Get the current page for this file
        current_page = get_current_page_from_file(filepath)
        
        # Create navigation with active state for this specific file
        nav_with_active = update_navigation_with_active(navigation_template, current_page)
        
        # Fix the navigation
        if fix_navigation_in_file(filepath, nav_with_active):
            success_count += 1
        else:
            fail_count += 1
        print()  # Empty line for readability
    
    # Summary
    print("=" * 60)
    print("\nSummary:")
    print(f"  ✓ Successfully updated: {success_count} files")
    if fail_count > 0:
        print(f"  ✗ Failed: {fail_count} files")
    print("\n✅ Navigation fix complete!")
    
    # Final analysis
    print("\n" + "=" * 60)
    print("\nStep 4: Verifying changes...")
    analyze_current_navigation(str(module01_dir))

if __name__ == "__main__":
    main()
