#!/usr/bin/env python3
"""
Comprehensive fix for ALL HTML issues in 01module files
This version handles all variations of the mermaid issues more robustly.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def fix_html_file(filepath):
    """Fix all known issues in a single HTML file with detailed reporting"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = []
        
        # ======== FIX 1: Add missing securityLevel to mermaid initialization ========
        # Look for mermaid.initialize blocks without securityLevel
        mermaid_init_pattern = r'(mermaid\.initialize\(\s*\{[^}]*?)(flowchart:\s*\{[^}]*?\})\s*(\})'
        
        def check_and_fix_mermaid_init(match):
            full_match = match.group(0)
            if 'securityLevel' not in full_match:
                # Add securityLevel after flowchart
                return match.group(1) + match.group(2) + ',\n            securityLevel: \'loose\'\n        ' + match.group(3)
            return full_match
        
        new_content = re.sub(mermaid_init_pattern, check_and_fix_mermaid_init, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            fixes_made.append("Added securityLevel to mermaid initialization")
        
        # ======== FIX 2: Fix ALL incorrect mermaid closing tags ========
        # More comprehensive pattern to catch all variations
        # Look for any <pre class="mermaid"> block that ends with </div>
        
        # First approach: Find all mermaid blocks
        mermaid_blocks = []
        
        # Find all opening tags
        opening_pattern = r'<pre\s+class="mermaid">'
        for match in re.finditer(opening_pattern, content):
            start_pos = match.start()
            
            # Find the corresponding closing tag
            # Look for either </pre> or </div> after this position
            remaining_content = content[match.end():]
            
            # Find the next </pre> or </div>
            close_pre = remaining_content.find('</pre>')
            close_div = remaining_content.find('</div>')
            
            # If we find a </div> before a </pre> (or no </pre> at all), it's wrong
            if close_div != -1 and (close_pre == -1 or close_div < close_pre):
                # This mermaid block has incorrect closing
                mermaid_blocks.append({
                    'start': start_pos,
                    'end': match.end() + close_div + 6,  # 6 is length of </div>
                    'needs_fix': True
                })
        
        # Apply fixes from end to beginning to maintain positions
        if mermaid_blocks:
            for block in reversed(mermaid_blocks):
                if block['needs_fix']:
                    # Replace </div> with </pre> at the end of this block
                    block_content = content[block['start']:block['end']]
                    if block_content.endswith('</div>'):
                        fixed_block = block_content[:-6] + '</pre>'
                        content = content[:block['start']] + fixed_block + content[block['end']:]
            
            fixes_made.append(f"Fixed {len([b for b in mermaid_blocks if b.get('needs_fix')])} mermaid closing tags")
        
        # Alternative simpler approach if the above doesn't work
        # Just replace all instances where mermaid blocks end with </div>
        simple_pattern = r'(<pre\s+class="mermaid">[\s\S]*?)</div>'
        matches = list(re.finditer(simple_pattern, content))
        if matches:
            for match in reversed(matches):
                start, end = match.span()
                fixed = match.group(1) + '</pre>'
                content = content[:start] + fixed + content[end:]
            if not any('mermaid closing' in fix for fix in fixes_made):
                fixes_made.append(f"Fixed {len(matches)} mermaid closing tags (alternative method)")
        
        # ======== FIX 3: Fix CSS class names ========
        class_mappings = {
            'real_world_example': 'real-world-example',
            'real_world_analogy': 'real-world-analogy', 
            'best_practice': 'best-practice',
            'best_practices': 'best-practices',
            'key_concepts': 'key-concepts',
            'code_example': 'code-example',
            'important_note': 'important-note',
            'comparison_table': 'comparison-table',
            'practical_tip': 'practical-tip',
            'practical_application': 'practical-application',
            'debugging_tips': 'debugging-tips',
            'debugging_techniques': 'debugging-techniques',
            'exercise_list': 'exercise-list',
            'solution_example': 'solution-example',
            'common_issues': 'common-issues',
            'common_fixes': 'common-fixes',
            'svg_container': 'svg-container',
            'svg_diagram': 'svg-diagram',
            'resource_list': 'resource-list',
            'practice_list': 'practice-list',
            'takeaways_list': 'takeaways-list',
            'practices_list': 'practices-list',
            'concept_visualization': 'concept-visualization',
            'chaining_example': 'chaining-example',
            'side_effects': 'side-effects',
            'expressions_context': 'expressions-context',
            'special_comparisons': 'special-comparisons',
            'short_circuit': 'short-circuit',
            'bitwise_section': 'bitwise-section',
            'operator_precedence': 'operator-precedence',
            'string_operators': 'string-operators',
            'logical_operators': 'logical-operators',
            'comparison_operators': 'comparison-operators',
            'assignment_operators': 'assignment-operators',
            'arithmetic_operators': 'arithmetic-operators',
            'other_operators': 'other-operators',
            'data_types': 'data-types',
            'data_type_quirks': 'data-type-quirks',
            'practical_examples': 'practical-examples',
            'key_takeaways': 'key-takeaways'
        }
        
        css_fixes = 0
        for old_class, new_class in class_mappings.items():
            # Pattern to match class attribute with the old class name
            pattern = rf'class="([^"]*\b){old_class}(\b[^"]*)"'
            
            def replacement(match):
                nonlocal css_fixes
                css_fixes += 1
                return f'class="{match.group(1)}{new_class}{match.group(2)}"'
            
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
        
        if css_fixes > 0:
            fixes_made.append(f"Standardized {css_fixes} CSS class names")
        
        # Save if changes were made
        if content != original_content:
            # Create backup
            backup_dir = Path(filepath).parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            
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
        return False, [f"Error: {e}"]

# Main execution
if __name__ == "__main__":
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")
    
    print("=" * 70)
    print("COMPREHENSIVE FIX FOR ALL HTML ISSUES IN 01MODULE")
    print("=" * 70)
    
    # Get all HTML files
    html_files = list(module_dir.glob("*.html"))
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    files_modified = 0
    files_with_errors = 0
    total_fixes = 0
    
    # Process each file
    for filepath in sorted(html_files):
        print(f"Processing: {filepath.name}")
        modified, fixes = fix_html_file(filepath)
        
        if modified:
            files_modified += 1
            total_fixes += len(fixes)
            for fix in fixes:
                if fix.startswith("Error"):
                    print(f"  ❌ {fix}")
                    files_with_errors += 1
                else:
                    print(f"  ✅ {fix}")
        else:
            if fixes and any(f.startswith("Error") for f in fixes):
                print(f"  ❌ {fixes[0]}")
                files_with_errors += 1
            else:
                print(f"  ℹ️  No changes needed")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"Total files processed: {len(html_files)}")
    print(f"Files successfully modified: {files_modified}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Total fixes applied: {total_fixes}")
    
    if files_modified > 0:
        print(f"\n✅ Successfully fixed {files_modified} files!")
        print("📁 Backups have been created in the 'backups' subdirectory")
    else:
        print("\n✅ All files are already correct or no fixes could be applied!")
    
    if files_with_errors > 0:
        print(f"\n⚠️  {files_with_errors} files had errors during processing")
    
    print("\n" + "=" * 70)
