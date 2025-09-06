#!/usr/bin/env python3
"""Test script to verify navigation generation for different pages."""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import our script
sys.path.insert(0, str(Path(__file__).parent))

from fix_01module_navigation import get_session_navigation_info, create_01module_navigation

def test_navigation():
    """Test navigation generation for various pages."""
    
    test_files = [
        '/01module/course_introduction.html',  # Session 1 - first file
        '/01module/css_syntax_and_selectors.html',  # Session 3 - middle file
        '/01module/js_intro.html',  # Session 6 - first file
        '/01module/php_header_footer.html',  # Session 10 - not first file
        '/01module/project_static_site.html',  # Session 10 - last file
    ]
    
    print("=" * 80)
    print("NAVIGATION STRUCTURE TEST")
    print("=" * 80)
    
    for file_path in test_files:
        filename = os.path.basename(file_path)
        nav_info = get_session_navigation_info(file_path)
        
        print(f"\n📄 File: {filename}")
        print("-" * 40)
        
        if nav_info:
            print(f"Current Session: {nav_info['current_session']}")
            
            if 'prev' in nav_info:
                print(f"Previous Session Link: {nav_info['prev_title']}")
                print(f"  → Links to: {nav_info['prev']}")
            else:
                print("Previous Session Link: None (first session)")
            
            if 'next' in nav_info:
                print(f"Next Session Link: {nav_info['next_title']}")
                print(f"  → Links to: {nav_info['next']}")
            else:
                print("Next Session Link: None (last session)")
        else:
            print("❌ No navigation info found for this file")
    
    # Test the full navigation HTML for one file
    print("\n" + "=" * 80)
    print("SAMPLE NAVIGATION HTML (for js_intro.html)")
    print("=" * 80)
    
    nav_html = create_01module_navigation('/01module/js_intro.html')
    
    # Extract just the Quick Links section for display
    import re
    quick_links_match = re.search(r'<h4[^>]*>Quick Links</h4>.*?</ul>', nav_html, re.DOTALL)
    if quick_links_match:
        print("\nQuick Links Section:")
        print(quick_links_match.group())

if __name__ == "__main__":
    test_navigation()
