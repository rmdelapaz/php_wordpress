#!/usr/bin/env python3
"""
Script to fix the side navigation in 03module HTML files to match the consistent
functionality with dynamic lesson display per session.
Module 3: MySQL Database Development
"""

import os
import re
from bs4 import BeautifulSoup
import sys

def get_session_lessons(session_number):
    """Get all lessons for a specific session in Module 3."""
    session_lessons = {
        1: [  # Introduction to Databases
            {'file': '/03module/database_concepts_terminology.html', 'title': 'Database Concepts'},
            {'file': '/03module/types_of_databases.html', 'title': 'Types of Databases'},
            {'file': '/03module/introduction_to_mysql.html', 'title': 'Introduction to MySQL'},
            {'file': '/03module/mysql_xampp_mamp.html', 'title': 'MySQL in XAMPP/MAMP'},
            {'file': '/03module/using_phpmyadmin.html', 'title': 'Using phpMyAdmin'},
            {'file': '/03module/creating_databases_tables.html', 'title': 'Creating Databases'},
            {'file': '/03module/homework_database_schema.html', 'title': 'Homework: Database Schema'},
        ],
        2: [  # Database Design
            {'file': '/03module/data_modeling_concepts.html', 'title': 'Data Modeling'},
            {'file': '/03module/entity_relationship_diagrams.html', 'title': 'ER Diagrams'},
            {'file': '/03module/normalization_principles.html', 'title': 'Normalization'},
            {'file': '/03module/primary_foreign_keys.html', 'title': 'Keys & Relationships'},
            {'file': '/03module/indexes_importance.html', 'title': 'Indexes'},
            {'file': '/03module/database_constraints.html', 'title': 'Constraints'},
            {'file': '/03module/homework_database_design.html', 'title': 'Homework: Database Design'},
        ],
        3: [  # SQL Fundamentals
            {'file': '/03module/sql_syntax_conventions.html', 'title': 'SQL Syntax'},
            {'file': '/03module/mysql_data_types.html', 'title': 'Data Types'},
            {'file': '/03module/database_structure_ddl.html', 'title': 'DDL Commands'},
            {'file': '/03module/insert_update_delete.html', 'title': 'DML Commands'},
            {'file': '/03module/select_queries.html', 'title': 'SELECT Queries'},
            {'file': '/03module/where_filtering.html', 'title': 'WHERE Clauses'},
            {'file': '/03module/order_by_sorting.html', 'title': 'ORDER BY'},
            {'file': '/03module/homework_sql_queries.html', 'title': 'Homework: SQL Queries'},
        ],
        4: [  # Advanced SQL
            {'file': '/03module/sql_joins.html', 'title': 'SQL Joins'},
            {'file': '/03module/aggregate_functions.html', 'title': 'Aggregate Functions'},
            {'file': '/03module/group_by_having.html', 'title': 'GROUP BY'},
            {'file': '/03module/having_deep_dive.html', 'title': 'HAVING Clause'},
            {'file': '/03module/subqueries.html', 'title': 'Subqueries'},
            {'file': '/03module/views.html', 'title': 'Views'},
            {'file': '/03module/transactions.html', 'title': 'Transactions'},
            {'file': '/03module/stored_procedures.html', 'title': 'Stored Procedures'},
            {'file': '/03module/homework_advanced_sql.html', 'title': 'Homework: Advanced SQL'},
        ],
        5: [  # PHP and MySQL Integration
            {'file': '/03module/connecting_mysql.html', 'title': 'Connecting to MySQL'},
            {'file': '/03module/executing_queries.html', 'title': 'Executing Queries'},
            {'file': '/03module/prepared_statements.html', 'title': 'Prepared Statements'},
            {'file': '/03module/crud_operations.html', 'title': 'CRUD Operations'},
            {'file': '/03module/result_sets.html', 'title': 'Handling Results'},
            {'file': '/03module/error_debugging.html', 'title': 'Error Handling'},
            {'file': '/03module/php_mysql_integration.html', 'title': 'Project: PHP-MySQL App'},
        ],
    }
    return session_lessons.get(session_number, [])

def get_module_files(module_dir):
    """Get all HTML files in a module directory."""
    files = []
    if os.path.exists(module_dir):
        for file in os.listdir(module_dir):
            if file.endswith('.html'):
                files.append(os.path.join(module_dir, file))
    return sorted(files)

def get_session_navigation_info(current_file):
    """Get the previous and next session links based on current file."""
    # Map files to their sessions based on module3.html structure
    file_to_session = {
        # Session 1: Introduction to Databases
        'database_concepts_terminology.html': 1,
        'types_of_databases.html': 1,
        'introduction_to_mysql.html': 1,
        'intro_to_mysql.html': 1,  # Alternative name
        'mysql_xampp_mamp.html': 1,
        'using_phpmyadmin.html': 1,
        'creating_databases_tables.html': 1,
        'homework_database_schema.html': 1,
        
        # Session 2: Database Design
        'data_modeling_concepts.html': 2,
        'entity_relationship_diagrams.html': 2,
        'normalization_principles.html': 2,
        'primary_foreign_keys.html': 2,
        'indexes_importance.html': 2,
        'database_constraints.html': 2,
        'homework_database_design.html': 2,
        
        # Session 3: SQL Fundamentals
        'sql_syntax_conventions.html': 3,
        'mysql_data_types.html': 3,
        'database_structure_ddl.html': 3,
        'insert_update_delete.html': 3,
        'select_queries.html': 3,
        'where_filtering.html': 3,
        'order_by_sorting.html': 3,
        'homework_sql_queries.html': 3,
        
        # Session 4: Advanced SQL
        'sql_joins.html': 4,
        'aggregate_functions.html': 4,
        'group_by_having.html': 4,
        'having_deep_dive.html': 4,
        'subqueries.html': 4,
        'views.html': 4,
        'transactions.html': 4,
        'stored_procedures.html': 4,
        'homework_advanced_sql.html': 4,
        
        # Session 5: PHP and MySQL Integration
        'connecting_mysql.html': 5,
        'executing_queries.html': 5,
        'prepared_statements.html': 5,
        'crud_operations.html': 5,
        'result_sets.html': 5,
        'error_debugging.html': 5,
        'php_mysql_integration.html': 5,
        
        # Additional files that may exist in the folder
        'mysql_intro.html': 1,
        'mysql_setup.html': 1,
        'database_basics.html': 1,
        'relational_databases.html': 1,
        'nosql_overview.html': 1,
        'database_tools.html': 1,
        'phpmyadmin_tutorial.html': 1,
        'mysql_workbench.html': 1,
        'command_line_mysql.html': 1,
        
        'database_design_principles.html': 2,
        'er_modeling.html': 2,
        'normalization.html': 2,
        'denormalization.html': 2,
        'relationships.html': 2,
        'foreign_keys.html': 2,
        'composite_keys.html': 2,
        'indexing_strategies.html': 2,
        'performance_optimization.html': 2,
        
        'sql_basics.html': 3,
        'ddl_commands.html': 3,
        'dml_commands.html': 3,
        'create_table.html': 3,
        'alter_table.html': 3,
        'drop_table.html': 3,
        'insert_data.html': 3,
        'update_data.html': 3,
        'delete_data.html': 3,
        'select_basics.html': 3,
        'where_clause.html': 3,
        'order_by.html': 3,
        'limit_offset.html': 3,
        
        'inner_join.html': 4,
        'left_join.html': 4,
        'right_join.html': 4,
        'full_join.html': 4,
        'cross_join.html': 4,
        'self_join.html': 4,
        'multiple_joins.html': 4,
        'count_sum_avg.html': 4,
        'min_max.html': 4,
        'group_by.html': 4,
        'having_clause.html': 4,
        'nested_queries.html': 4,
        'correlated_subqueries.html': 4,
        'exists_not_exists.html': 4,
        'in_not_in.html': 4,
        'any_all.html': 4,
        'creating_views.html': 4,
        'updateable_views.html': 4,
        'transaction_basics.html': 4,
        'commit_rollback.html': 4,
        'isolation_levels.html': 4,
        'deadlocks.html': 4,
        'stored_procs.html': 4,
        'functions.html': 4,
        'triggers.html': 4,
        'events.html': 4,
        
        'mysqli_connection.html': 5,
        'pdo_connection.html': 5,
        'connection_handling.html': 5,
        'query_execution.html': 5,
        'prepared_stmt.html': 5,
        'bind_parameters.html': 5,
        'sql_injection.html': 5,
        'security_best_practices.html': 5,
        'create_read.html': 5,
        'update_delete.html': 5,
        'fetch_data.html': 5,
        'fetch_assoc.html': 5,
        'fetch_array.html': 5,
        'fetch_object.html': 5,
        'num_rows.html': 5,
        'affected_rows.html': 5,
        'last_insert_id.html': 5,
        'error_handling.html': 5,
        'debugging_queries.html': 5,
        'query_logging.html': 5,
        'final_project.html': 5,
        'crud_project.html': 5,
        'user_management.html': 5,
        'blog_database.html': 5,
        'ecommerce_database.html': 5,
    }
    
    # First lesson of each session - VERIFIED from module3.html
    session_first_lessons = {
        1: {'file': '/03module/database_concepts_terminology.html', 'title': 'Session 1: Databases'},
        2: {'file': '/03module/data_modeling_concepts.html', 'title': 'Session 2: Design'},
        3: {'file': '/03module/sql_syntax_conventions.html', 'title': 'Session 3: SQL Basics'},
        4: {'file': '/03module/sql_joins.html', 'title': 'Session 4: Advanced SQL'},
        5: {'file': '/03module/connecting_mysql.html', 'title': 'Session 5: PHP-MySQL'},
    }
    
    # Get filename from path
    import os
    filename = os.path.basename(current_file)
    
    # Get current session
    current_session = file_to_session.get(filename)
    
    if not current_session:
        print(f"  ⚠ Warning: No session mapping for {filename}")
        return None
    
    result = {'current_session': current_session}
    
    # Get previous session link
    if current_session > 1:
        prev_session = current_session - 1
        result['prev'] = session_first_lessons[prev_session]['file']
        result['prev_title'] = session_first_lessons[prev_session]['title']
    else:
        # Link to Module 2 last session (Session 10)
        result['prev'] = '/02module/php_planning_php_application.html'
        result['prev_title'] = 'Module 2: Project'
    
    # Get next session link  
    if current_session < 5:
        next_session = current_session + 1
        result['next'] = session_first_lessons[next_session]['file']
        result['next_title'] = session_first_lessons[next_session]['title']
    elif current_session == 5:
        # Last session links to Module 4 first lesson
        result['next'] = '/04module/intro_to_wordpress.html'
        result['next_title'] = 'Module 4: WordPress'
    
    return result

def create_03module_navigation(current_file=None):
    """Create the proper navigation structure for Module 3."""
    # Get session navigation info if current file is provided
    prev_session_html = ""
    next_session_html = ""
    current_session_num = ""
    session_lessons_html = ""
    current_session = None
    
    if current_file:
        nav_info = get_session_navigation_info(current_file)
        if nav_info:
            current_session = nav_info['current_session']
            # Get current session number for the header
            current_session_num = f"Session {current_session}"
            
            # Add previous session link if available
            if 'prev' in nav_info:
                prev_session_html = f'''                                    <li><a href="{nav_info['prev']}" class="sidebar-link prev-session">← Prev: {nav_info['prev_title']}</a></li>\n'''
            
            # Add next session link if available
            if 'next' in nav_info:
                next_session_html = f'''                                    <li><a href="{nav_info['next']}" class="sidebar-link next-session">Next: {nav_info['next_title']} →</a></li>\n'''
            
            # Get lessons for current session
            lessons = get_session_lessons(current_session)
            if lessons:
                lesson_items = []
                for lesson in lessons:
                    lesson_items.append(f'''                                    <li><a href="{lesson['file']}" class="sidebar-link">{lesson['title']}</a></li>''')
                session_lessons_html = '\n'.join(lesson_items)
    
    # If no current session, default to "Sessions" and show all session links
    if not current_session_num:
        current_session_num = "Sessions"
        # Show all sessions as overview
        session_lessons_html = '''                                    <li><a href="/03module/database_concepts_terminology.html" class="sidebar-link">Session 1: Databases</a></li>
                                    <li><a href="/03module/data_modeling_concepts.html" class="sidebar-link">Session 2: Design</a></li>
                                    <li><a href="/03module/sql_syntax_conventions.html" class="sidebar-link">Session 3: SQL Basics</a></li>
                                    <li><a href="/03module/sql_joins.html" class="sidebar-link">Session 4: Advanced SQL</a></li>
                                    <li><a href="/03module/connecting_mysql.html" class="sidebar-link">Session 5: PHP-MySQL</a></li>'''
    
    navigation_html = f'''<div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 3: MySQL Database</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">{current_session_num}</h4>
                                <ul class="sidebar-menu">
{session_lessons_html}
                                </ul>
                            </div>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Quick Links</h4>
                                <ul class="sidebar-menu">
                                    <li><a href="/module3.html" class="sidebar-link">Module Overview</a></li>
{prev_session_html}{next_session_html}                                    <li><a href="/module2.html" class="sidebar-link">← Previous Module</a></li>
                                    <li><a href="/module4.html" class="sidebar-link">Next Module →</a></li>
                                    <li><a href="/resources.html" class="sidebar-link">Resources</a></li>
                                </ul>
                            </div>
                        </div>'''
    return navigation_html

def get_current_page_from_file(filepath):
    """Determine which page is current based on the filename."""
    filename = os.path.basename(filepath)
    # Map filenames to their lesson titles as shown in sidebar
    page_map = {
        # Session 1: Introduction to Databases
        'database_concepts_terminology.html': 'Database Concepts',
        'types_of_databases.html': 'Types of Databases',
        'introduction_to_mysql.html': 'Introduction to MySQL',
        'intro_to_mysql.html': 'Introduction to MySQL',
        'mysql_xampp_mamp.html': 'MySQL in XAMPP/MAMP',
        'using_phpmyadmin.html': 'Using phpMyAdmin',
        'creating_databases_tables.html': 'Creating Databases',
        'homework_database_schema.html': 'Homework: Database Schema',
        
        # Session 2: Database Design
        'data_modeling_concepts.html': 'Data Modeling',
        'entity_relationship_diagrams.html': 'ER Diagrams',
        'normalization_principles.html': 'Normalization',
        'primary_foreign_keys.html': 'Keys & Relationships',
        'indexes_importance.html': 'Indexes',
        'database_constraints.html': 'Constraints',
        'homework_database_design.html': 'Homework: Database Design',
        
        # Session 3: SQL Fundamentals
        'sql_syntax_conventions.html': 'SQL Syntax',
        'mysql_data_types.html': 'Data Types',
        'database_structure_ddl.html': 'DDL Commands',
        'insert_update_delete.html': 'DML Commands',
        'select_queries.html': 'SELECT Queries',
        'where_filtering.html': 'WHERE Clauses',
        'order_by_sorting.html': 'ORDER BY',
        'homework_sql_queries.html': 'Homework: SQL Queries',
        
        # Session 4: Advanced SQL
        'sql_joins.html': 'SQL Joins',
        'aggregate_functions.html': 'Aggregate Functions',
        'group_by_having.html': 'GROUP BY',
        'having_deep_dive.html': 'HAVING Clause',
        'subqueries.html': 'Subqueries',
        'views.html': 'Views',
        'transactions.html': 'Transactions',
        'stored_procedures.html': 'Stored Procedures',
        'homework_advanced_sql.html': 'Homework: Advanced SQL',
        
        # Session 5: PHP and MySQL Integration
        'connecting_mysql.html': 'Connecting to MySQL',
        'executing_queries.html': 'Executing Queries',
        'prepared_statements.html': 'Prepared Statements',
        'crud_operations.html': 'CRUD Operations',
        'result_sets.html': 'Handling Results',
        'error_debugging.html': 'Error Handling',
        'php_mysql_integration.html': 'Project: PHP-MySQL App',
        
        # Additional possible files
        'mysql_intro.html': 'Introduction to MySQL',
        'database_basics.html': 'Database Basics',
        'sql_basics.html': 'SQL Basics',
        'inner_join.html': 'Inner Join',
        'left_join.html': 'Left Join',
        'mysqli_connection.html': 'MySQLi Connection',
        'pdo_connection.html': 'PDO Connection',
        'final_project.html': 'Final Project',
    }
    return page_map.get(filename, '')

def update_navigation_with_active(navigation_html, current_page):
    """Add the 'active' class to the current page in navigation."""
    if not current_page:
        return navigation_html
    
    # Parse the navigation HTML
    soup = BeautifulSoup(navigation_html, 'html.parser')
    
    # Find all sidebar links
    all_links = soup.find_all('a', class_='sidebar-link')
    
    for link in all_links:
        # Skip next-session, prev-session and other special links
        if 'next-session' in link.get('class', []) or 'prev-session' in link.get('class', []):
            continue
            
        # Get the link text
        link_text = link.get_text(strip=True)
        
        # Check if this is the current page
        if link_text == current_page:
            # Add active class to the link
            current_classes = link.get('class', [])
            if 'active' not in current_classes:
                current_classes.append('active')
                link['class'] = current_classes
            
            # Also add active class to the parent li if it exists
            parent_li = link.find_parent('li')
            if parent_li:
                li_classes = parent_li.get('class', [])
                if 'active' not in li_classes:
                    li_classes.append('active')
                    parent_li['class'] = li_classes
        else:
            # Remove active class if present
            current_classes = link.get('class', [])
            if 'active' in current_classes:
                current_classes.remove('active')
                link['class'] = current_classes
            
            # Also remove from parent li
            parent_li = link.find_parent('li')
            if parent_li:
                li_classes = parent_li.get('class', [])
                if 'active' in li_classes:
                    li_classes.remove('active')
                    if li_classes:
                        parent_li['class'] = li_classes
                    else:
                        del parent_li['class']
    
    return str(soup)

def add_sidebar_assets(soup):
    """Add sidebar enhancement CSS and toggle functionality to the HTML."""
    added_something = False
    head = soup.find('head')
    
    if head:
        # Check and add sidebar-enhanced.css
        existing_enhanced_css = soup.find('link', {'href': '/assets/css/sidebar-enhanced.css'})
        if not existing_enhanced_css:
            enhanced_css = soup.new_tag('link', rel='stylesheet', href='/assets/css/sidebar-enhanced.css')
            main_css = head.find('link', {'href': '/assets/css/main.css'})
            if main_css:
                main_css.insert_after(enhanced_css)
            else:
                head.append(enhanced_css)
            added_something = True
        
        # Check and add sidebar-toggle.css
        existing_toggle_css = soup.find('link', {'href': '/assets/css/sidebar-toggle.css'})
        if not existing_toggle_css:
            toggle_css = soup.new_tag('link', rel='stylesheet', href='/assets/css/sidebar-toggle.css')
            # Add after sidebar-enhanced.css
            enhanced_css_link = head.find('link', {'href': '/assets/css/sidebar-enhanced.css'})
            if enhanced_css_link:
                enhanced_css_link.insert_after(toggle_css)
            else:
                main_css = head.find('link', {'href': '/assets/css/main.css'})
                if main_css:
                    main_css.insert_after(toggle_css)
                else:
                    head.append(toggle_css)
            added_something = True
    
    # Add JS before closing body tag
    body = soup.find('body')
    if body:
        # Check if sidebar-toggle.js already exists
        existing_toggle_js = soup.find('script', {'src': '/assets/js/sidebar-toggle.js'})
        if not existing_toggle_js:
            toggle_js = soup.new_tag('script', src='/assets/js/sidebar-toggle.js')
            body.append(toggle_js)
            added_something = True
    
    return added_something

def fix_navigation_in_file(filepath, navigation_template):
    """Fix the navigation in a single HTML file."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the sidebar nav
        sidebar_nav = soup.find('div', class_='sidebar-nav')
        
        if not sidebar_nav:
            # Try to find the sidebar container
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                # Clear existing content and add new navigation
                sidebar.clear()
                new_nav = BeautifulSoup(navigation_template, 'html.parser')
                sidebar.append(new_nav)
                print(f"  ✓ Added navigation structure to sidebar")
            else:
                print(f"  ⚠ Warning: No sidebar found")
                return False
        else:
            # Replace existing navigation
            parent = sidebar_nav.parent
            sidebar_nav.decompose()
            new_nav = BeautifulSoup(navigation_template, 'html.parser')
            parent.append(new_nav)
            print(f"  ✓ Replaced existing navigation")
        
        # Get the current page and update active state
        current_page = get_current_page_from_file(filepath)
        if current_page:
            # Find the newly added sidebar-nav and update it
            sidebar_nav = soup.find('div', class_='sidebar-nav')
            if sidebar_nav:
                updated_nav = update_navigation_with_active(str(sidebar_nav), current_page)
                new_sidebar_nav = BeautifulSoup(updated_nav, 'html.parser').find('div', class_='sidebar-nav')
                sidebar_nav.replace_with(new_sidebar_nav)
                print(f"  ✓ Set active state for: {current_page}")
        else:
            print(f"  ⚠ Could not determine current page for: {os.path.basename(filepath)}")
        
        # Add sidebar assets (enhanced CSS and toggle functionality)
        if add_sidebar_assets(soup):
            print(f"  ✓ Added sidebar enhancements and toggle")
        
        # Write the updated content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  ✓ Successfully updated {os.path.basename(filepath)}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to fix navigation in all 03module files."""
    
    # Define paths
    if os.path.exists(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\03module"):
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
        print(f"Using Windows WSL path: {base_path}")
    elif os.path.exists("/home/practicalace/projects/php_wordpress/03module"):
        base_path = "/home/practicalace/projects/php_wordpress"
        print(f"Using Linux path: {base_path}")
    else:
        base_path = os.getcwd()
        print(f"Using current directory: {base_path}")
        
    module03_dir = os.path.join(base_path, "03module")
    
    print(f"\nLooking for Module 3 files in: {module03_dir}")
    print(f"Directory exists: {os.path.exists(module03_dir)}")
    
    print("=" * 60)
    print("Module 3: MySQL Database - Navigation Fixer")
    print("=" * 60)
    
    # Show module structure
    print("\n📚 Module 3 Structure (5 Sessions):")
    print("  Session 1: Introduction to Databases")
    print("  Session 2: Database Design")
    print("  Session 3: SQL Fundamentals")
    print("  Session 4: Advanced SQL")
    print("  Session 5: PHP and MySQL Integration")
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nDo you want to proceed with fixing the navigation? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Process all Module 3 HTML files
    print("\n" + "=" * 60)
    print("\nUpdating Module 3 files...")
    print("=" * 60 + "\n")
    
    files = get_module_files(str(module03_dir))
    
    if not files:
        print(f"No HTML files found in {module03_dir}")
        return
    
    success_count = 0
    fail_count = 0
    
    for filepath in files:
        print(f"Processing: {os.path.basename(filepath)}")
        
        # Get the current page for this file
        current_page = get_current_page_from_file(filepath)
        
        # Create navigation with active state AND next session link for this specific file
        nav_template = create_03module_navigation(filepath)
        nav_with_active = update_navigation_with_active(nav_template, current_page)
        
        # Fix the navigation
        if fix_navigation_in_file(filepath, nav_with_active):
            success_count += 1
        else:
            fail_count += 1
        print()  # Empty line for readability
    
    # Summary
    print("=" * 60)
    print("\nSummary:")
    print(f"  ✓ Successfully updated: {success_count} files")
    if fail_count > 0:
        print(f"  ✗ Failed: {fail_count} files")
    print("\n✅ Module 3 navigation fix complete!")

if __name__ == "__main__":
    main()
