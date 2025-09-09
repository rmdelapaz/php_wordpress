#!/usr/bin/env python3
"""
Move unlinked 03module files to 03extras folder
- Analyzes module3.html for linked files
- Creates 03extras directory
- Moves all files not linked in module3.html
- Preserves files for future use in other modules
- Works with Windows WSL paths
"""

import os
import shutil
import sys
from pathlib import Path

def get_base_path():
    """Get the correct base path for WSL or Windows environment."""
    if sys.platform == "win32" or os.path.exists(r"\\wsl$"):
        # Windows environment - use WSL path
        return r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
    else:
        # Linux/WSL environment
        return "/home/practicalace/projects/php_wordpress"

def get_linked_files_from_module3():
    """Extract list of files that ARE linked in module3.html."""
    # Based on the module3.html content, these files are linked
    linked_files = {
        # Session 1: Introduction to Databases
        'database_concepts_terminology.html',
        'types_of_databases.html',
        'introduction_to_mysql.html',
        'mysql_xampp_mamp.html',
        'using_phpmyadmin.html',
        'creating_databases_tables.html',
        'homework_database_schema.html',
        
        # Session 2: Database Design
        'data_modeling_concepts.html',
        'entity_relationship_diagrams.html',
        'normalization_principles.html',
        'primary_foreign_keys.html',
        'indexes_importance.html',
        'database_constraints.html',
        'homework_database_design.html',
        
        # Session 3: SQL Fundamentals
        'sql_syntax_conventions.html',
        'mysql_data_types.html',
        'database_structure_ddl.html',
        'insert_update_delete.html',
        'select_queries.html',
        'where_filtering.html',
        'order_by_sorting.html',
        'homework_sql_queries.html',  # Note: This appears twice in module3.html
        
        # Session 4: Advanced SQL
        'sql_joins.html',
        'aggregate_functions.html',
        'group_by_having.html',
        'having_deep_dive.html',
        'subqueries.html',
        'views.html',
        'transactions.html',
        'stored_procedures.html',
        # homework_sql_queries.html is referenced again here
        
        # Session 5: PHP and MySQL Integration
        'connecting_mysql.html',
        'executing_queries.html',
        'prepared_statements.html',
        'crud_operations.html',
        'result_sets.html',
        'error_debugging.html',
        'php_mysql_integration.html',
    }
    
    return linked_files

def get_all_files_in_03module(module_path):
    """Get all HTML files currently in 03module directory."""
    if not os.path.exists(module_path):
        return set()
    
    all_files = set()
    for file in os.listdir(module_path):
        # Only consider HTML files (not backups)
        if file.endswith('.html') and not any(backup in file for backup in ['.backup', '.mermaid_backup', '.diagram_backup']):
            all_files.add(file)
    
    return all_files

def analyze_module3():
    """Analyze which files should be moved to 03extras."""
    base_path = get_base_path()
    module_path = os.path.join(base_path, "03module")
    
    # Get linked files from module3.html
    linked_files = get_linked_files_from_module3()
    
    # Get all files in 03module
    all_files = get_all_files_in_03module(module_path)
    
    # Files to move are those not linked
    unlinked_files = all_files - linked_files
    
    return linked_files, unlinked_files, all_files

def main():
    """Main function to move unlinked files to 03extras."""
    
    print("=" * 70)
    print("Moving Unlinked 03module Files to 03extras")
    print("=" * 70)
    
    # Get paths
    base_path = get_base_path()
    module_path = os.path.join(base_path, "03module")
    extras_path = os.path.join(base_path, "03extras")
    
    print(f"Base path: {base_path}")
    print(f"Source: {module_path}")
    print(f"Destination: {extras_path}")
    
    # Check if 03module exists
    if not os.path.exists(module_path):
        print(f"\n✗ Error: 03module directory not found at {module_path}")
        return
    
    # Analyze files
    linked_files, unlinked_files, all_files = analyze_module3()
    
    print(f"\n=== FILE ANALYSIS ===")
    print(f"Total files in 03module: {len(all_files)}")
    print(f"Files linked in module3.html: {len(linked_files)}")
    print(f"Files to move to 03extras: {len(unlinked_files)}")
    
    if len(unlinked_files) == 0:
        print("\n✓ All files in 03module are linked in module3.html")
        print("No files need to be moved.")
        return
    
    # List unlinked files
    print("\n=== FILES TO BE MOVED ===")
    for file in sorted(unlinked_files):
        print(f"  - {file}")
    
    # Create 03extras directory if it doesn't exist
    if not os.path.exists(extras_path):
        os.makedirs(extras_path)
        print(f"\n✓ Created directory: 03extras")
    else:
        print(f"\n✓ Directory exists: 03extras")
    
    # Move files
    moved_count = 0
    skipped_count = 0
    error_count = 0
    backup_count = 0
    
    print("\n" + "-" * 70)
    print("Moving files...")
    print("-" * 70)
    
    for filename in sorted(unlinked_files):
        source_file = os.path.join(module_path, filename)
        dest_file = os.path.join(extras_path, filename)
        
        # Check if source file exists
        if not os.path.exists(source_file):
            print(f"  ⚬ Skipped {filename} (not found)")
            skipped_count += 1
            continue
        
        try:
            # Check if destination already exists
            if os.path.exists(dest_file):
                print(f"  ⚠ {filename} already exists in 03extras - overwriting")
            
            # Move the file
            shutil.move(source_file, dest_file)
            moved_count += 1
            print(f"  ✓ Moved {filename}")
            
            # Also move associated backup files if they exist
            backup_patterns = [
                f"{filename}.backup",
                f"{filename}.mermaid_backup",
                f"{filename}.diagram_backup",
                f"{filename}.backup_final",
                f"{filename}.backup2"
            ]
            
            for backup_pattern in backup_patterns:
                backup_source = os.path.join(module_path, backup_pattern)
                if os.path.exists(backup_source):
                    backup_dest = os.path.join(extras_path, backup_pattern)
                    shutil.move(backup_source, backup_dest)
                    backup_count += 1
                    print(f"    → Also moved backup: {backup_pattern}")
            
        except Exception as e:
            print(f"  ✗ Error moving {filename}: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"  Files moved: {moved_count}")
    print(f"  Backup files moved: {backup_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    
    # List remaining files in 03module
    print("\n" + "-" * 70)
    print("Files remaining in 03module:")
    print("-" * 70)
    
    remaining_files = []
    if os.path.exists(module_path):
        all_files = os.listdir(module_path)
        html_files = [f for f in all_files if f.endswith('.html') and not any(b in f for b in ['.backup', '.mermaid_backup', '.diagram_backup'])]
        remaining_files = sorted(html_files)
        
        print(f"Total HTML files remaining: {len(remaining_files)}")
        
        # Show all remaining files (should match linked files)
        if len(remaining_files) <= 40:  # Show all if reasonable number
            for file in remaining_files:
                status = "✓" if file in linked_files else "⚠"
                print(f"  {status} {file}")
        else:
            # Show first 10 and last 5
            for file in remaining_files[:10]:
                status = "✓" if file in linked_files else "⚠"
                print(f"  {status} {file}")
            print(f"  ... and {len(remaining_files) - 15} more files")
            for file in remaining_files[-5:]:
                status = "✓" if file in linked_files else "⚠"
                print(f"  {status} {file}")
    
    # List files now in 03extras
    if moved_count > 0:
        print("\n" + "-" * 70)
        print("Files now in 03extras:")
        print("-" * 70)
        
        if os.path.exists(extras_path):
            extras_files = os.listdir(extras_path)
            html_extras = [f for f in extras_files if f.endswith('.html') and not any(b in f for b in ['.backup', '.mermaid_backup', '.diagram_backup'])]
            
            print(f"Total HTML files in 03extras: {len(html_extras)}")
            
            for file in sorted(html_extras):
                print(f"  - {file}")
    
    # Check for any issues
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("-" * 70)
    
    # Check if homework_sql_queries.html exists (it's referenced twice)
    sql_queries_file = os.path.join(module_path, 'homework_sql_queries.html')
    if os.path.exists(sql_queries_file):
        print("✓ homework_sql_queries.html is present (referenced twice in module3.html)")
    else:
        print("⚠ homework_sql_queries.html is missing (but referenced in module3.html)")
    
    # Check for any potential issues
    issues = []
    
    # Check if all linked files exist
    missing_linked = []
    for file in linked_files:
        if not os.path.exists(os.path.join(module_path, file)):
            missing_linked.append(file)
    
    if missing_linked:
        print(f"\n⚠ Warning: {len(missing_linked)} linked files are missing from 03module:")
        for file in missing_linked:
            print(f"  - {file}")
    else:
        print("✓ All linked files are present in 03module")
    
    print("\n" + "=" * 70)
    if moved_count > 0:
        print("✓ File reorganization complete!")
        print(f"\n{moved_count} unlinked files have been moved to 03extras")
        print("These files can be used in other modules or advanced courses.")
    else:
        print("✓ Module 3 file structure is already optimized!")
        print("\nAll files in 03module are properly linked in module3.html")
    
    print("\nNext steps:")
    print("1. Verify module3.html links are working correctly")
    print("2. Consider using 03extras files for advanced database topics")
    print("3. Files in 03extras can be integrated into other modules as needed")
    print("=" * 70)

if __name__ == "__main__":
    # Analyze first
    print("Analyzing Module 3 file structure...")
    linked, unlinked, total = analyze_module3()
    
    if len(unlinked) == 0:
        print("\n✓ Good news! All files in 03module are properly linked.")
        print("No files need to be moved to 03extras.")
    else:
        print(f"\nFound {len(unlinked)} unlinked file(s) that should be moved to 03extras:")
        for file in sorted(unlinked):
            print(f"  - {file}")
        
        # Confirm before proceeding
        print("\nThis script will move these unlinked files from 03module to 03extras.")
        response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            main()
        else:
            print("Operation cancelled.")
