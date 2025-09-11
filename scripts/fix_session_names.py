#!/usr/bin/env python3
"""
Fix session names in sidebar titles for all module HTML files.
This script adds descriptive session names to the sidebar section titles.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Base path for WSL
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"

# Session names mapping for each module
SESSION_NAMES = {
    "01module": {
        "Session 1": "Session 1: Introduction",
        "Session 2": "Session 2: HTML Fundamentals", 
        "Session 3": "Session 3: CSS Basics",
        "Session 4": "Session 4: CSS Layout",
        "Session 5": "Session 5: CSS Frameworks",
        "Session 6": "Session 6: JavaScript Basics",
        "Session 7": "Session 7: DOM Manipulation",
        "Session 8": "Session 8: jQuery",
        "Session 9": "Session 9: PHP Introduction",
        "Session 10": "Session 10: Final Project"
    },
    "02module": {
        "Session 1": "Session 1: PHP Basics",
        "Session 2": "Session 2: Variables and Data Types",
        "Session 3": "Session 3: Control Structures",
        "Session 4": "Session 4: Functions",
        "Session 5": "Session 5: Arrays",
        "Session 6": "Session 6: Forms and User Input",
        "Session 7": "Session 7: Working with Files",
        "Session 8": "Session 8: Object-Oriented PHP",
        "Session 9": "Session 9: Error Handling",
        "Session 10": "Session 10: PHP Project"
    },
    "03module": {
        "Session 1": "Session 1: Introduction to Databases",
        "Session 2": "Session 2: Database Design",
        "Session 3": "Session 3: SQL Basics",
        "Session 4": "Session 4: Advanced SQL",
        "Session 5": "Session 5: PHP and MySQL",
        "Session 6": "Session 6: Database Project"
    },
    "04module": {
        "Session 1": "Session 1: WordPress Introduction",
        "Session 2": "Session 2: Docker Setup",
        "Session 3": "Session 3: WordPress Installation",
        "Session 4": "Session 4: WordPress Basics",
        "Session 5": "Session 5: Content Management"
    },
    "05module": {
        "Session 1": "Session 1: Theme Structure",
        "Session 2": "Session 2: Template Hierarchy",
        "Session 3": "Session 3: The Loop",
        "Session 4": "Session 4: Custom Templates",
        "Session 5": "Session 5: Theme Functions",
        "Session 6": "Session 6: Customizer API",
        "Session 7": "Session 7: Theme Project"
    },
    "06module": {
        "Session 1": "Session 1: Plugin Basics",
        "Session 2": "Session 2: Hooks and Filters",
        "Session 3": "Session 3: Admin Pages and Settings",
        "Session 4": "Session 4: Custom Post Types",
        "Session 5": "Session 5: Shortcodes and Widgets",
        "Session 6": "Session 6: Plugin Security",
        "Session 7": "Session 7: Plugin Project"
    }
}

def find_session_title(content: str) -> Tuple[str, int, int]:
    """
    Find the current session title in the sidebar.
    Returns the title text and its position in the file.
    """
    # Pattern to match session title in sidebar
    pattern = r'<h4 class="sidebar-section-title">(Session \d+)[^<]*</h4>'
    match = re.search(pattern, content)
    
    if match:
        return match.group(1), match.start(), match.end()
    return None, -1, -1

def get_session_name(module: str, session_text: str) -> str:
    """
    Get the full session name with description for a given module and session.
    """
    if module in SESSION_NAMES:
        return SESSION_NAMES[module].get(session_text, session_text)
    return session_text

def fix_session_names(file_path: str, module: str) -> bool:
    """
    Fix session names in a single HTML file.
    Returns True if file was modified, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the session title
        session_text, start_pos, end_pos = find_session_title(content)
        
        if session_text and start_pos != -1:
            # Get the full session name
            full_session_name = get_session_name(module, session_text)
            
            # Check if it needs updating
            current_full_text = content[start_pos:end_pos]
            if full_session_name not in current_full_text:
                # Build the new h4 tag
                new_h4 = f'<h4 class="sidebar-section-title">{full_session_name}</h4>'
                
                # Replace in content
                new_content = content[:start_pos] + new_h4 + content[end_pos:]
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Fixed: {os.path.basename(file_path)} - Added '{full_session_name}'")
                return True
            else:
                print(f"⏭️  Skipped: {os.path.basename(file_path)} - Already has full session name")
                return False
        else:
            print(f"❌ No session title found in: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def process_module(module: str) -> Dict[str, int]:
    """
    Process all HTML files in a module directory.
    Returns statistics about the processing.
    """
    module_path = os.path.join(BASE_PATH, module)
    stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
    
    if not os.path.exists(module_path):
        print(f"❌ Module directory not found: {module_path}")
        stats["errors"] = 1
        return stats
    
    print(f"\n📁 Processing module: {module}")
    print("=" * 50)
    
    # Get all HTML files in the module directory
    html_files = [f for f in os.listdir(module_path) if f.endswith('.html')]
    
    for html_file in sorted(html_files):
        file_path = os.path.join(module_path, html_file)
        stats["processed"] += 1
        
        if fix_session_names(file_path, module):
            stats["modified"] += 1
        else:
            stats["skipped"] += 1
    
    return stats

def main():
    """
    Main function to process all modules.
    """
    print("🔧 Session Name Fixer Script")
    print("=" * 50)
    print(f"Base path: {BASE_PATH}")
    print("=" * 50)
    
    total_stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
    
    # Process each module
    for module in SESSION_NAMES.keys():
        stats = process_module(module)
        
        # Update total stats
        for key in total_stats:
            total_stats[key] += stats[key]
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  Total files processed: {total_stats['processed']}")
    print(f"  Files modified: {total_stats['modified']}")
    print(f"  Files skipped: {total_stats['skipped']}")
    print(f"  Errors: {total_stats['errors']}")
    print("=" * 50)
    print("✅ Session name fixing complete!")

if __name__ == "__main__":
    main()
