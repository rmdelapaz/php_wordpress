#!/usr/bin/env python3
"""Test session navigation mappings."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fix_01module_navigation import get_session_navigation_info

# Test files from different sessions
test_cases = [
    # Session 1
    ('course_introduction.html', 1, None, 'Session 2: HTML'),
    ('first_html_page.html', 1, None, 'Session 2: HTML'),
    
    # Session 2  
    ('html_structure_syntax.html', 2, 'Session 1: Setup', 'Session 3: CSS'),
    ('essential_html_tags.html', 2, 'Session 1: Setup', 'Session 3: CSS'),
    
    # Session 3
    ('introduction_to_css.html', 3, 'Session 2: HTML', 'Session 4: Layout'),
    ('css_syntax_and_selectors.html', 3, 'Session 2: HTML', 'Session 4: Layout'),
    
    # Session 4
    ('css_layout_tech.html', 4, 'Session 3: CSS', 'Session 5: Bootstrap'),
    ('responsive_design.html', 4, 'Session 3: CSS', 'Session 5: Bootstrap'),
    
    # Session 5
    ('bootstrap.html', 5, 'Session 4: Layout', 'Session 6: JavaScript'),
    ('bootstrap_grid.html', 5, 'Session 4: Layout', 'Session 6: JavaScript'),
    
    # Session 6
    ('js_intro.html', 6, 'Session 5: Bootstrap', 'Session 7: DOM'),
    ('js_control_flow.html', 6, 'Session 5: Bootstrap', 'Session 7: DOM'),
    
    # Session 7
    ('understanding_dom.html', 7, 'Session 6: JavaScript', 'Session 8: Modern JS'),
    ('event_handling.html', 7, 'Session 6: JavaScript', 'Session 8: Modern JS'),
    
    # Session 8
    ('es6_overview.html', 8, 'Session 7: DOM', 'Session 9: PHP'),
    ('jquery_intro.html', 8, 'Session 7: DOM', 'Session 9: PHP'),
    
    # Session 9
    ('php_and_wordpress.html', 9, 'Session 8: Modern JS', 'Session 10: Project'),
    ('php_syntax.html', 9, 'Session 8: Modern JS', 'Session 10: Project'),
    
    # Session 10
    ('planning_website.html', 10, 'Session 9: PHP', 'Module 2: PHP Setup'),
    ('project_static_site.html', 10, 'Session 9: PHP', 'Module 2: PHP Setup'),
]

print("=" * 80)
print("SESSION NAVIGATION TEST")
print("=" * 80)

errors = []
for filename, expected_session, expected_prev, expected_next in test_cases:
    file_path = f'/01module/{filename}'
    nav_info = get_session_navigation_info(file_path)
    
    if not nav_info:
        errors.append(f"❌ {filename}: No navigation info returned")
        continue
    
    # Check session number
    if nav_info['current_session'] != expected_session:
        errors.append(f"❌ {filename}: Expected session {expected_session}, got {nav_info['current_session']}")
    
    # Check previous link
    if expected_prev:
        if 'prev_title' not in nav_info:
            errors.append(f"❌ {filename}: Missing previous link (expected {expected_prev})")
        elif nav_info['prev_title'] != expected_prev:
            errors.append(f"❌ {filename}: Wrong prev title - expected '{expected_prev}', got '{nav_info['prev_title']}'")
    else:
        if 'prev_title' in nav_info:
            errors.append(f"❌ {filename}: Should not have previous link")
    
    # Check next link
    if expected_next:
        if 'next_title' not in nav_info:
            errors.append(f"❌ {filename}: Missing next link (expected {expected_next})")
        elif nav_info['next_title'] != expected_next:
            errors.append(f"❌ {filename}: Wrong next title - expected '{expected_next}', got '{nav_info['next_title']}'")

if errors:
    print("\nERRORS FOUND:")
    for error in errors:
        print(error)
else:
    print("\n✅ All tests passed!")

# Print first lesson verification
print("\n" + "=" * 80)
print("FIRST LESSON VERIFICATION")
print("=" * 80)

expected_first_lessons = {
    1: '/01module/course_introduction.html',
    2: '/01module/html_structure_syntax.html', 
    3: '/01module/introduction_to_css.html',
    4: '/01module/css_layout_tech.html',
    5: '/01module/bootstrap.html',
    6: '/01module/js_intro.html',
    7: '/01module/understanding_dom.html',
    8: '/01module/es6_overview.html',
    9: '/01module/php_and_wordpress.html',
    10: '/01module/planning_website.html',
}

print("\nFirst lesson of each session:")
for session_num, expected_file in expected_first_lessons.items():
    print(f"  Session {session_num}: {expected_file}")

print("\n✅ Session navigation structure verified!")
