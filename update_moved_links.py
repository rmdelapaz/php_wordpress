#!/usr/bin/env python3
"""
Update links in moved HTML files from 07module, 08module, 09module to 06module
"""

import os
from pathlib import Path

def update_links_in_file(file_path):
    """Update all links in a single HTML file"""
    updates_made = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all occurrences of /07module/, /08module/, /09module/ with /06module/
        replacements = [
            ('/07module/', '/06module/'),
            ('/08module/', '/06module/'),
            ('/09module/', '/06module/'),
        ]
        
        for old_path, new_path in replacements:
            count = content.count(old_path)
            if count > 0:
                content = content.replace(old_path, new_path)
                updates_made.append(f"Replaced {count} occurrences of '{old_path}' with '{new_path}'")
        
        # Save the file if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return updates_made
        
    except Exception as e:
        print(f"Error updating {file_path.name}: {e}")
        return []
    
    return []

def main():
    """Main function to update all moved files"""
    base_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\06module")
    
    # List of files that were moved
    files_to_update = [
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
    
    total_files_updated = 0
    
    for filename in files_to_update:
        file_path = base_path / filename
        
        if file_path.exists():
            print(f"\nProcessing: {filename}")
            updates = update_links_in_file(file_path)
            
            if updates:
                total_files_updated += 1
                for update in updates:
                    print(f"  • {update}")
            else:
                print(f"  • No updates needed")
        else:
            print(f"\n⚠️  File not found: {filename}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(files_to_update)}")
    print(f"Files updated: {total_files_updated}")
    print("\n✅ Link update completed successfully!")

if __name__ == "__main__":
    main()
