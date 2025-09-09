#!/usr/bin/env python3
"""
Script to fix the side navigation in 02module HTML files to match the consistent
functionality with dynamic lesson display per session.
Module 2: PHP Fundamentals
"""

import os
import re
from bs4 import BeautifulSoup
import sys

def get_session_lessons(session_number):
    """Get all lessons for a specific session in Module 2."""
    session_lessons = {
        1: [  # PHP Setup and Syntax
            {'file': '/02module/review_php_setup.html', 'title': 'Review PHP Setup'},
            {'file': '/02module/php_tags_basic_syntax.html', 'title': 'PHP Tags & Syntax'},
            {'file': '/02module/php_output_methods.html', 'title': 'Output Methods'},
            {'file': '/02module/php_comments.html', 'title': 'Comments in PHP'},
            {'file': '/02module/php_variables_and_data_types.html', 'title': 'Variables & Data Types'},
            {'file': '/02module/php_constants.html', 'title': 'Constants'},
            {'file': '/02module/homework_php_script.html', 'title': 'Homework: PHP Script'},
        ],
        2: [  # Operators and Expressions
            {'file': '/02module/php_arithmetic_operators.html', 'title': 'Arithmetic Operators'},
            {'file': '/02module/php_assignment_operators.html', 'title': 'Assignment Operators'},
            {'file': '/02module/php_comparison_operators.html', 'title': 'Comparison Operators'},
            {'file': '/02module/php_logical_operators.html', 'title': 'Logical Operators'},
            {'file': '/02module/php_string_operators.html', 'title': 'String Operators'},
            {'file': '/02module/php_array_operators.html', 'title': 'Array Operators'},
            {'file': '/02module/php_type_operators.html', 'title': 'Type Operators'},
            {'file': '/02module/php_operator_precedence.html', 'title': 'Operator Precedence'},
            {'file': '/02module/homework_php_calculator.html', 'title': 'Homework: Calculator'},
        ],
        3: [  # Control Structures - Conditionals
            {'file': '/02module/php_if.html', 'title': 'If Statements'},
            {'file': '/02module/php_if_else.html', 'title': 'If-Else Statements'},
            {'file': '/02module/php_if_elseif_else.html', 'title': 'If-Elseif-Else'},
            {'file': '/02module/php_switch.html', 'title': 'Switch Statements'},
            {'file': '/02module/php_ternary.html', 'title': 'Ternary Operator'},
            {'file': '/02module/php_null_coalescing.html', 'title': 'Null Coalescing'},
            {'file': '/02module/homework_php_grades.html', 'title': 'Homework: Grades'},
        ],
        4: [  # Control Structures - Loops
            {'file': '/02module/php_for_loops.html', 'title': 'For Loops'},
            {'file': '/02module/php_while_loops.html', 'title': 'While Loops'},
            {'file': '/02module/php_do_while_loops.html', 'title': 'Do-While Loops'},
            {'file': '/02module/php_foreach_loops_with_arrays.html', 'title': 'Foreach Loops'},
            {'file': '/02module/php_control_break_continue.html', 'title': 'Break & Continue'},
            {'file': '/02module/homework_php_loops.html', 'title': 'Homework: Loops'},
        ],
        5: [  # Arrays
            {'file': '/02module/php_indexed_array.html', 'title': 'Indexed Arrays'},
            {'file': '/02module/php_associative_arrays.html', 'title': 'Associative Arrays'},
            {'file': '/02module/php_multidimensional_arrays.html', 'title': 'Multidimensional Arrays'},
            {'file': '/02module/php_array_functions.html', 'title': 'Array Functions'},
            {'file': '/02module/php_array_sorting.html', 'title': 'Array Sorting'},
            {'file': '/02module/php_array_iteration.html', 'title': 'Array Iteration'},
            {'file': '/02module/homework_php_array_creation_manipulation.html', 'title': 'Homework: Arrays'},
        ],
        6: [  # Functions
            {'file': '/02module/php_function_declaration_and_calling.html', 'title': 'Function Declaration'},
            {'file': '/02module/php_function_parameters_and return_values.html', 'title': 'Parameters & Returns'},
            {'file': '/02module/php_default_parameter_values.html', 'title': 'Default Parameters'},
            {'file': '/02module/php_variable_scope.html', 'title': 'Variable Scope'},
            {'file': '/02module/php_anonymoous_functions_and_closures.html', 'title': 'Anonymous Functions'},
            {'file': '/02module/php_built_in_php_functions_overview.html', 'title': 'Built-in Functions'},
            {'file': '/02module/homework_php_create_library_custom_functions.html', 'title': 'Homework: Functions'},
        ],
        7: [  # Working with Forms
            {'file': '/02module/php_html_forms_review.html', 'title': 'HTML Forms Review'},
            {'file': '/02module/php_get_vs_post_methods.html', 'title': 'GET vs POST'},
            {'file': '/02module/php_accessing_form_data_get_post.html', 'title': 'Accessing Form Data'},
            {'file': '/02module/php_form_validation_techniques.html', 'title': 'Form Validation'},
            {'file': '/02module/php_sanitizing_user_input.html', 'title': 'Sanitizing Input'},
            {'file': '/02module/php_file_uploads.html', 'title': 'File Uploads'},
            {'file': '/02module/homework_create_contact_form_validation.html', 'title': 'Homework: Contact Form'},
        ],
        8: [  # Introduction to Object-Oriented PHP
            {'file': '/02module/php_oop_concepts.html', 'title': 'OOP Concepts'},
            {'file': '/02module/php_creating_classes_and instantiating_objects.html', 'title': 'Classes & Objects'},
            {'file': '/02module/php_constructor_and_destructor.html', 'title': 'Constructor & Destructor'},
            {'file': '/02module/php_access_modifiers.html', 'title': 'Access Modifiers'},
            {'file': '/02module/php_this_keyword.html', 'title': 'The $this Keyword'},
            {'file': '/02module/php_static_properties_and_methods.html', 'title': 'Static Properties'},
            {'file': '/02module/homework_php_create_simple_class.html', 'title': 'Homework: Classes'},
        ],
        9: [  # Advanced OOP Concepts
            {'file': '/02module/php_inheritance.html', 'title': 'Inheritance'},
            {'file': '/02module/php_method_overriding.html', 'title': 'Method Overriding'},
            {'file': '/02module/php_abstract_classes.html', 'title': 'Abstract Classes'},
            {'file': '/02module/php_interfaces.html', 'title': 'Interfaces'},
            {'file': '/02module/php_namespaces.html', 'title': 'Namespaces'},
            {'file': '/02module/php_traits.html', 'title': 'Traits'},
            {'file': '/02module/homework_php_extend_with_inheritance.html', 'title': 'Homework: Inheritance'},
        ],
        10: [  # Mini-Project: Dynamic PHP Application
            {'file': '/02module/php_planning_php_application.html', 'title': 'Planning Application'},
            {'file': '/02module/php_implementing_user_input.html', 'title': 'User Input'},
            {'file': '/02module/php_working_with_sessions_cookies.html', 'title': 'Sessions & Cookies'},
            {'file': '/02module/php_creating_reusable_php_components.html', 'title': 'Reusable Components'},
            {'file': '/02module/project_php_dynamic_web_app_with_authentication.html', 'title': 'Project: Dynamic App'},
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
    # Map files to their sessions based on module2.html structure
    file_to_session = {
        # Session 1: PHP Setup and Syntax
        'review_php_setup.html': 1,
        'php_tags_basic_syntax.html': 1,
        'php_output_methods.html': 1,
        'php_comments.html': 1,
        'php_variables_and_data_types.html': 1,
        'php_constants.html': 1,
        'homework_php_script.html': 1,
        
        # Session 2: Operators and Expressions
        'php_arithmetic_operators.html': 2,
        'php_assignment_operators.html': 2,
        'php_comparison_operators.html': 2,
        'php_logical_operators.html': 2,
        'php_string_operators.html': 2,
        'php_array_operators.html': 2,
        'php_type_operators.html': 2,
        'php_operator_precedence.html': 2,
        'homework_php_calculator.html': 2,
        
        # Session 3: Control Structures - Conditionals
        'php_if.html': 3,
        'php_if_else.html': 3,
        'php_if_elseif_else.html': 3,
        'php_switch.html': 3,
        'php_ternary.html': 3,
        'php_null_coalescing.html': 3,
        'homework_php_grades.html': 3,
        
        # Session 4: Control Structures - Loops
        'php_for_loops.html': 4,
        'php_while_loops.html': 4,
        'php_do_while_loops.html': 4,
        'php_foreach_loops_with_arrays.html': 4,
        'php_control_break_continue.html': 4,
        'homework_php_loops.html': 4,
        
        # Session 5: Arrays
        'php_indexed_array.html': 5,
        'php_associative_arrays.html': 5,
        'php_multidimensional_arrays.html': 5,
        'php_array_functions.html': 5,
        'php_array_functions_broke.html': 5,  # Alternative version
        'php_array_sorting.html': 5,
        'php_array_iteration.html': 5,
        'php_array_iteration_2.html': 5,  # Alternative version
        'homework_php_array_creation_manipulation.html': 5,
        
        # Session 6: Functions
        'php_function_declaration_and_calling.html': 6,
        'php_function_parameters_and return_values.html': 6,
        'php_default_parameter_values.html': 6,
        'php_variable_scope.html': 6,
        'php_anonymoous_functions_and_closures.html': 6,
        'php_built_in_php_functions_overview.html': 6,
        'homework_php_create_library_custom_functions.html': 6,
        
        # Session 7: Working with Forms
        'php_html_forms_review.html': 7,
        'php_get_vs_post_methods.html': 7,
        'php_accessing_form_data_get_post.html': 7,
        'php_form_validation_techniques.html': 7,
        'php_sanitizing_user_input.html': 7,
        'php_sanitizing_user_input2.html': 7,  # Alternative version
        'php_file_uploads.html': 7,
        'homework_create_contact_form_validation.html': 7,
        'homework_php_create_contact_form_validation.html': 7,  # Alternative name
        'homework_contact_form.html': 7,
        
        # Session 8: Introduction to Object-Oriented PHP
        'php_oop_concepts.html': 8,
        'intro_to_oop.html': 8,
        'php_creating_classes_and instantiating_objects.html': 8,
        'classes_and_objects.html': 8,
        'php_constructor_and_destructor.html': 8,
        'php_access_modifiers.html': 8,
        'php_this_keyword.html': 8,
        'php_static_properties_and_methods.html': 8,
        'homework_php_create_simple_class.html': 8,
        
        # Session 9: Advanced OOP Concepts
        'php_inheritance.html': 9,
        'inheritance_and_polymorphism.html': 9,
        'php_method_overriding.html': 9,
        'php_abstract_classes.html': 9,
        'php_interfaces.html': 9,
        'interfaces_and_abstract_classes.html': 9,
        'php_namespaces.html': 9,
        'namespaces_autoloading.html': 9,
        'php_traits.html': 9,
        'traits_and_generators.html': 9,
        'homework_php_extend_with_inheritance.html': 9,
        'homework_oop_project.html': 9,
        
        # Session 10: Mini-Project
        'php_planning_php_application.html': 10,
        'project_planning.html': 10,
        'php_implementing_user_input.html': 10,
        'implementing_features.html': 10,
        'php_working_with_sessions_cookies.html': 10,
        'sessions_and_cookies.html': 10,
        'php_creating_reusable_php_components.html': 10,
        'php_creating_reusable_corrected.html': 10,
        'project_php_dynamic_web_app_with_authentication.html': 10,
        'final_project_blog_cms.html': 10,
        
        # Additional files that may belong to various sessions
        'php_fundamentals_review.html': 1,
        'php_setup_ubuntu.html': 1,
        'functions_in_php.html': 6,
        'arrays_and_data_manipulation.html': 5,
        'control_structures_deep_dive.html': 3,
        'handling_form_data.html': 7,
        'form_validation_sanitization.html': 7,
        'input_validation_techniques.html': 7,
        'file_uploads.html': 7,
        'secure_file_handling.html': 7,
        'password_hashing.html': 7,
        'common_vulnerabilities.html': 7,
        'working_with_json.html': 6,
        'consuming_apis.html': 10,
        'creating_api_endpoints.html': 10,
        'api_authentication.html': 10,
        'mvc_architecture.html': 10,
        'database_design.html': 10,
        'intro_to_mysql.html': 10,
        'php_mysql_connection.html': 10,
        'crud_operations.html': 10,
        'prepared_statements.html': 10,
        'error_handling.html': 6,
        'debugging_techniques.html': 6,
        'performance_optimization.html': 10,
        'unit_testing_basics.html': 10,
        'testing_deployment.html': 10,
        'code_quality_tools.html': 10,
        'intro_to_composer.html': 10,
        'laravel_basics.html': 10,
        'symfony_overview.html': 10,
        'regex_in_php.html': 6,
    }
    
    # First lesson of each session - VERIFIED from module2.html
    session_first_lessons = {
        1: {'file': '/02module/review_php_setup.html', 'title': 'Session 1: PHP Setup'},
        2: {'file': '/02module/php_arithmetic_operators.html', 'title': 'Session 2: Operators'},
        3: {'file': '/02module/php_if.html', 'title': 'Session 3: Conditionals'},
        4: {'file': '/02module/php_for_loops.html', 'title': 'Session 4: Loops'},
        5: {'file': '/02module/php_indexed_array.html', 'title': 'Session 5: Arrays'},
        6: {'file': '/02module/php_function_declaration_and_calling.html', 'title': 'Session 6: Functions'},
        7: {'file': '/02module/php_html_forms_review.html', 'title': 'Session 7: Forms'},
        8: {'file': '/02module/php_oop_concepts.html', 'title': 'Session 8: OOP Intro'},
        9: {'file': '/02module/php_inheritance.html', 'title': 'Session 9: Advanced OOP'},
        10: {'file': '/02module/php_planning_php_application.html', 'title': 'Session 10: Project'},
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
    
    # Get previous session link (if not first session)
    if current_session > 1:
        prev_session = current_session - 1
        result['prev'] = session_first_lessons[prev_session]['file']
        result['prev_title'] = session_first_lessons[prev_session]['title']
    else:
        # Link to Module 1 last session
        result['prev'] = '/01module/project_static_site.html'
        result['prev_title'] = 'Module 1: Project'
    
    # Get next session link (if not last session)  
    if current_session < 10:
        next_session = current_session + 1
        result['next'] = session_first_lessons[next_session]['file']
        result['next_title'] = session_first_lessons[next_session]['title']
    elif current_session == 10:
        # Last session links to Module 3 first lesson
        result['next'] = '/03module/intro_to_mysql.html'
        result['next_title'] = 'Module 3: MySQL'
    
    return result

def create_02module_navigation(current_file=None):
    """Create the proper navigation structure for Module 2."""
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
        session_lessons_html = '''                                    <li><a href="/02module/review_php_setup.html" class="sidebar-link">Session 1: PHP Setup</a></li>
                                    <li><a href="/02module/php_arithmetic_operators.html" class="sidebar-link">Session 2: Operators</a></li>
                                    <li><a href="/02module/php_if.html" class="sidebar-link">Session 3: Conditionals</a></li>
                                    <li><a href="/02module/php_for_loops.html" class="sidebar-link">Session 4: Loops</a></li>
                                    <li><a href="/02module/php_indexed_array.html" class="sidebar-link">Session 5: Arrays</a></li>
                                    <li><a href="/02module/php_function_declaration_and_calling.html" class="sidebar-link">Session 6: Functions</a></li>
                                    <li><a href="/02module/php_html_forms_review.html" class="sidebar-link">Session 7: Forms</a></li>
                                    <li><a href="/02module/php_oop_concepts.html" class="sidebar-link">Session 8: OOP Intro</a></li>
                                    <li><a href="/02module/php_inheritance.html" class="sidebar-link">Session 9: Advanced OOP</a></li>
                                    <li><a href="/02module/php_planning_php_application.html" class="sidebar-link">Session 10: Project</a></li>'''
    
    navigation_html = f'''<div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 2: PHP Fundamentals</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">{current_session_num}</h4>
                                <ul class="sidebar-menu">
{session_lessons_html}
                                </ul>
                            </div>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Quick Links</h4>
                                <ul class="sidebar-menu">
                                    <li><a href="/module2.html" class="sidebar-link">Module Overview</a></li>
{prev_session_html}{next_session_html}                                    <li><a href="/module1.html" class="sidebar-link">← Previous Module</a></li>
                                    <li><a href="/module3.html" class="sidebar-link">Next Module →</a></li>
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
        # Session 1
        'review_php_setup.html': 'Review PHP Setup',
        'php_tags_basic_syntax.html': 'PHP Tags & Syntax',
        'php_output_methods.html': 'Output Methods',
        'php_comments.html': 'Comments in PHP',
        'php_variables_and_data_types.html': 'Variables & Data Types',
        'php_constants.html': 'Constants',
        'homework_php_script.html': 'Homework: PHP Script',
        
        # Session 2
        'php_arithmetic_operators.html': 'Arithmetic Operators',
        'php_assignment_operators.html': 'Assignment Operators',
        'php_comparison_operators.html': 'Comparison Operators',
        'php_logical_operators.html': 'Logical Operators',
        'php_string_operators.html': 'String Operators',
        'php_array_operators.html': 'Array Operators',
        'php_type_operators.html': 'Type Operators',
        'php_operator_precedence.html': 'Operator Precedence',
        'homework_php_calculator.html': 'Homework: Calculator',
        
        # Session 3
        'php_if.html': 'If Statements',
        'php_if_else.html': 'If-Else Statements',
        'php_if_elseif_else.html': 'If-Elseif-Else',
        'php_switch.html': 'Switch Statements',
        'php_ternary.html': 'Ternary Operator',
        'php_null_coalescing.html': 'Null Coalescing',
        'homework_php_grades.html': 'Homework: Grades',
        
        # Session 4
        'php_for_loops.html': 'For Loops',
        'php_while_loops.html': 'While Loops',
        'php_do_while_loops.html': 'Do-While Loops',
        'php_foreach_loops_with_arrays.html': 'Foreach Loops',
        'php_control_break_continue.html': 'Break & Continue',
        'homework_php_loops.html': 'Homework: Loops',
        
        # Session 5
        'php_indexed_array.html': 'Indexed Arrays',
        'php_associative_arrays.html': 'Associative Arrays',
        'php_multidimensional_arrays.html': 'Multidimensional Arrays',
        'php_array_functions.html': 'Array Functions',
        'php_array_sorting.html': 'Array Sorting',
        'php_array_iteration.html': 'Array Iteration',
        'homework_php_array_creation_manipulation.html': 'Homework: Arrays',
        
        # Session 6
        'php_function_declaration_and_calling.html': 'Function Declaration',
        'php_function_parameters_and return_values.html': 'Parameters & Returns',
        'php_default_parameter_values.html': 'Default Parameters',
        'php_variable_scope.html': 'Variable Scope',
        'php_anonymoous_functions_and_closures.html': 'Anonymous Functions',
        'php_built_in_php_functions_overview.html': 'Built-in Functions',
        'homework_php_create_library_custom_functions.html': 'Homework: Functions',
        
        # Session 7
        'php_html_forms_review.html': 'HTML Forms Review',
        'php_get_vs_post_methods.html': 'GET vs POST',
        'php_accessing_form_data_get_post.html': 'Accessing Form Data',
        'php_form_validation_techniques.html': 'Form Validation',
        'php_sanitizing_user_input.html': 'Sanitizing Input',
        'php_file_uploads.html': 'File Uploads',
        'homework_create_contact_form_validation.html': 'Homework: Contact Form',
        'homework_php_create_contact_form_validation.html': 'Homework: Contact Form',
        
        # Session 8
        'php_oop_concepts.html': 'OOP Concepts',
        'php_creating_classes_and instantiating_objects.html': 'Classes & Objects',
        'php_constructor_and_destructor.html': 'Constructor & Destructor',
        'php_access_modifiers.html': 'Access Modifiers',
        'php_this_keyword.html': 'The $this Keyword',
        'php_static_properties_and_methods.html': 'Static Properties',
        'homework_php_create_simple_class.html': 'Homework: Classes',
        
        # Session 9
        'php_inheritance.html': 'Inheritance',
        'php_method_overriding.html': 'Method Overriding',
        'php_abstract_classes.html': 'Abstract Classes',
        'php_interfaces.html': 'Interfaces',
        'php_namespaces.html': 'Namespaces',
        'php_traits.html': 'Traits',
        'homework_php_extend_with_inheritance.html': 'Homework: Inheritance',
        
        # Session 10
        'php_planning_php_application.html': 'Planning Application',
        'php_implementing_user_input.html': 'User Input',
        'php_working_with_sessions_cookies.html': 'Sessions & Cookies',
        'php_creating_reusable_php_components.html': 'Reusable Components',
        'php_creating_reusable_corrected.html': 'Reusable Components',
        'project_php_dynamic_web_app_with_authentication.html': 'Project: Dynamic App',
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
    """Main function to fix navigation in all 02module files."""
    
    # Define paths
    if os.path.exists(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module"):
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
        print(f"Using Windows WSL path: {base_path}")
    elif os.path.exists("/home/practicalace/projects/php_wordpress/02module"):
        base_path = "/home/practicalace/projects/php_wordpress"
        print(f"Using Linux path: {base_path}")
    else:
        base_path = os.getcwd()
        print(f"Using current directory: {base_path}")
        
    module02_dir = os.path.join(base_path, "02module")
    
    print(f"\nLooking for Module 2 files in: {module02_dir}")
    print(f"Directory exists: {os.path.exists(module02_dir)}")
    
    print("=" * 60)
    print("Module 2: PHP Fundamentals - Navigation Fixer")
    print("=" * 60)
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nDo you want to proceed with fixing the navigation? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Process all Module 2 HTML files
    print("\n" + "=" * 60)
    print("\nUpdating Module 2 files...")
    print("=" * 60 + "\n")
    
    files = get_module_files(str(module02_dir))
    
    if not files:
        print(f"No HTML files found in {module02_dir}")
        return
    
    success_count = 0
    fail_count = 0
    
    for filepath in files:
        # Get the current page for this file
        current_page = get_current_page_from_file(filepath)
        
        # Create navigation with active state AND next session link for this specific file
        nav_template = create_02module_navigation(filepath)
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
    print("\n✅ Module 2 navigation fix complete!")

if __name__ == "__main__":
    main()
