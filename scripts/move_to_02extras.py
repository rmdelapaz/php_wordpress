#!/usr/bin/env python3
"""
Move unlinked 02module files to 02extras folder
- Creates 02extras directory
- Moves all files not linked in module2.html
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

def get_linked_files():
    """Get list of files that ARE linked in module2.html."""
    # These are the files currently linked in module2.html
    linked_files = {
        'review_php_setup.html',
        'php_tags_basic_syntax.html',
        'php_output_methods.html',
        'php_comments.html',
        'php_variables_and_data_types.html',
        'php_constants.html',
        'homework_php_script.html',
        'php_arithmetic_operators.html',
        'php_assignment_operators.html',
        'php_comparison_operators.html',
        'php_logical_operators.html',
        'php_string_operators.html',
        # Note: php_array_operators.html has empty link but file exists
        'php_type_operators.html',
        'php_operator_precedence.html',
        'homework_php_calculator.html',
        'php_if.html',
        'php_if_else.html',
        'php_if_elseif_else.html',
        'php_switch.html',
        'php_ternary.html',
        'php_null_coalescing.html',
        'homework_php_grades.html',
        'php_for_loops.html',
        'php_while_loops.html',
        'php_do_while_loops.html',
        'php_foreach_loops_with_arrays.html',
        'php_control_break_continue.html',
        'homework_php_loops.html',
        'php_indexed_array.html',
        'php_associative_arrays.html',
        'php_multidimensional_arrays.html',
        'php_array_functions.html',
        'php_array_sorting.html',
        'php_array_iteration.html',
        'homework_php_array_creation_manipulation.html',
        'php_function_declaration_and_calling.html',
        'php_function_parameters_and return_values.html',
        'php_default_parameter_values.html',
        'php_variable_scope.html',
        'php_anonymoous_functions_and_closures.html',
        'php_built_in_php_functions_overview.html',
        'homework_php_create_library_custom_functions.html',
        'php_html_forms_review.html',
        'php_get_vs_post_methods.html',
        'php_accessing_form_data_get_post.html',
        'php_form_validation_techniques.html',
        'php_sanitizing_user_input.html',
        'php_file_uploads.html',
        # Note: homework_create_contact_form_validation.html is wrong name
        'php_oop_concepts.html',
        'php_creating_classes_and instantiating_objects.html',
        'php_constructor_and_destructor.html',
        'php_access_modifiers.html',
        # Note: php_this_keyword.html has empty link but file exists
        'php_static_properties_and_methods.html',
        'homework_php_create_simple_class.html',
        'php_inheritance.html',
        'php_method_overriding.html',
        'php_abstract_classes.html',
        'php_interfaces.html',
        'php_namespaces.html',
        'php_traits.html',
        'homework_php_extend_with_inheritance.html',
        'php_planning_php_application.html',
        'php_implementing_user_input.html',
        'php_working_with_sessions_cookies.html',
        'php_creating_reusable_php_components.html',
    }
    
    # Add the files with broken links that should stay
    # (they're referenced but with wrong names)
    linked_files.add('php_array_operators.html')  # Has empty href but should stay
    linked_files.add('php_this_keyword.html')     # Has empty href but should stay
    
    return linked_files

def get_unlinked_files():
    """Get list of files to move to 02extras."""
    # Complete list of files that should be moved
    unlinked_files = {
        # Framework Related
        'homework_framework_project.html',
        'intro_to_composer.html',
        'laravel_basics.html',
        'symfony_overview.html',
        
        # Database Related
        'crud_operations.html',
        'database_design.html',
        'intro_to_mysql.html',
        'php_mysql_connection.html',
        
        # Security
        'common_vulnerabilities.html',
        'homework_secure_app.html',
        'password_hashing.html',
        'secure_file_handling.html',
        
        # Testing
        'debugging_techniques.html',
        'homework_add_tests.html',
        'testing_deployment.html',
        'unit_testing_basics.html',
        
        # API Related
        'api_authentication.html',
        'consuming_apis.html',
        'creating_api_endpoints.html',
        'working_with_json.html',
        
        # Alternative/Duplicate Versions
        'php_array_functions_broke.html',
        'php_array_iteration_2.html',
        'php_creating_reusable_corrected.html',
        'php_sanitizing_user_input2.html',
        
        # Additional Exercises/Projects
        'final_project_blog_cms.html',
        'homework_contact_form.html',
        'homework_oop_project.html',
        'homework_optimization.html',
        'homework_php_create_contact_form_validation.html',
        'homework_user_management.html',
        'homework_weather_app.html',
        'project_php_dynamic_web_app_with_authentication.html',
        'project_planning.html',
        
        # Deep Dive Topics
        'control_structures_deep_dive.html',
        'performance_optimization.html',
        
        # Other Topics
        'arrays_and_data_manipulation.html',
        'classes_and_objects.html',
        'code_quality_tools.html',
        'error_handling.html',
        'file_uploads.html',
        'form_validation_sanitization.html',
        'functions_in_php.html',
        'handling_form_data.html',
        'implementing_features.html',
        'inheritance_and_polymorphism.html',
        'input_validation_techniques.html',
        'interfaces_and_abstract_classes.html',
        'intro_to_oop.html',
        'mvc_architecture.html',
        'namespaces_autoloading.html',
        'php_fundamentals_review.html',
        'php_setup_ubuntu.html',
        'prepared_statements.html',
        'regex_in_php.html',
        'sessions_and_cookies.html',
        'traits_and_generators.html',
    }
    
    return unlinked_files

def main():
    """Main function to move unlinked files to 02extras."""
    
    print("=" * 70)
    print("Moving Unlinked 02module Files to 02extras")
    print("=" * 70)
    
    # Get paths
    base_path = get_base_path()
    module_path = os.path.join(base_path, "02module")
    extras_path = os.path.join(base_path, "02extras")
    
    print(f"Base path: {base_path}")
    print(f"Source: {module_path}")
    print(f"Destination: {extras_path}")
    
    # Check if 02module exists
    if not os.path.exists(module_path):
        print(f"\n✗ Error: 02module directory not found at {module_path}")
        return
    
    # Create 02extras directory if it doesn't exist
    if not os.path.exists(extras_path):
        os.makedirs(extras_path)
        print(f"\n✓ Created directory: 02extras")
    else:
        print(f"\n✓ Directory exists: 02extras")
    
    # Get lists of files
    linked_files = get_linked_files()
    unlinked_files = get_unlinked_files()
    
    print(f"\nFiles to keep in 02module: {len(linked_files)}")
    print(f"Files to move to 02extras: {len(unlinked_files)}")
    
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
                print(f"  ⚠ {filename} already exists in 02extras - overwriting")
            
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
    
    # List remaining files in 02module
    print("\n" + "-" * 70)
    print("Files remaining in 02module:")
    print("-" * 70)
    
    remaining_files = []
    if os.path.exists(module_path):
        all_files = os.listdir(module_path)
        html_files = [f for f in all_files if f.endswith('.html') and not f.endswith('.backup')]
        remaining_files = sorted(html_files)
        
        print(f"Total HTML files remaining: {len(remaining_files)}")
        
        # Verify these are all linked files
        for file in remaining_files[:10]:  # Show first 10
            status = "✓" if file in linked_files else "⚠"
            print(f"  {status} {file}")
        
        if len(remaining_files) > 10:
            print(f"  ... and {len(remaining_files) - 10} more files")
    
    # List files now in 02extras
    print("\n" + "-" * 70)
    print("Files now in 02extras:")
    print("-" * 70)
    
    if os.path.exists(extras_path):
        extras_files = os.listdir(extras_path)
        html_extras = [f for f in extras_files if f.endswith('.html') and not f.endswith('.backup')]
        
        print(f"Total HTML files in 02extras: {len(html_extras)}")
        
        # Group by category for display
        categories = {
            'Framework': [],
            'Database': [],
            'Security': [],
            'API': [],
            'Testing': [],
            'Projects': [],
            'Other': []
        }
        
        for file in html_extras:
            if 'framework' in file or 'laravel' in file or 'symfony' in file or 'composer' in file:
                categories['Framework'].append(file)
            elif 'mysql' in file or 'database' in file or 'crud' in file:
                categories['Database'].append(file)
            elif 'secure' in file or 'password' in file or 'vulnerab' in file:
                categories['Security'].append(file)
            elif 'api' in file or 'json' in file:
                categories['API'].append(file)
            elif 'test' in file or 'debug' in file:
                categories['Testing'].append(file)
            elif 'project' in file or 'final' in file:
                categories['Projects'].append(file)
            else:
                categories['Other'].append(file)
        
        for category, files in categories.items():
            if files:
                print(f"\n  {category} ({len(files)} files):")
                for file in sorted(files)[:3]:  # Show first 3 of each category
                    print(f"    - {file}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")
    
    print("\n" + "=" * 70)
    print("✓ File reorganization complete!")
    print("\nNext steps:")
    print("1. Update module2.html to fix empty/broken links")
    print("2. Consider creating additional modules for advanced topics")
    print("3. Files in 02extras can be used for Module 3+ or advanced courses")
    print("=" * 70)

if __name__ == "__main__":
    # Confirm before proceeding
    print("This script will move unlinked files from 02module to 02extras.")
    print("This action will reorganize your file structure.")
    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        main()
    else:
        print("Operation cancelled.")
