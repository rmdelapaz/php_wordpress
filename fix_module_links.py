#!/usr/bin/env python3
"""
Update all links in moved HTML files from 07module, 08module, 09module to 06module
"""

import os
import re
from pathlib import Path

def update_file_links(filepath):
    """Update all module links in a single file"""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Keep original for comparison
        original_content = content
        
        # Replace all variations of module links
        replacements = [
            # href attributes
            ('href="/07module/', 'href="/06module/'),
            ('href="/08module/', 'href="/06module/'),
            ('href="/09module/', 'href="/06module/'),
            # Links to next module (Session 10)
            ('href="/10module/', 'href="/07module/'),
            # Any other references
            ('/07module/', '/06module/'),
            ('/08module/', '/06module/'),
            ('/09module/', '/06module/'),
        ]
        
        changes_made = []
        for old_text, new_text in replacements:
            if old_text in content:
                count = content.count(old_text)
                content = content.replace(old_text, new_text)
                changes_made.append(f"  Replaced {count} instances of '{old_text}'")
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made
        
        return []
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def main():
    # Set the base path
    base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\06module"
    
    # List of files that were moved from 07module, 08module, 09module
    moved_files = [
        # From 07module (Session 7: AJAX)
        'ajax_overview.html',
        'ajax_handlers.html',
        'admin_frontend_ajax.html',
        'ajax_security.html',
        'ajax_error_handling.html',
        'loading_scripts.html',
        'homework_ajax_plugin.html',
        
        # From 08module (Session 8: REST API)
        'rest_api_intro.html',
        'endpoints_routes.html',
        'using_rest_api.html',
        'custom_endpoints.html',
        'authentication.html',
        'extending_endpoints.html',
        'homework_rest_api.html',
        
        # From 09module (Session 9: Security & Performance)
        'security_principles.html',
        'input_validation.html',
        'capability_checks.html',
        'data_encryption.html',
        'preventing_attacks.html',
        'performance_optimization.html',
        'caching_strategies.html',
        'homework_security_audit.html'
    ]
    
    print("=" * 60)
    print("Updating Links in Moved HTML Files")
    print("=" * 60)
    print(f"Base path: {base_path}")
    print(f"Files to update: {len(moved_files)}")
    print("-" * 60)
    
    # Track statistics
    files_updated = 0
    files_not_found = 0
    files_no_changes = 0
    
    # Process each file
    for filename in moved_files:
        filepath = os.path.join(base_path, filename)
        
        if os.path.exists(filepath):
            print(f"\nProcessing: {filename}")
            changes = update_file_links(filepath)
            
            if changes:
                files_updated += 1
                for change in changes:
                    print(change)
            else:
                files_no_changes += 1
                print("  No changes needed")
        else:
            files_not_found += 1
            print(f"\n❌ File not found: {filename}")
            print(f"   Full path: {filepath}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Files updated: {files_updated}")
    print(f"➖ Files with no changes: {files_no_changes}")
    print(f"❌ Files not found: {files_not_found}")
    print(f"📁 Total files processed: {len(moved_files)}")
    
    if files_updated > 0:
        print("\n✅ Link updates completed successfully!")
    elif files_not_found > 0:
        print("\n⚠️  Some files were not found. Check the file paths.")
    else:
        print("\n✅ All files already have correct links!")

if __name__ == "__main__":
    main()
