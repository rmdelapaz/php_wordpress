#!/usr/bin/env python3
"""
Fix js_control_flow.html issues
"""

import os
import re
import shutil
from datetime import datetime

# Configuration
PROJECT_ROOT = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
MODULE_DIR = os.path.join(PROJECT_ROOT, "01module")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "01module_backups", f"control_flow_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

def create_backup():
    """Create backup of js_control_flow.html."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    src = os.path.join(MODULE_DIR, "js_control_flow.html")
    if os.path.exists(src):
        dst = os.path.join(BACKUP_DIR, "js_control_flow.html")
        shutil.copy2(src, dst)
        print(f"Backed up to: {dst}")

def fix_js_control_flow():
    """Fix all issues in js_control_flow.html."""
    filepath = os.path.join(MODULE_DIR, "js_control_flow.html")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix title and meta tags
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Control Flow (Conditionals, Loops) - Module 1: JavaScript Fundamentals</title>',
        content
    )
    
    content = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="Module 1, Session 6: Control Flow (Conditionals, Loops). Learn JavaScript conditionals and loops for web development.">',
        content
    )
    
    content = re.sub(
        r'<meta name="keywords" content=".*?">',
        '<meta name="keywords" content="PHP, WordPress, web development, JavaScript, control flow, conditionals, loops, if else, for, while, switch">',
        content
    )
    
    # 2. Fix main heading
    content = re.sub(
        r'<h1>.*?</h1>',
        '<h1>Control Flow (Conditionals, Loops)</h1>',
        content,
        count=1
    )
    
    # 3. Fix breadcrumb
    breadcrumb_pattern = r'(<span aria-current="page">).*?(</span>)'
    content = re.sub(
        breadcrumb_pattern,
        r'\1Control Flow (Conditionals, Loops)\2',
        content
    )
    
    # 4. Fix sidebar navigation
    sidebar_pattern = r'(<div class="sidebar-section">)(.*?)(</div>\s*</div>\s*</aside>)'
    new_sidebar = r'''\1
                                <h4 class="sidebar-section-title">Session 6: JavaScript Fundamentals</h4>
                                <a href="/01module/js_intro.html" class="sidebar-link">Introduction to JavaScript</a>
                                <a href="/01module/js_syntax_fundamentals.html" class="sidebar-link">Syntax & Variables</a>
                                <a href="/01module/js_operators_and_expressions.html" class="sidebar-link">Operators & Expressions</a>
                                <a href="/01module/js_control_flow.html" class="sidebar-link active">Control Flow</a>
                                <a href="/01module/js_functions_and_scope.html" class="sidebar-link">Functions & Scope</a>
                                <a href="/01module/homework_simple_js_programs.html" class="sidebar-link">Homework</a>
                            </div>\3'''
    content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)
    
    # 5. Fix lesson meta
    meta_pattern = r'(<span>Module 1:).*?(</span>)'
    content = re.sub(
        meta_pattern,
        r'\1 Session 6\2',
        content
    )
    
    # 6. Fix navigation
    nav_pattern = r'<div class="lesson-navigation">.*?</div>\s*(?=</article>)'
    new_nav = '''<div class="lesson-navigation">
                            <a href="/01module/js_operators_and_expressions.html" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    Operators and Expressions
                                </span>
                            </a>
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>
                            
                            <a href="/01module/js_functions_and_scope.html" class="lesson-nav-button next">
                                <span>
                                    <small>Next</small><br>
                                    Functions and Scope
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>
                        </div>'''
    content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
    
    # 7. Fix learning objectives
    objectives_pattern = r'(<div class="lesson-objectives">.*?<ul>)(.*?)(</ul>)'
    new_objectives = """
                                <li>Understand how conditional statements control program flow</li>
                                <li>Master different types of loops in JavaScript</li>
                                <li>Learn to use break and continue statements effectively</li>
                                <li>Apply control flow patterns to solve real-world problems</li>"""
    content = re.sub(
        objectives_pattern,
        r'\1' + new_objectives + r'\n            \3',
        content,
        flags=re.DOTALL
    )
    
    # 8. Fix Mermaid diagram closing tags
    # Find all mermaid blocks that incorrectly end with </div> instead of </pre>
    content = re.sub(
        r'(<pre class="mermaid">.*?)</div>',
        r'\1</pre>',
        content,
        flags=re.DOTALL
    )
    
    # Write the fixed content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: js_control_flow.html")
    return True

def main():
    print("=" * 60)
    print("Fixing js_control_flow.html")
    print("=" * 60)
    
    # Create backup
    print("\n1. Creating backup...")
    create_backup()
    
    # Fix the file
    print("\n2. Fixing issues...")
    if fix_js_control_flow():
        print("\n✅ Successfully fixed js_control_flow.html")
        print("\nFixed issues:")
        print("- Title and metadata")
        print("- Main heading")
        print("- Breadcrumb navigation")
        print("- Sidebar navigation links")
        print("- Lesson meta information")
        print("- Previous/Next navigation")
        print("- Learning objectives")
        print("- Mermaid diagram closing tags")
    else:
        print("\n❌ Failed to fix js_control_flow.html")

if __name__ == "__main__":
    main()
