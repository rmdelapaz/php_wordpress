#!/usr/bin/env python3
"""
Script to compare navigation structures across different modules.
This helps identify inconsistencies between module navigation implementations.
"""

import os
from bs4 import BeautifulSoup
import json

def analyze_module_navigation(module_dir, module_name):
    """Analyze navigation structure in a module's files."""
    results = {
        'module': module_name,
        'files': {},
        'summary': {
            'total_files': 0,
            'files_with_sidebar': 0,
            'files_with_proper_nav': 0,
            'navigation_structures': []
        }
    }
    
    if not os.path.exists(module_dir):
        print(f"Warning: Module directory {module_dir} does not exist")
        return results
    
    # Get all HTML files
    html_files = [f for f in os.listdir(module_dir) if f.endswith('.html')]
    results['summary']['total_files'] = len(html_files)
    
    for filename in sorted(html_files):
        filepath = os.path.join(module_dir, filename)
        file_info = {
            'has_sidebar': False,
            'has_sidebar_nav': False,
            'sidebar_structure': None,
            'navigation_items': [],
            'active_items': [],
            'issues': []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for sidebar
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                file_info['has_sidebar'] = True
                results['summary']['files_with_sidebar'] += 1
                
                # Check for sidebar-nav
                sidebar_nav = soup.find('div', class_='sidebar-nav')
                if sidebar_nav:
                    file_info['has_sidebar_nav'] = True
                    results['summary']['files_with_proper_nav'] += 1
                    
                    # Extract structure
                    structure = {
                        'title': '',
                        'sections': []
                    }
                    
                    # Get title
                    title = sidebar_nav.find('h3', class_='sidebar-title')
                    if title:
                        structure['title'] = title.get_text(strip=True)
                    else:
                        file_info['issues'].append('Missing sidebar title')
                    
                    # Get sections
                    sections = sidebar_nav.find_all('div', class_='sidebar-section')
                    for section in sections:
                        section_info = {
                            'title': '',
                            'links': []
                        }
                        
                        section_title = section.find('h4', class_='sidebar-section-title')
                        if section_title:
                            section_info['title'] = section_title.get_text(strip=True)
                        
                        # Get links
                        links = section.find_all('a', class_='sidebar-link')
                        for link in links:
                            link_info = {
                                'text': link.get_text(strip=True),
                                'href': link.get('href', ''),
                                'active': 'active' in link.get('class', [])
                            }
                            section_info['links'].append(link_info)
                            file_info['navigation_items'].append(link_info['text'])
                            
                            if link_info['active']:
                                file_info['active_items'].append(link_info['text'])
                        
                        structure['sections'].append(section_info)
                    
                    file_info['sidebar_structure'] = structure
                    
                    # Check for common issues
                    if len(file_info['active_items']) == 0:
                        file_info['issues'].append('No active navigation item')
                    elif len(file_info['active_items']) > 1:
                        file_info['issues'].append('Multiple active navigation items')
                    
                    # Store unique structure
                    structure_json = json.dumps(structure, sort_keys=True)
                    if structure_json not in results['summary']['navigation_structures']:
                        results['summary']['navigation_structures'].append(structure_json)
                else:
                    file_info['issues'].append('Sidebar exists but missing sidebar-nav structure')
            else:
                file_info['issues'].append('No sidebar found')
        
        except Exception as e:
            file_info['issues'].append(f'Error reading file: {str(e)}')
        
        results['files'][filename] = file_info
    
    return results

def compare_modules(module_results):
    """Compare navigation structures across modules."""
    print("\n" + "=" * 80)
    print("NAVIGATION STRUCTURE COMPARISON")
    print("=" * 80)
    
    for result in module_results:
        module_name = result['module']
        summary = result['summary']
        
        print(f"\n{module_name}:")
        print(f"  Total HTML files: {summary['total_files']}")
        print(f"  Files with sidebar: {summary['files_with_sidebar']}")
        print(f"  Files with proper nav structure: {summary['files_with_proper_nav']}")
        print(f"  Unique navigation structures: {len(summary['navigation_structures'])}")
        
        # Show issues
        issues_count = {}
        for filename, file_info in result['files'].items():
            for issue in file_info['issues']:
                if issue not in issues_count:
                    issues_count[issue] = 0
                issues_count[issue] += 1
        
        if issues_count:
            print("  Issues found:")
            for issue, count in sorted(issues_count.items()):
                print(f"    - {issue}: {count} file(s)")
    
    print("\n" + "=" * 80)
    print("DETAILED FILE ANALYSIS")
    print("=" * 80)
    
    for result in module_results:
        module_name = result['module']
        print(f"\n{module_name} Files:")
        
        for filename in sorted(result['files'].keys()):
            file_info = result['files'][filename]
            status = "✓" if file_info['has_sidebar_nav'] and not file_info['issues'] else "⚠"
            print(f"  {status} {filename}")
            
            if file_info['active_items']:
                print(f"      Active: {', '.join(file_info['active_items'])}")
            
            if file_info['issues']:
                for issue in file_info['issues']:
                    print(f"      Issue: {issue}")

def print_recommended_structure():
    """Print the recommended navigation structure."""
    print("\n" + "=" * 80)
    print("RECOMMENDED NAVIGATION STRUCTURE FOR MODULE 1")
    print("=" * 80)
    print("""
<aside class="sidebar">
    <div class="sidebar-nav">
        <h3 class="sidebar-title">Module 1: Web Fundamentals</h3>
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Module Sessions</h4>
            <ul class="sidebar-menu">
                <li><a href="/01module/course_introduction.html" class="sidebar-link [active]">
                    <span class="session-number">1</span> Course Introduction
                </a></li>
                <li><a href="/01module/first_html_page.html" class="sidebar-link">
                    <span class="session-number">2</span> Your First HTML Page
                </a></li>
                <li><a href="/01module/introduction_to_css.html" class="sidebar-link">
                    <span class="session-number">3</span> Introduction to CSS
                </a></li>
                <li><a href="/01module/js_intro.html" class="sidebar-link">
                    <span class="session-number">4</span> JavaScript Introduction
                </a></li>
                <li><a href="/01module/php_and_wordpress.html" class="sidebar-link">
                    <span class="session-number">5</span> PHP and WordPress Overview
                </a></li>
                <li><a href="/01module/php_header_footer.html" class="sidebar-link">
                    <span class="session-number">6</span> PHP Headers and Footers
                </a></li>
                <li><a href="/01module/project_static_site.html" class="sidebar-link">
                    <span class="session-number">7</span> Project: Static Website
                </a></li>
            </ul>
        </div>
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Quick Links</h4>
            <ul class="sidebar-menu">
                <li><a href="/module1.html" class="sidebar-link">Module Overview</a></li>
                <li><a href="/02module/review_php_setup.html" class="sidebar-link next-lesson">Next: PHP Setup →</a></li>
                <li><a href="/resources.html" class="sidebar-link">Resources</a></li>
            </ul>
        </div>
    </div>
</aside>

Key Improvements:
- Session numbers (1-7) instead of module.lesson format (1.1-1.7)
- Cleaner visual with session numbers in styled spans
- "Module Sessions" header is clearer
- "Quick Links" section with Next Module link for easy progression
- The [active] class should be added dynamically to the current page's link.
    """)

def main():
    """Main function to compare navigation across modules."""
    
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
    
    modules = [
        ('01module', 'Module 1: Web Fundamentals'),
        ('02module', 'Module 2: PHP Fundamentals'),
        ('03module', 'Module 3: MySQL Database')
    ]
    
    print("=" * 80)
    print("MODULE NAVIGATION STRUCTURE ANALYZER")
    print("=" * 80)
    
    # Analyze each module
    module_results = []
    for module_dir, module_name in modules:
        module_path = os.path.join(base_path, module_dir)
        print(f"\nAnalyzing {module_name}...")
        print(f"  Path: {module_path}")
        print(f"  Exists: {os.path.exists(module_path)}")
        results = analyze_module_navigation(module_path, module_name)
        module_results.append(results)
    
    # Compare results
    compare_modules(module_results)
    
    # Show recommended structure
    print_recommended_structure()
    
    print("\n" + "=" * 80)
    print("\nAnalysis complete!")
    print("\nTo fix Module 1 navigation, run: python fix_01module_navigation.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
