import os
from fix_01module_navigation import get_session_navigation_info

# Test different files
test_files = [
    'course_introduction.html',  # Session 1
    'css_syntax_and_selectors.html',  # Session 3
    'js_intro.html',  # Session 6
    'php_header_footer.html',  # Session 10
    'project_static_site.html',  # Session 10
]

print("NAVIGATION TEST RESULTS")
print("=" * 60)

for filename in test_files:
    file_path = f'/01module/{filename}'
    nav_info = get_session_navigation_info(file_path)
    
    print(f"\nFile: {filename}")
    if nav_info:
        print(f"  Session: {nav_info['current_session']}")
        if 'prev' in nav_info:
            print(f"  Prev: {nav_info['prev_title']} -> {nav_info['prev']}")
        if 'next' in nav_info:
            print(f"  Next: {nav_info['next_title']} -> {nav_info['next']}")
    else:
        print("  No navigation info")
    print("-" * 40)
