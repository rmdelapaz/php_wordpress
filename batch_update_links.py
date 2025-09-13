#!/usr/bin/env python3
"""
Simple script to update links in all moved HTML files
"""

import os
from pathlib import Path

# Base path
base_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\06module")

# List of all files that were moved
files_to_update = [
    # From 07module
    'ajax_overview.html',
    'ajax_handlers.html',
    'admin_frontend_ajax.html',
    'ajax_security.html',
    'ajax_error_handling.html',
    'loading_scripts.html',
    'homework_ajax_plugin.html',
    # From 08module
    'rest_api_intro.html',
    'endpoints_routes.html',
    'using_rest_api.html',
    'custom_endpoints.html',
    'authentication.html',
    'extending_endpoints.html',
    'homework_rest_api.html',
    # From 09module
    'security_principles.html',
    'input_validation.html',
    'capability_checks.html',
    'data_encryption.html',
    'preventing_attacks.html',
    'performance_optimization.html',
    'caching_strategies.html',
    'homework_security_audit.html'
]

updated_count = 0

for filename in files_to_update:
    file_path = base_path / filename
    
    if file_path.exists():
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all module references
            original = content
            content = content.replace('/07module/', '/06module/')
            content = content.replace('/08module/', '/06module/')
            content = content.replace('/09module/', '/06module/')
            content = content.replace('/10module/', '/07module/')  # Fix next session links
            
            # Write back if changed
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                print(f"✓ Updated: {filename}")
            else:
                print(f"  No changes: {filename}")
                
        except Exception as e:
            print(f"✗ Error updating {filename}: {e}")
    else:
        print(f"⚠ File not found: {filename}")

print(f"\n✅ Updated {updated_count} files successfully!")
