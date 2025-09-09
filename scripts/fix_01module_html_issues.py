#!/usr/bin/env python3
"""
Fix common HTML issues in 01module files:
1. Add missing securityLevel: 'loose' to mermaid initialization
2. Fix incorrect mermaid closing tags (</div> to </pre>)
3. Standardize CSS class names
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create a backup of the file before modifying"""
    backup_dir = Path(filepath).parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{Path(filepath).stem}_{timestamp}{Path(filepath).suffix}"
    backup_path = backup_dir / backup_name
    
    shutil.copy2(filepath, backup_path)
    print(f"  Backup created: {backup_path}")
    return backup_path

def fix_mermaid_initialization(content):
    """Add missing securityLevel: 'loose' to mermaid initialization"""
    
    # Pattern to find mermaid initialization without securityLevel
    pattern = r'(mermaid\.initialize\(\s*\{[^}]*?)(flowchart:\s*\{[^}]*?\})\s*(\})'
    
    def replacement(match):
        init_part = match.group(1)
        flowchart_part = match.group(2)
        closing = match.group(3)
        
        # Check if securityLevel already exists
        if 'securityLevel' not in init_part:
            # Add securityLevel after flowchart
            return f'{init_part}{flowchart_part},\n            securityLevel: \'loose\'\n        {closing}'
        else:
            return match.group(0)
    
    # Apply the fix
    fixed_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Count fixes
    fixes_made = 1 if fixed_content != content else 0
    
    return fixed_content, fixes_made

def fix_mermaid_closing_tags(content):
    """Fix incorrect mermaid diagram closing tags (</div> should be </pre>)"""
    
    # Pattern to find mermaid blocks with incorrect closing
    # Looking for <pre class="mermaid"> ... </div>
    pattern = r'(<pre\s+class="mermaid">[\s\S]*?)</div>'
    
    fixes_made = 0
    
    def replacement(match):
        nonlocal fixes_made
        fixes_made += 1
        return match.group(1) + '</pre>'
    
    # Apply the fix
    fixed_content = re.sub(pattern, replacement, content)
    
    return fixed_content, fixes_made

def standardize_css_classes(content):
    """Standardize CSS class names from underscore to kebab-case"""
    
    # Map of underscore classes to kebab-case equivalents
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
        'takeaways_list': 'takeaways-list',
        'practice_list': 'practice-list',
        'real_world_analogy': 'real-world-analogy',
        'concept_visualization': 'concept-visualization',
        'data_type_table': 'data-type-table',
        'data_type_quirks': 'data-type-quirks',
        'control_statements': 'control-statements',
        'common_patterns': 'common-patterns',
        'advanced_topics': 'advanced-topics',
        'key_takeaways': 'key-takeaways',
        'module_intro': 'module-intro',
        'module_details': 'module-details'
    }
    
    fixes_made = 0
    fixed_content = content
    
    for old_class, new_class in class_mappings.items():
        # Pattern to match class attribute with the old class name
        pattern = rf'class="([^"]*\b){old_class}(\b[^"]*)"'
        
        def replacement(match):
            nonlocal fixes_made
            fixes_made += 1
            return f'class="{match.group(1)}{new_class}{match.group(2)}"'
        
        fixed_content = re.sub(pattern, replacement, fixed_content)
    
    return fixed_content, fixes_made

def validate_html_structure(content, filename):
    """Check for common HTML structure issues"""
    issues = []
    
    # Check for unclosed tags
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    if open_divs != close_divs:
        issues.append(f"  ⚠️  Mismatched div tags: {open_divs} opening, {close_divs} closing")
    
    # Check for mermaid blocks
    mermaid_blocks = re.findall(r'<pre\s+class="mermaid">', content)
    mermaid_closes_pre = content.count('</pre>')
    
    # Check if there are still </div> after mermaid blocks
    remaining_bad_closes = len(re.findall(r'<pre\s+class="mermaid">[\s\S]*?</div>', content))
    if remaining_bad_closes > 0:
        issues.append(f"  ⚠️  Still {remaining_bad_closes} mermaid blocks with incorrect closing tags")
    
    return issues

def process_file(filepath):
    """Process a single HTML file"""
    print(f"\nProcessing: {filepath}")
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_fixes = 0
        
        # Apply fixes
        print("  Applying fixes...")
        
        # Fix 1: Mermaid initialization
        content, fixes = fix_mermaid_initialization(content)
        if fixes > 0:
            print(f"    ✓ Fixed mermaid initialization")
        total_fixes += fixes
        
        # Fix 2: Mermaid closing tags
        content, fixes = fix_mermaid_closing_tags(content)
        if fixes > 0:
            print(f"    ✓ Fixed {fixes} mermaid closing tags")
        total_fixes += fixes
        
        # Fix 3: CSS class names
        content, fixes = standardize_css_classes(content)
        if fixes > 0:
            print(f"    ✓ Standardized {fixes} CSS class names")
        total_fixes += fixes
        
        # Validate structure
        issues = validate_html_structure(content, filepath)
        if issues:
            print("  Validation issues found:")
            for issue in issues:
                print(issue)
        
        # Save if changes were made
        if content != original_content:
            # Create backup
            backup_file(filepath)
            
            # Save fixed content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ File updated with {total_fixes} fixes")
            return True
        else:
            print("  ℹ️  No changes needed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """Main function to process all HTML files in 01module directory"""
    
    # Define the directory
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")
    
    if not module_dir.exists():
        print(f"Error: Directory {module_dir} does not exist!")
        return
    
    # Get all HTML files
    html_files = list(module_dir.glob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in {module_dir}")
        return
    
    print(f"Found {len(html_files)} HTML files in {module_dir}")
    print("=" * 60)
    
    # Process each file
    files_modified = 0
    files_processed = 0
    
    for filepath in html_files:
        if process_file(filepath):
            files_modified += 1
        files_processed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Files unchanged: {files_processed - files_modified}")
    
    if files_modified > 0:
        print(f"\n✅ Successfully fixed {files_modified} files!")
        print("Backups have been created in the 'backups' subdirectory")
    else:
        print("\n✅ All files are already correct!")

if __name__ == "__main__":
    main()
