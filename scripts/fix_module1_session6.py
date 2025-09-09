#!/usr/bin/env python3
"""
Module 1: Session 6 Corrections Script
This script fixes issues in the JavaScript Fundamentals session files.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
MODULE_DIR = os.path.join(PROJECT_ROOT, "01module")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "01module_backups", f"session6_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

# Session 6 files to process
SESSION_6_FILES = [
    "js_intro.html",
    "js_syntax_fundamentals.html",
    "js_syntaxx1.html",  # File with typo to rename
    "js_operators_and_expressions.html",
    "js_control_flow.html",
    "js_functions_and_scope.html",
    "homework_simple_js_programs.html"
]

# Correct navigation order for Session 6
NAVIGATION_ORDER = [
    ("js_intro.html", "Introduction to JavaScript"),
    ("js_syntax_fundamentals.html", "JavaScript Syntax, Variables, and Data Types"),
    ("js_operators_and_expressions.html", "Operators and Expressions"),
    ("js_control_flow.html", "Control Flow (Conditionals, Loops)"),
    ("js_functions_and_scope.html", "Functions and Scope"),
    ("homework_simple_js_programs.html", "Homework: Simple JavaScript Programs")
]

def create_backup():
    """Create backup of current session 6 files."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    for filename in SESSION_6_FILES:
        src = os.path.join(MODULE_DIR, filename)
        if os.path.exists(src):
            dst = os.path.join(BACKUP_DIR, filename)
            shutil.copy2(src, dst)
            print(f"Backed up: {filename}")
    
    print(f"\nBackup created at: {BACKUP_DIR}")

def rename_typo_file():
    """Rename js_syntaxx1.html if it exists."""
    old_file = os.path.join(MODULE_DIR, "js_syntaxx1.html")
    
    if os.path.exists(old_file):
        # Check if js_syntax_fundamentals.html already exists
        correct_file = os.path.join(MODULE_DIR, "js_syntax_fundamentals.html")
        if os.path.exists(correct_file):
            # Create a backup with different name to avoid conflict
            backup_file = os.path.join(MODULE_DIR, "js_syntax_fundamentals_backup.html")
            shutil.move(old_file, backup_file)
            print(f"Renamed js_syntaxx1.html to js_syntax_fundamentals_backup.html (file already exists)")
        else:
            shutil.move(old_file, correct_file)
            print(f"Renamed js_syntaxx1.html to js_syntax_fundamentals.html")
        return True
    return False

def fix_navigation(filepath, current_index):
    """Fix the navigation links in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine previous and next lessons
    if current_index > 0:
        prev_file, prev_title = NAVIGATION_ORDER[current_index - 1]
    else:
        # First lesson of session 6, link back to Session 5 or module overview
        prev_file = "/01module/homework_bootstrap_profile.html"
        prev_title = "Homework: Bootstrap Profile"
    
    if current_index < len(NAVIGATION_ORDER) - 1:
        next_file, next_title = NAVIGATION_ORDER[current_index + 1]
    else:
        # Last lesson of session 6, link to Session 7
        next_file = "/01module/understanding_dom.html"
        next_title = "Understanding the DOM"
    
    # Update navigation section
    nav_pattern = r'<div class="lesson-navigation">.*?</div>\s*(?=</article>|$)'
    
    new_nav = f'''<div class="lesson-navigation">
                            <a href="/01module/{prev_file}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    {prev_title}
                                </span>
                            </a>
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>
                            
                            <a href="/01module/{next_file}" class="lesson-nav-button next">
                                <span>
                                    <small>Next</small><br>
                                    {next_title}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>
                        </div>'''
    
    content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
    
    return content

def fix_metadata(content, filename, title):
    """Fix metadata in the HTML head section."""
    # Update title tag
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{title} - Module 1: JavaScript Fundamentals</title>',
        content
    )
    
    # Update meta description
    content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="Module 1, Session 6: {title}. Learn JavaScript fundamentals for web development.">',
        content
    )
    
    # Update keywords
    keywords = title.lower().replace(" ", ", ").replace(":", "").replace("(", "").replace(")", "")
    content = re.sub(
        r'<meta name="keywords" content=".*?">',
        f'<meta name="keywords" content="PHP, WordPress, web development, JavaScript, {keywords}">',
        content
    )
    
    return content

def fix_breadcrumbs(content, title):
    """Fix breadcrumb navigation."""
    breadcrumb_pattern = r'<nav class="breadcrumb.*?</nav>'
    
    new_breadcrumb = f'''<nav class="breadcrumb container" aria-label="Breadcrumb">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <a href="/module1.html">Module 1</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <span aria-current="page">{title}</span>
                </li>
            </ol>
        </nav>'''
    
    content = re.sub(breadcrumb_pattern, new_breadcrumb, content, flags=re.DOTALL)
    
    return content

def fix_sidebar_links(content):
    """Update sidebar navigation links for Session 6."""
    sidebar_pattern = r'<div class="sidebar-section">.*?</div>\s*(?=</div>\s*</aside>)'
    
    new_sidebar = '''<div class="sidebar-section">
                                <h4 class="sidebar-section-title">Session 6: JavaScript Fundamentals</h4>
                                <a href="/01module/js_intro.html" class="sidebar-link">Introduction to JavaScript</a>
                                <a href="/01module/js_syntax_fundamentals.html" class="sidebar-link">Syntax & Variables</a>
                                <a href="/01module/js_operators_and_expressions.html" class="sidebar-link">Operators & Expressions</a>
                                <a href="/01module/js_control_flow.html" class="sidebar-link">Control Flow</a>
                                <a href="/01module/js_functions_and_scope.html" class="sidebar-link">Functions & Scope</a>
                                <a href="/01module/homework_simple_js_programs.html" class="sidebar-link">Homework</a>
                            </div>'''
    
    content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)
    
    return content

def fix_lesson_meta(content):
    """Update lesson metadata section."""
    meta_pattern = r'<div class="lesson-meta">.*?</div>\s*(?=</header>)'
    
    new_meta = '''<div class="lesson-meta">
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <span>Duration: 30 minutes</span>
                                </div>
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 14l9-5-9-5-9 5 9 5z"/>
                                    </svg>
                                    <span>Module 1: Session 6</span>
                                </div>
                            </div>'''
    
    content = re.sub(meta_pattern, new_meta, content, flags=re.DOTALL)
    
    return content

def process_file(filename, index):
    """Process a single file with all corrections."""
    filepath = os.path.join(MODULE_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found")
        return False
    
    # Get the correct title for this file
    _, title = NAVIGATION_ORDER[index]
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all fixes
    content = fix_navigation(filepath, index)
    content = fix_metadata(content, filename, title)
    content = fix_breadcrumbs(content, title)
    content = fix_sidebar_links(content)
    content = fix_lesson_meta(content)
    
    # Update the main heading
    content = re.sub(
        r'<h1>.*?</h1>',
        f'<h1>{title}</h1>',
        content,
        count=1
    )
    
    # Write the updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {filename}")
    return True

def main():
    """Main execution function."""
    print("=" * 60)
    print("Module 1: Session 6 Corrections Script")
    print("=" * 60)
    
    # Create backup
    print("\n1. Creating backup...")
    create_backup()
    
    # Rename typo file
    print("\n2. Fixing filename typo...")
    if rename_typo_file():
        # Update the list to use correct filename
        SESSION_6_FILES[2] = "js_syntax_fundamentals.html"
    
    # Process each file
    print("\n3. Processing Session 6 files...")
    success_count = 0
    
    for i, (filename, _) in enumerate(NAVIGATION_ORDER):
        if process_file(filename, i):
            success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed: {success_count}/{len(NAVIGATION_ORDER)}")
    print(f"Backup location: {BACKUP_DIR}")
    
    # Additional checks
    print("\n4. Verifying corrections...")
    
    # Check that all files exist with correct names
    all_exist = True
    for filename, _ in NAVIGATION_ORDER:
        filepath = os.path.join(MODULE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"ERROR: {filename} not found after corrections")
            all_exist = False
    
    if all_exist:
        print("✓ All files exist with correct names")
    
    # Check that typo file no longer exists
    typo_file = os.path.join(MODULE_DIR, "js_syntaxx1.html")
    if not os.path.exists(typo_file):
        print("✓ Typo file (js_syntaxx1.html) has been renamed")
    else:
        print("WARNING: js_syntaxx1.html still exists")
    
    print("\n✨ Session 6 corrections completed!")
    print("\nNext steps:")
    print("1. Review the corrected files in your browser")
    print("2. Test navigation between lessons")
    print("3. Verify all links work correctly")
    print("4. Check that the sidebar navigation is consistent")

if __name__ == "__main__":
    main()
