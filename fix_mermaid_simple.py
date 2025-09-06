#!/usr/bin/env python3
"""
Fix common HTML issues in 01module files - Simplified version
"""

import os
import re
from pathlib import Path

def fix_mermaid_issues(filepath):
    """Fix mermaid-related issues in a single file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes_made = []
    
    # Fix 1: Add missing securityLevel to mermaid initialization
    if 'mermaid.initialize' in content and 'securityLevel' not in content:
        # Find the mermaid initialization and add securityLevel
        pattern = r'(mermaid\.initialize\(\s*\{[^}]*?flowchart:\s*\{[^}]*?\})'
        replacement = r'\1,\n            securityLevel: "loose"'
        content = re.sub(pattern, replacement, content)
        if content != original_content:
            fixes_made.append("Added securityLevel to mermaid init")
    
    # Fix 2: Fix mermaid closing tags (</div> should be </pre>)
    # Look for <pre class="mermaid"> followed eventually by </div>
    pattern = r'(<pre\s+class="mermaid">(?:(?!</pre>).)*?)</div>'
    
    def fix_closing(match):
        return match.group(1) + '</pre>'
    
    new_content = re.sub(pattern, fix_closing, content, flags=re.DOTALL)
    if new_content != content:
        fixes_made.append("Fixed mermaid closing tags")
        content = new_content
    
    # Save if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixes_made
    
    return False, []

# Main execution
module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")

# Test on specific problem files first
test_files = [
    "js_syntax_fundamentals.html",
    "js_control_flow.html",
    "js_operators_and_expressions.html"
]

print("Fixing HTML issues in 01module files...")
print("=" * 60)

for filename in test_files:
    filepath = module_dir / filename
    if filepath.exists():
        print(f"\nProcessing: {filename}")
        modified, fixes = fix_mermaid_issues(filepath)
        if modified:
            print(f"  ✅ Fixed: {', '.join(fixes)}")
        else:
            print(f"  ℹ️ No changes needed")
    else:
        print(f"\n❌ File not found: {filename}")

print("\n" + "=" * 60)
print("Fix process complete!")
