#!/usr/bin/env python3
"""
Fix and standardize Quick Links section in sidebar for all module HTML files.
Ensures consistent navigation links across all modules.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Base path for WSL
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"

def extract_quick_links_section(content: str) -> Tuple[str, int, int]:
    """
    Extract the Quick Links section from the HTML content.
    Returns the quick links HTML, start position, and end position.
    """
    # Pattern to find the Quick Links section
    pattern = r'(<h4 class="sidebar-section-title">Quick Links</h4>.*?</ul>\s*</div>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return match.group(1), match.start(1), match.end(1)
    return None, -1, -1

def get_module_navigation_info(module: str, file_name: str) -> Dict[str, str]:
    """
    Get navigation information for a file based on its module and name.
    """
    module_num = int(module.replace("module", ""))
    prev_module = f"module{module_num - 1}" if module_num > 1 else None
    next_module = f"module{module_num + 1}" if module_num < 9 else None
    
    return {
        "module_num": module_num,
        "prev_module": prev_module,
        "next_module": next_module,
        "module_overview": f"/module{module_num}.html"
    }

def generate_quick_links(nav_info: Dict[str, str], file_name: str) -> str:
    """
    Generate the Quick Links section HTML based on navigation info.
    """
    module_num = nav_info["module_num"]
    
    # Build the quick links HTML
    quick_links = f'''<h4 class="sidebar-section-title">Quick Links</h4>
<ul class="sidebar-menu">
    <li><a class="sidebar-link" href="/module{module_num}.html">Module Overview</a></li>'''
    
    # Add previous lesson link if not the first file
    # This is a simplified version - you might want to enhance this with actual file ordering
    quick_links += f'''
    <li><a class="sidebar-link" href="/">← Course Home</a></li>'''
    
    # Add next module link if not the last module
    if nav_info["next_module"]:
        next_module_num = int(nav_info["next_module"].replace("module", ""))
        quick_links += f'''
    <li><a class="sidebar-link" href="/module{next_module_num}.html">Next Module →</a></li>'''
    
    quick_links += '''
    <li><a class="sidebar-link" href="/resources.html">Resources</a></li>
</ul>'''
    
    return quick_links

def fix_quick_links(file_path: str, module: str) -> bool:
    """
    Fix the Quick Links section in a single HTML file.
    Returns True if file was modified, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract current quick links section
        current_links, start_pos, end_pos = extract_quick_links_section(content)
        
        if current_links and start_pos != -1:
            # Get navigation info
            file_name = os.path.basename(file_path)
            nav_info = get_module_navigation_info(module, file_name)
            
            # Generate new quick links
            new_quick_links = generate_quick_links(nav_info, file_name)
            
            # Check if update is needed (simple comparison)
            if current_links.strip() != new_quick_links.strip():
                # Replace in content
                new_content = content[:start_pos] + new_quick_links + content[end_pos:]
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Fixed: {os.path.basename(file_path)} - Updated Quick Links")
                return True
            else:
                print(f"⏭️  Skipped: {os.path.basename(file_path)} - Quick Links already correct")
                return False
        else:
            print(f"⚠️  Warning: {os.path.basename(file_path)} - No Quick Links section found")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def process_module(module: str) -> Dict[str, int]:
    """
    Process all HTML files in a module directory.
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
        
        if fix_quick_links(file_path, module):
            stats["modified"] += 1
        else:
            stats["skipped"] += 1
    
    return stats

def main():
    """
    Main function to process all modules.
    """
    print("🔧 Quick Links Standardizer Script")
    print("=" * 50)
    print(f"Base path: {BASE_PATH}")
    print("=" * 50)
    
    total_stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
    
    # Process modules 1-6 (the ones with content)
    modules = [f"{i:02d}module" for i in range(1, 7)]
    
    for module in modules:
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
    print("✅ Quick Links standardization complete!")

if __name__ == "__main__":
    main()
