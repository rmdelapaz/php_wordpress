#!/usr/bin/env python3
"""
Fix ALL HTML issues in 01module files
This script will process every HTML file and fix common issues.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def fix_all_issues_in_file(filepath):
    """Fix all known issues in a single HTML file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = []
        
        # Fix 1: Add missing securityLevel to mermaid initialization
        if 'mermaid.initialize' in content:
            # Check if securityLevel is missing
            init_match = re.search(r'mermaid\.initialize\(\s*\{([^}]*)\}', content, re.DOTALL)
            if init_match and 'securityLevel' not in init_match.group(1):
                # Add securityLevel after flowchart section
                pattern = r'(mermaid\.initialize\(\s*\{[^}]*?flowchart:\s*\{[^}]*?\})'
                replacement = r'\1,\n            securityLevel: \'loose\''
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                if new_content != content:
                    content = new_content
                    fixes_made.append("Added securityLevel to mermaid init")
        
        # Fix 2: Fix ALL mermaid closing tags (</div> should be </pre>)
        # Find all mermaid blocks with incorrect closing
        mermaid_pattern = r'(<pre\s+class="mermaid">(?:(?!</pre>).)*?)</div>'
        matches = list(re.finditer(mermaid_pattern, content, re.DOTALL))
        
        if matches:
            # Replace from end to beginning to maintain positions
            for match in reversed(matches):
                start, end = match.span()
                fixed_block = match.group(1) + '</pre>'
                content = content[:start] + fixed_block + content[end:]
            fixes_made.append(f"Fixed {len(matches)} mermaid closing tags")
        
        # Fix 3: Fix CSS class names (underscore to kebab-case)
        class_mappings = {
            'real_world_example': 'real-world-example',
            'best_practice': 'best-practice',
            'key_concepts': 'key-concepts',
            'code_example': 'code-example',
            'important_note': 'important-note',
            'comparison_table': 'comparison-table',
            'practical_tip': 'practical-tip',
            'debugging_tips': 'debugging-tips',
            'exercise_list': 'exercise-list',
            'solution_example': 'solution-example',
            'common_issues': 'common-issues',
            'debugging_techniques': 'debugging-techniques',
            'common_fixes': 'common-fixes',
            'best_practices': 'best-practices',
            'svg_container': 'svg-container',
            'svg_diagram': 'svg-diagram',
            'resource_list': 'resource-list',
            'practice_list': 'practice-list',
            'real_world_analogy': 'real-world-analogy',
            'concept_visualization': 'concept-visualization'
        }
        
        css_fixes = 0
        for old_class, new_class in class_mappings.items():
            pattern = rf'class="([^"]*\b){old_class}(\b[^"]*)"'
            def replacement(match):
                nonlocal css_fixes
                css_fixes += 1
                return f'class="{match.group(1)}{new_class}{match.group(2)}"'
            content = re.sub(pattern, replacement, content)
        
        if css_fixes > 0:
            fixes_made.append(f"Fixed {css_fixes} CSS class names")
        
        # Save if changes were made
        if content != original_content:
            # Create backup directory if it doesn't exist
            backup_dir = Path(filepath).parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            # Create backup with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{Path(filepath).stem}_{timestamp}{Path(filepath).suffix}"
            backup_path = backup_dir / backup_name
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Save fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, fixes_made
        
        return False, []
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, []

# Main execution
module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")

print("=" * 60)
print("Fixing ALL HTML issues in 01module directory")
print("=" * 60)

# Get all HTML files
html_files = list(module_dir.glob("*.html"))
print(f"Found {len(html_files)} HTML files")
print()

files_modified = 0
total_fixes = 0

for filepath in sorted(html_files):
    print(f"Processing: {filepath.name}")
    modified, fixes = fix_all_issues_in_file(filepath)
    
    if modified:
        files_modified += 1
        total_fixes += len(fixes)
        for fix in fixes:
            print(f"  ✅ {fix}")
    else:
        print(f"  ℹ️ No changes needed")

print("\n" + "=" * 60)
print("SUMMARY")
print(f"Files processed: {len(html_files)}")
print(f"Files modified: {files_modified}")
print(f"Total fixes applied: {total_fixes}")

if files_modified > 0:
    print(f"\n✅ Successfully fixed {files_modified} files!")
    print("Backups have been created in the 'backups' subdirectory")
else:
    print("\n✅ All files are already correct!")
