#!/usr/bin/env python3
"""
Verify that all HTML files are correctly referencing mermaid-universal-fix.js
"""

import os
import re

def check_mermaid_references(filepath):
    """Check if a file has correct Mermaid references"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for old v2 references
        if 'mermaid-fix-v2' in content:
            issues.append("Contains reference to mermaid-fix-v2.js")
        
        # Check for incorrect paths
        if 'mermaid-universal-fix.js' in content:
            # Extract the actual script tags
            script_matches = re.findall(r'<script[^>]*src="([^"]*mermaid-universal-fix\.js)"[^>]*>', content)
            for match in script_matches:
                if match != '/assets/js/mermaid-universal-fix.js':
                    issues.append(f"Incorrect path: {match}")
        
        # Check if file has Mermaid content but no fix
        has_mermaid = ('class="mermaid"' in content or 
                      'pre class="mermaid"' in content or
                      'class="mermaid-container"' in content)
        
        if has_mermaid and 'mermaid-universal-fix.js' not in content:
            issues.append("Has Mermaid content but no fix script")
        
        return issues
        
    except Exception as e:
        return [f"Error reading file: {e}"]

def main():
    """Main function to check all HTML files"""
    
    # Get the current directory
    if os.name == 'nt':  # Windows
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:  # Linux/Unix
        base_dir = os.getcwd()
    
    print("Verifying Mermaid references in all HTML files...")
    print("=" * 60)
    
    # Check 01module directory
    module_dir = os.path.join(base_dir, '01module')
    
    if os.path.exists(module_dir):
        html_files = [f for f in os.listdir(module_dir) if f.endswith('.html')]
        
        files_with_issues = 0
        total_files = len(html_files)
        
        for filename in sorted(html_files):
            filepath = os.path.join(module_dir, filename)
            issues = check_mermaid_references(filepath)
            
            if issues:
                files_with_issues += 1
                print(f"\n❌ {filename}:")
                for issue in issues:
                    print(f"   - {issue}")
        
        if files_with_issues == 0:
            print("\n✅ All files have correct Mermaid references!")
        else:
            print(f"\n\nSummary:")
            print(f"  Total files checked: {total_files}")
            print(f"  Files with issues: {files_with_issues}")
            print(f"  Files OK: {total_files - files_with_issues}")
    else:
        print(f"Error: Directory not found: {module_dir}")
    
    # Check if the mermaid-universal-fix.js file exists
    mermaid_file = os.path.join(base_dir, 'assets', 'js', 'mermaid-universal-fix.js')
    if os.path.exists(mermaid_file):
        print(f"\n✅ mermaid-universal-fix.js exists at the correct location")
    else:
        print(f"\n❌ mermaid-universal-fix.js NOT FOUND at {mermaid_file}")

if __name__ == "__main__":
    main()
