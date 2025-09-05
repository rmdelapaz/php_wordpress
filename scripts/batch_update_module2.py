#!/usr/bin/env python3
"""
Batch update script for Module 2: PHP Fundamentals
Updates ALL Module 2 HTML files with the new template structure
Includes all 122 files found in the 02module directory
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Base directory - Linux path
BASE_DIR = Path("/home/practicalace/projects/php_wordpress/02module")

# Check if directory exists
if not BASE_DIR.exists():
    print(f"❌ Error: Directory {BASE_DIR} does not exist!")
    print(f"Current working directory: {os.getcwd()}")
    print("\nTrying alternative paths...")
    
    # Try alternative paths
    alt_paths = [
        Path.cwd() / "02module",
        Path.home() / "projects/php_wordpress/02module",
        Path("/mnt/c/Users") / os.environ.get('USER', '') / "projects/php_wordpress/02module"
    ]
    
    for alt_path in alt_paths:
        if alt_path.exists():
            BASE_DIR = alt_path
            print(f"✅ Found directory at: {BASE_DIR}")
            break
    else:
        print("❌ Could not find the 02module directory. Please update BASE_DIR in the script.")
        exit(1)

# Files that have already been updated (will be skipped)
ALREADY_UPDATED = []  # Add filenames here as they get manually updated

def check_if_updated(filepath):
    """
    Check if a file has already been updated with the new template
    by looking for specific markers in the file content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # Read first 1000 chars
            
            # Check for new template markers
            markers = [
                'class="site-header"',
                'class="lesson-objectives"',
                'class="lesson-navigation"',
                'PHP WordPress Course',
                'class="sidebar-nav"'
            ]
            
            # If 3 or more markers are found, file is likely updated
            found_markers = sum(1 for marker in markers if marker in content)
            return found_markers >= 3
            
    except Exception as e:
        print(f"    ⚠️ Could not check file: {e}")
        return False

# Complete Module 2 structure - ALL 122 files organized by topic
module2_files = {
    "php_basics": {
        "title": "PHP Basics & Setup",
        "files": [
            ("review_php_setup.html", "Review PHP Setup", "30 minutes",
             "Review PHP installation and setup on different platforms."),
            ("php_setup_ubuntu.html", "PHP Setup on Ubuntu", "45 minutes",
             "Install and configure PHP on Ubuntu Linux systems."),
            ("php_tags_basic_syntax.html", "PHP Tags and Basic Syntax", "30 minutes",
             "Learn PHP opening and closing tags, and basic syntax rules."),
            ("php_comments.html", "PHP Comments", "20 minutes",
             "Master single-line and multi-line comments in PHP."),
            ("php_output_methods.html", "PHP Output Methods", "30 minutes",
             "Learn echo, print, and other output methods in PHP."),
            ("php_fundamentals_review.html", "PHP Fundamentals Review", "45 minutes",
             "Comprehensive review of PHP fundamentals.")
        ]
    },
    "variables_data_types": {
        "title": "Variables & Data Types",
        "files": [
            ("php_variables_and_data_types.html", "PHP Variables and Data Types", "45 minutes",
             "Understanding PHP variables, data types, and type juggling."),
            ("php_constants.html", "PHP Constants", "30 minutes",
             "Define and use constants in PHP applications."),
            ("php_variable_scope.html", "PHP Variable Scope", "45 minutes",
             "Master local, global, and static variable scope in PHP."),
            ("php_type_operators.html", "PHP Type Operators", "30 minutes",
             "Work with type operators and type checking in PHP.")
        ]
    },
    "operators": {
        "title": "PHP Operators",
        "files": [
            ("php_arithmetic_operators.html", "PHP Arithmetic Operators", "30 minutes",
             "Master addition, subtraction, multiplication, division, and modulus operators."),
            ("php_assignment_operators.html", "PHP Assignment Operators", "30 minutes",
             "Learn assignment operators including compound assignments."),
            ("php_comparison_operators.html", "PHP Comparison Operators", "30 minutes",
             "Use comparison operators for conditional logic."),
            ("php_logical_operators.html", "PHP Logical Operators", "30 minutes",
             "Implement AND, OR, NOT, and XOR logical operations."),
            ("php_string_operators.html", "PHP String Operators", "20 minutes",
             "Concatenate and manipulate strings with operators."),
            ("php_array_operators.html", "PHP Array Operators", "30 minutes",
             "Use array operators for union and comparison."),
            ("php_operator_precedence.html", "PHP Operator Precedence", "30 minutes",
             "Understand operator precedence and evaluation order."),
            ("php_ternary.html", "PHP Ternary Operator", "30 minutes",
             "Master the ternary conditional operator."),
            ("php_null_coalescing.html", "PHP Null Coalescing Operator", "30 minutes",
             "Use the null coalescing operator for default values.")
        ]
    },
    "control_structures": {
        "title": "Control Structures",
        "files": [
            ("control_structures_deep_dive.html", "Control Structures Deep Dive", "60 minutes",
             "Comprehensive exploration of PHP control structures."),
            ("php_if.html", "PHP If Statement", "30 minutes",
             "Master the basic if conditional statement."),
            ("php_if_else.html", "PHP If-Else Statement", "30 minutes",
             "Implement if-else conditional logic."),
            ("php_if_elseif_else.html", "PHP If-ElseIf-Else", "30 minutes",
             "Handle multiple conditions with elseif."),
            ("php_switch.html", "PHP Switch Statement", "30 minutes",
             "Use switch statements for multiple conditions."),
            ("php_control_break_continue.html", "PHP Break and Continue", "30 minutes",
             "Control loop execution with break and continue.")
        ]
    },
    "loops": {
        "title": "Loops in PHP",
        "files": [
            ("php_for_loops.html", "PHP For Loops", "30 minutes",
             "Master for loops for iterative operations."),
            ("php_while_loops.html", "PHP While Loops", "30 minutes",
             "Implement while loops for conditional iteration."),
            ("php_do_while_loops.html", "PHP Do-While Loops", "30 minutes",
             "Use do-while loops for guaranteed execution."),
            ("php_foreach_loops_with_arrays.html", "PHP Foreach Loops", "45 minutes",
             "Iterate through arrays with foreach loops."),
            ("homework_php_loops.html", "Homework: PHP Loops", "60 minutes",
             "Practice exercises for mastering PHP loops.")
        ]
    },
    "functions": {
        "title": "Functions in PHP",
        "files": [
            ("functions_in_php.html", "Functions in PHP", "45 minutes",
             "Introduction to creating and using functions."),
            ("php_function_declaration_and_calling.html", "Function Declaration and Calling", "45 minutes",
             "Declare and call functions in PHP."),
            ("php_function_parameters_and return_values.html", "Function Parameters and Return Values", "45 minutes",
             "Work with function parameters and return values."),
            ("php_default_parameter_values.html", "Default Parameter Values", "30 minutes",
             "Set default values for function parameters."),
            ("php_anonymoous_functions_and_closures.html", "Anonymous Functions and Closures", "45 minutes",
             "Master anonymous functions and closures."),
            ("php_built_in_php_functions_overview.html", "Built-in PHP Functions", "45 minutes",
             "Overview of PHP's built-in function library."),
            ("php_creating_reusable_php_components.html", "Creating Reusable Components", "45 minutes",
             "Build reusable PHP components and libraries."),
            ("php_creating_reusable_corrected.html", "Creating Reusable Components (Corrected)", "45 minutes",
             "Updated guide for creating reusable PHP components."),
            ("homework_php_create_library_custom_functions.html", "Homework: Create Function Library", "90 minutes",
             "Build a library of custom PHP functions.")
        ]
    },
    "arrays": {
        "title": "Arrays and Data Manipulation",
        "files": [
            ("arrays_and_data_manipulation.html", "Arrays and Data Manipulation", "60 minutes",
             "Comprehensive guide to PHP arrays."),
            ("php_indexed_array.html", "PHP Indexed Arrays", "30 minutes",
             "Work with numerically indexed arrays."),
            ("php_associative_arrays.html", "PHP Associative Arrays", "30 minutes",
             "Master key-value pair associative arrays."),
            ("php_multidimensional_arrays.html", "PHP Multidimensional Arrays", "45 minutes",
             "Handle complex multidimensional array structures."),
            ("php_array_functions.html", "PHP Array Functions", "45 minutes",
             "Use built-in array manipulation functions."),
            ("php_array_functions_broke.html", "PHP Array Functions (Fixed)", "45 minutes",
             "Corrected array function examples and usage."),
            ("php_array_iteration.html", "PHP Array Iteration", "30 minutes",
             "Iterate through arrays with various methods."),
            ("php_array_iteration_2.html", "PHP Array Iteration Advanced", "30 minutes",
             "Advanced array iteration techniques."),
            ("php_array_sorting.html", "PHP Array Sorting", "30 minutes",
             "Sort arrays with various sorting functions."),
            ("homework_php_array_creation_manipulation.html", "Homework: Array Manipulation", "60 minutes",
             "Practice array creation and manipulation.")
        ]
    },
    "forms": {
        "title": "Working with Forms",
        "files": [
            ("php_html_forms_review.html", "HTML Forms Review", "30 minutes",
             "Review HTML form structure for PHP processing."),
            ("handling_form_data.html", "Handling Form Data in PHP", "45 minutes",
             "Process form submissions with PHP."),
            ("php_get_vs_post_methods.html", "GET vs POST Methods", "30 minutes",
             "Understand the differences between GET and POST."),
            ("php_accessing_form_data_get_post.html", "Accessing Form Data", "45 minutes",
             "Access and process GET and POST data."),
            ("form_validation_sanitization.html", "Form Validation and Sanitization", "60 minutes",
             "Validate and sanitize form input data."),
            ("php_form_validation_techniques.html", "Form Validation Techniques", "45 minutes",
             "Advanced form validation strategies."),
            ("php_sanitizing_user_input.html", "Sanitizing User Input", "45 minutes",
             "Secure user input sanitization methods."),
            ("php_sanitizing_user_input2.html", "Advanced Input Sanitization", "45 minutes",
             "Advanced techniques for input sanitization."),
            ("php_implementing_user_input.html", "Implementing User Input", "45 minutes",
             "Safely implement user input in applications."),
            ("file_uploads.html", "File Uploads in PHP", "45 minutes",
             "Handle file uploads securely."),
            ("php_file_uploads.html", "PHP File Upload Implementation", "45 minutes",
             "Complete guide to implementing file uploads."),
            ("homework_contact_form.html", "Homework: Contact Form", "90 minutes",
             "Build a complete contact form with validation."),
            ("homework_php_create_contact_form_validation.html", "Homework: Form Validation", "90 minutes",
             "Create a contact form with comprehensive validation.")
        ]
    },
    "sessions_cookies": {
        "title": "Sessions and Cookies",
        "files": [
            ("sessions_and_cookies.html", "Sessions and Cookies", "60 minutes",
             "Understanding PHP sessions and cookies."),
            ("php_working_with_sessions_cookies.html", "Working with Sessions and Cookies", "60 minutes",
             "Implement session and cookie functionality.")
        ]
    },
    "oop": {
        "title": "Object-Oriented PHP",
        "files": [
            ("intro_to_oop.html", "Introduction to OOP", "60 minutes",
             "Object-oriented programming concepts in PHP."),
            ("php_oop_concepts.html", "PHP OOP Concepts", "45 minutes",
             "Core OOP concepts and principles."),
            ("classes_and_objects.html", "Classes and Objects", "60 minutes",
             "Creating and using classes and objects."),
            ("php_creating_classes_and instantiating_objects.html", "Creating Classes", "45 minutes",
             "Create classes and instantiate objects."),
            ("php_constructor_and_destructor.html", "Constructors and Destructors", "45 minutes",
             "Use constructors and destructors in classes."),
            ("php_access_modifiers.html", "Access Modifiers", "30 minutes",
             "Public, private, and protected access modifiers."),
            ("php_this_keyword.html", "The $this Keyword", "30 minutes",
             "Understanding and using the $this keyword."),
            ("php_static_properties_and_methods.html", "Static Properties and Methods", "45 minutes",
             "Work with static class members."),
            ("inheritance_and_polymorphism.html", "Inheritance and Polymorphism", "45 minutes",
             "Implement inheritance and polymorphism."),
            ("php_inheritance.html", "PHP Inheritance", "45 minutes",
             "Master class inheritance in PHP."),
            ("php_method_overriding.html", "Method Overriding", "30 minutes",
             "Override parent class methods."),
            ("interfaces_and_abstract_classes.html", "Interfaces and Abstract Classes", "45 minutes",
             "Use interfaces and abstract classes."),
            ("php_interfaces.html", "PHP Interfaces", "45 minutes",
             "Define and implement interfaces."),
            ("php_abstract_classes.html", "PHP Abstract Classes", "45 minutes",
             "Create and extend abstract classes."),
            ("php_traits.html", "PHP Traits", "45 minutes",
             "Use traits for code reuse."),
            ("php_namespaces.html", "PHP Namespaces", "45 minutes",
             "Organize code with namespaces."),
            ("homework_php_create_simple_class.html", "Homework: Create Simple Class", "60 minutes",
             "Build your first PHP class."),
            ("homework_php_extend_with_inheritance.html", "Homework: Inheritance", "60 minutes",
             "Practice inheritance with PHP classes."),
            ("homework_oop_project.html", "Homework: OOP Project", "120 minutes",
             "Complete OOP project implementation.")
        ]
    },
    "database": {
        "title": "Database Operations",
        "files": [
            ("intro_to_mysql.html", "Introduction to MySQL", "45 minutes",
             "MySQL database fundamentals."),
            ("php_mysql_connection.html", "PHP MySQL Connection", "45 minutes",
             "Connect PHP to MySQL databases."),
            ("crud_operations.html", "CRUD Operations", "90 minutes",
             "Create, Read, Update, Delete operations."),
            ("prepared_statements.html", "Prepared Statements", "60 minutes",
             "Secure database queries with prepared statements."),
            ("database_design.html", "Database Design", "60 minutes",
             "Design efficient database schemas."),
            ("homework_user_management.html", "Homework: User Management", "120 minutes",
             "Build a user management system.")
        ]
    },
    "apis": {
        "title": "APIs and Web Services",
        "files": [
            ("working_with_json.html", "Working with JSON", "45 minutes",
             "Parse and generate JSON data in PHP."),
            ("consuming_apis.html", "Consuming APIs", "60 minutes",
             "Consume external REST APIs."),
            ("creating_api_endpoints.html", "Creating API Endpoints", "60 minutes",
             "Build RESTful API endpoints."),
            ("api_authentication.html", "API Authentication", "45 minutes",
             "Implement API authentication."),
            ("homework_weather_app.html", "Homework: Weather App", "90 minutes",
             "Build a weather app using APIs.")
        ]
    },
    "security": {
        "title": "PHP Security",
        "files": [
            ("common_vulnerabilities.html", "Common Vulnerabilities", "60 minutes",
             "Understand common PHP security issues."),
            ("input_validation_techniques.html", "Input Validation Techniques", "45 minutes",
             "Comprehensive input validation strategies."),
            ("password_hashing.html", "Password Hashing", "45 minutes",
             "Secure password storage techniques."),
            ("secure_file_handling.html", "Secure File Handling", "45 minutes",
             "Handle files securely in PHP."),
            ("homework_secure_app.html", "Homework: Secure Application", "90 minutes",
             "Implement security best practices.")
        ]
    },
    "frameworks": {
        "title": "PHP Frameworks",
        "files": [
            ("mvc_architecture.html", "MVC Architecture", "60 minutes",
             "Model-View-Controller design pattern."),
            ("intro_to_composer.html", "Introduction to Composer", "45 minutes",
             "PHP dependency management with Composer."),
            ("laravel_basics.html", "Laravel Basics", "90 minutes",
             "Getting started with Laravel framework."),
            ("symfony_overview.html", "Symfony Overview", "60 minutes",
             "Introduction to Symfony framework."),
            ("homework_framework_project.html", "Homework: Framework Project", "120 minutes",
             "Build a project using a PHP framework.")
        ]
    },
    "testing_debugging": {
        "title": "Testing and Debugging",
        "files": [
            ("debugging_techniques.html", "Debugging Techniques", "45 minutes",
             "Master PHP debugging strategies."),
            ("error_handling.html", "Error Handling", "45 minutes",
             "Implement proper error handling."),
            ("unit_testing_basics.html", "Unit Testing Basics", "60 minutes",
             "Write unit tests for PHP code."),
            ("code_quality_tools.html", "Code Quality Tools", "45 minutes",
             "Use tools for code quality assurance."),
            ("homework_add_tests.html", "Homework: Add Tests", "90 minutes",
             "Add tests to existing code.")
        ]
    },
    "advanced": {
        "title": "Advanced PHP Topics",
        "files": [
            ("namespaces_autoloading.html", "Namespaces and Autoloading", "45 minutes",
             "Advanced namespace and autoloading."),
            ("traits_and_generators.html", "Traits and Generators", "45 minutes",
             "Use traits and generators effectively."),
            ("regex_in_php.html", "Regular Expressions in PHP", "60 minutes",
             "Master regex pattern matching."),
            ("performance_optimization.html", "Performance Optimization", "60 minutes",
             "Optimize PHP application performance."),
            ("homework_optimization.html", "Homework: Optimization", "90 minutes",
             "Optimize application performance.")
        ]
    },
    "projects": {
        "title": "PHP Projects",
        "files": [
            ("php_planning_php_application.html", "Planning PHP Applications", "45 minutes",
             "Plan and architect PHP applications."),
            ("project_planning.html", "Project Planning", "60 minutes",
             "Comprehensive project planning."),
            ("implementing_features.html", "Implementing Features", "120 minutes",
             "Build core application features."),
            ("testing_deployment.html", "Testing and Deployment", "60 minutes",
             "Test and deploy PHP applications."),
            ("homework_php_calculator.html", "Homework: PHP Calculator", "90 minutes",
             "Build a functional calculator."),
            ("homework_php_grades.html", "Homework: Grade Calculator", "60 minutes",
             "Create a grade calculation system."),
            ("homework_php_script.html", "Homework: PHP Script", "60 minutes",
             "Write a complete PHP script."),
            ("project_php_dynamic_web_app_with_authentication.html", "Project: Dynamic Web App", "180 minutes",
             "Build a dynamic web app with authentication."),
            ("final_project_blog_cms.html", "Final Project: Blog CMS", "240 minutes",
             "Complete blog content management system.")
        ]
    }
}

def get_all_files_from_structure():
    """Get all files from the module structure"""
    all_files = []
    for session_data in module2_files.values():
        for file_info in session_data["files"]:
            all_files.append(file_info[0])
    return all_files

def generate_html(session_key, session_data, file_index, file_info, module_num="2"):
    """Generate complete HTML for a lesson file with proper navigation"""
    
    filename, title, duration, description = file_info
    session_title = session_data["title"]
    
    # Generate components
    sidebar_html = generate_sidebar(session_title, session_data["files"], file_index, module_num)
    nav_html = generate_navigation_simple(title, module_num)  # Simplified navigation
    objectives = generate_objectives(title)
    content = generate_content(title, description)
    homework = generate_homework(title)
    
    # Complete HTML template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>{title} - PHP WordPress Course</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="PHP, WordPress, web development, {title.lower().replace(' ', ', ')}">
    <meta name="author" content="PHP WordPress Course">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
    <!-- Skip to main content -->
    <a href="#main-content" class="sr-only">Skip to main content</a>
    
    <div class="page-wrapper">
        {generate_header(module_num)}
        {generate_progress_bar()}
        {generate_breadcrumb(title, module_num)}
        
        <!-- Main Content -->
        <main id="main-content" class="main-content" role="main">
            <div class="container">
                <div class="content-with-sidebar">
                    {sidebar_html}
                    
                    <!-- Main Lesson Content -->
                    <article class="lesson-content">
                        <header class="lesson-header">
                            <h1>{title}</h1>
                            <div class="lesson-meta">
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <span>Duration: {duration}</span>
                                </div>
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 14l9-5-9-5-9 5 9 5z"/>
                                    </svg>
                                    <span>Module {module_num}: {session_title}</span>
                                </div>
                            </div>
                        </header>

                        {objectives}
                        
                        <!-- Lesson Body -->
                        <div class="lesson-body">
                            {content}
                            
                            {homework}
                            
                            {generate_resources(title)}
                        </div>

                        {nav_html}
                    </article>
                </div>
            </div>
        </main>

        {generate_footer()}
    </div>

    <!-- Back to Top -->
    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 19V5M12 5l-7 7M12 5l7 7"/>
        </svg>
    </button>

    <!-- JavaScript -->
    <script src="/assets/js/navigation.js"></script>
    <script src="/assets/js/site-config.js"></script>
</body>
</html>"""
    
    return html

def generate_navigation_simple(title, module_num="2"):
    """Generate simplified lesson navigation"""
    nav_html = f"""                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">
                            <a href="/module{module_num}.html" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Back to</small><br>
                                    Module {module_num} Overview
                                </span>
                            </a>
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>
                            
                            <a href="/module3.html" class="lesson-nav-button next">
                                <span>
                                    <small>Next Module</small><br>
                                    Module 3: MySQL Database
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>
                        </div>"""
    
    return nav_html

def generate_header(module_num="2"):
    """Generate standard header HTML with Module 2 active"""
    return f"""        <!-- Header -->
        <header class="site-header" role="banner">
            <div class="header-container">
                <div class="site-branding">
                    <a href="/" class="site-logo">
                        <h1 class="site-title">PHP WordPress Development</h1>
                    </a>
                </div>
                
                <nav class="main-navigation" role="navigation" aria-label="Main navigation">
                    <button class="mobile-menu-btn" aria-label="Toggle navigation" aria-expanded="false">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                    
                    <div class="nav-menu">
                        <ul class="nav-list">
                            <li class="nav-item"><a href="/" class="nav-link">Home</a></li>
                            <li class="nav-item dropdown">
                                <button class="nav-link dropdown-toggle active" aria-haspopup="true">Modules</button>
                                <div class="dropdown-menu">
                                    <a href="/module1.html" class="dropdown-item">Module 1: Web Fundamentals</a>
                                    <a href="/module2.html" class="dropdown-item active">Module 2: PHP Fundamentals</a>
                                    <a href="/module3.html" class="dropdown-item">Module 3: MySQL Database</a>
                                    <a href="/module4.html" class="dropdown-item">Module 4: WordPress & Docker</a>
                                    <a href="/module5.html" class="dropdown-item">Module 5: Theme Development</a>
                                    <a href="/module6.html" class="dropdown-item">Module 6: Plugin Development</a>
                                    <a href="/module7.html" class="dropdown-item">Module 7: Advanced WordPress</a>
                                    <a href="/module8.html" class="dropdown-item">Module 8: Deployment</a>
                                    <a href="/module9.html" class="dropdown-item">Module 9: Final Project</a>
                                </div>
                            </li>
                            <li class="nav-item"><a href="/resources.html" class="nav-link">Resources</a></li>
                            <li class="nav-item"><a href="/about.html" class="nav-link">About</a></li>
                        </ul>
                    </div>
                </nav>
                
                <div class="search-container">
                    <div class="search-input-wrapper">
                        <svg class="search-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                        </svg>
                        <input type="search" class="search-input" placeholder="Search lessons..." aria-label="Search">
                    </div>
                    <div class="search-results"></div>
                </div>
            </div>
        </header>"""

def generate_progress_bar():
    """Generate progress bar HTML"""
    return """        <!-- Progress Bar -->
        <div class="progress-container">
            <div class="progress-header">
                <h2 class="progress-title">Course Progress</h2>
                <span class="progress-text">Loading...</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-fill">
                    <span class="progress-bar-text"></span>
                </div>
            </div>
        </div>"""

def generate_breadcrumb(title, module_num="2"):
    """Generate breadcrumb HTML"""
    return f"""        <!-- Breadcrumb -->
        <nav class="breadcrumb container" aria-label="Breadcrumb">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <a href="/module{module_num}.html">Module {module_num}</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <span aria-current="page">{title}</span>
                </li>
            </ol>
        </nav>"""

def generate_sidebar(session_title, files, current_index, module_num="2"):
    """Generate sidebar HTML"""
    sidebar = f"""                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module {module_num}: {session_title}</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Lessons</h4>"""
    
    for i, file_info in enumerate(files):
        filename, title, _, _ = file_info
        active = " active" if i == current_index else ""
        sidebar += f"""
                                <a href="/0{module_num}module/{filename}" class="sidebar-link{active}">{title}</a>"""
    
    sidebar += """
                            </div>
                        </div>
                    </aside>"""
    
    return sidebar

def generate_objectives(title):
    """Generate learning objectives based on title"""
    objectives = """                        <!-- Learning Objectives -->
                        <div class="lesson-objectives">
                            <h2>Learning Objectives</h2>
                            <ul>"""
    
    title_lower = title.lower()
    
    # PHP-specific objectives based on keywords
    if "setup" in title_lower:
        objectives += """
                                <li>Set up PHP development environment</li>
                                <li>Configure PHP for optimal development</li>
                                <li>Understand PHP installation options</li>
                                <li>Test PHP installation and configuration</li>"""
    elif any(word in title_lower for word in ["variable", "data type", "constant"]):
        objectives += """
                                <li>Understand PHP variables and constants</li>
                                <li>Master PHP data types</li>
                                <li>Learn variable scope and lifetime</li>
                                <li>Apply best practices for naming and usage</li>"""
    elif "operator" in title_lower:
        objectives += """
                                <li>Master PHP operators</li>
                                <li>Understand operator precedence</li>
                                <li>Apply operators in practical scenarios</li>
                                <li>Write efficient expressions</li>"""
    elif any(word in title_lower for word in ["loop", "for", "while", "foreach"]):
        objectives += """
                                <li>Master PHP loop structures</li>
                                <li>Choose appropriate loop types</li>
                                <li>Control loop execution flow</li>
                                <li>Optimize loop performance</li>"""
    elif "function" in title_lower:
        objectives += """
                                <li>Create and use PHP functions</li>
                                <li>Understand function parameters and returns</li>
                                <li>Master variable scope in functions</li>
                                <li>Build reusable code components</li>"""
    elif "array" in title_lower:
        objectives += """
                                <li>Master PHP array operations</li>
                                <li>Work with different array types</li>
                                <li>Use array functions effectively</li>
                                <li>Manipulate complex data structures</li>"""
    elif "form" in title_lower:
        objectives += """
                                <li>Process HTML forms with PHP</li>
                                <li>Validate and sanitize form data</li>
                                <li>Handle file uploads securely</li>
                                <li>Implement form security best practices</li>"""
    elif any(word in title_lower for word in ["oop", "object", "class"]):
        objectives += """
                                <li>Understand OOP principles in PHP</li>
                                <li>Create and use classes and objects</li>
                                <li>Implement inheritance and polymorphism</li>
                                <li>Apply OOP best practices</li>"""
    elif any(word in title_lower for word in ["database", "mysql", "crud"]):
        objectives += """
                                <li>Connect PHP to databases</li>
                                <li>Execute database queries from PHP</li>
                                <li>Implement CRUD operations</li>
                                <li>Secure database operations</li>"""
    elif "api" in title_lower:
        objectives += """
                                <li>Work with APIs in PHP</li>
                                <li>Parse and generate JSON data</li>
                                <li>Consume external web services</li>
                                <li>Create RESTful endpoints</li>"""
    elif "security" in title_lower:
        objectives += """
                                <li>Identify security vulnerabilities</li>
                                <li>Implement secure coding practices</li>
                                <li>Protect against common attacks</li>
                                <li>Validate and sanitize all input</li>"""
    else:
        objectives += """
                                <li>Master PHP programming concepts</li>
                                <li>Write clean, maintainable code</li>
                                <li>Apply best practices</li>
                                <li>Build dynamic applications</li>"""
    
    objectives += """
                            </ul>
                        </div>"""
    
    return objectives

def generate_content(title, description):
    """Generate lesson content based on title"""
    content = f"""                            <section>
                                <h2>Introduction</h2>
                                <p class="lead">{description}</p>
                                
                                <div class="alert alert-info">
                                    <div class="alert-icon">💡</div>
                                    <div class="alert-content">
                                        <div class="alert-title">Key Concept</div>
                                        <div class="alert-message">PHP is the foundation of WordPress. Every concept you learn here will directly apply to WordPress development.</div>
                                    </div>
                                </div>
                            </section>

                            <section>
                                <h2>Core Concepts</h2>
                                <p>This lesson covers essential PHP concepts for WordPress development.</p>
                                
                                <pre><code class="language-php">&lt;?php
// Example PHP code
// Tailored to the specific lesson topic
?&gt;</code></pre>
                                
                                <div class="best_practice">
                                    <h3>Best Practices</h3>
                                    <ul>
                                        <li>Follow PSR coding standards</li>
                                        <li>Always validate user input</li>
                                        <li>Use prepared statements for databases</li>
                                        <li>Implement proper error handling</li>
                                        <li>Keep security as top priority</li>
                                    </ul>
                                </div>
                            </section>

                            <section>
                                <h2>Practical Examples</h2>
                                <p>Real-world examples to reinforce your learning.</p>
                                
                                <div class="example-code">
                                    <h3>Example Implementation</h3>
                                    <pre><code class="language-php">&lt;?php
// Practical example
// Specific to lesson content
?&gt;</code></pre>
                                </div>
                            </section>

                            <section>
                                <h2>WordPress Application</h2>
                                <div class="real_world_example">
                                    <h3>How This Applies to WordPress</h3>
                                    <p>This PHP concept is essential for WordPress because:</p>
                                    <ul>
                                        <li>WordPress core uses these patterns</li>
                                        <li>Themes require this knowledge</li>
                                        <li>Plugins implement these concepts</li>
                                        <li>Custom functionality depends on it</li>
                                    </ul>
                                </div>
                            </section>

                            <section>
                                <h2>Practice Exercise</h2>
                                <p>Apply what you've learned with hands-on practice.</p>
                                
                                <div class="alert alert-success">
                                    <div class="alert-icon">💻</div>
                                    <div class="alert-content">
                                        <div class="alert-title">Try It Now</div>
                                        <div class="alert-message">Open your PHP environment and practice these concepts!</div>
                                    </div>
                                </div>
                            </section>"""
    
    return content

def generate_homework(title):
    """Generate homework section based on title"""
    if "homework" in title.lower() or "project" in title.lower():
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Assignment Requirements</h2>
                                <p>Complete this project to demonstrate mastery of the concepts:</p>
                                <ol>
                                    <li>Plan your implementation approach</li>
                                    <li>Write clean, well-commented code</li>
                                    <li>Test thoroughly with various inputs</li>
                                    <li>Follow PHP best practices</li>
                                    <li>Document your solution</li>
                                </ol>
                                
                                <h3>Submission Guidelines</h3>
                                <ul>
                                    <li>Upload to GitHub with README</li>
                                    <li>Include setup instructions</li>
                                    <li>Add code comments</li>
                                    <li>Test before submission</li>
                                </ul>
                                
                                <p><strong>Due:</strong> Before next session</p>
                            </div>"""
    else:
        return """                            <!-- Practice -->
                            <div class="homework">
                                <h2>Practice Exercises</h2>
                                <p>Reinforce your learning with these exercises:</p>
                                <ul>
                                    <li>Review lesson code examples</li>
                                    <li>Complete practice problems</li>
                                    <li>Experiment with variations</li>
                                    <li>Research related PHP functions</li>
                                </ul>
                                
                                <p><strong>Challenge:</strong> Build a small project using these concepts.</p>
                            </div>"""

def generate_resources(title):
    """Generate resources section"""
    return """                            <!-- Resources -->
                            <section class="resources">
                                <h2>Additional Resources</h2>
                                <ul>
                                    <li><a href="https://www.php.net/manual/en/" target="_blank">PHP Official Documentation</a></li>
                                    <li><a href="https://phptherightway.com/" target="_blank">PHP: The Right Way</a></li>
                                    <li><a href="https://www.w3schools.com/php/" target="_blank">W3Schools PHP Tutorial</a></li>
                                    <li><a href="https://developer.wordpress.org/apis/" target="_blank">WordPress Developer Resources</a></li>
                                    <li><a href="https://www.phptutorial.net/" target="_blank">PHP Tutorial</a></li>
                                </ul>
                            </section>"""

def generate_footer():
    """Generate footer HTML"""
    return """        <!-- Footer -->
        <footer class="site-footer" role="contentinfo">
            <div class="footer-container">
                <div class="footer-content">
                    <div class="footer-section footer-about">
                        <h3>PHP WordPress Development</h3>
                        <p>Complete Web Development Course</p>
                    </div>
                    
                    <div class="footer-section">
                        <h4>Quick Links</h4>
                        <ul class="footer-links">
                            <li><a href="/">Home</a></li>
                            <li><a href="/module2.html">Module 2</a></li>
                            <li><a href="/resources.html">Resources</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-section">
                        <h4>Support</h4>
                        <ul class="footer-links">
                            <li><a href="/help.html">Help Center</a></li>
                            <li><a href="/faq.html">FAQ</a></li>
                            <li><a href="/contact.html">Contact</a></li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <div class="footer-bottom-content">
                        <p class="copyright">&copy; 2025 PHP WordPress Development Course</p>
                        <nav class="footer-bottom-links">
                            <a href="/privacy.html">Privacy</a>
                            <span class="separator">|</span>
                            <a href="/terms.html">Terms</a>
                        </nav>
                    </div>
                </div>
            </div>
        </footer>"""

# Main execution
def main():
    """Main function to update all Module 2 files"""
    
    print(f"🚀 PHP WordPress Course - Module 2 Complete Update Script")
    print("="*60)
    print(f"📁 Working directory: {BASE_DIR}")
    print(f"✅ Directory exists: {BASE_DIR.exists()}")
    print(f"📅 Update started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get all existing files in directory
    existing_files = list(BASE_DIR.glob("*.html"))
    existing_filenames = [f.name for f in existing_files]
    print(f"📊 Found {len(existing_files)} existing HTML files in directory")
    
    # Get all files from our structure
    structured_files = get_all_files_from_structure()
    print(f"📋 Structure contains {len(structured_files)} defined files")
    
    # Find files in directory but not in structure
    unstructured_files = [f for f in existing_filenames if f not in structured_files]
    print(f"🔍 Found {len(unstructured_files)} files not in structure definition\n")
    
    updated_files = []
    created_files = []
    failed_files = []
    skipped_files = []
    already_updated_files = []
    
    # Process structured files
    processed = 0
    total_files = len(structured_files) + len(unstructured_files)
    
    print("📝 Processing structured files...")
    for session_key, session_data in module2_files.items():
        print(f"\n📁 {session_data['title']}...")
        
        for file_index, file_info in enumerate(session_data["files"]):
            filename = file_info[0]
            filepath = BASE_DIR / filename
            processed += 1
            
            # Check if already updated
            if filename in ALREADY_UPDATED:
                already_updated_files.append(filename)
                print(f"  ⏭️  Skipped (manual): {filename}")
                continue
            
            if filepath.exists() and check_if_updated(filepath):
                skipped_files.append(filename)
                print(f"  ⏭️  Skipped (updated): {filename}")
                continue
            
            try:
                html_content = generate_html(session_key, session_data, file_index, file_info)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                if filepath.exists():
                    updated_files.append(filename)
                    print(f"  ✅ Updated: {filename} [{processed}/{total_files}]")
                else:
                    created_files.append(filename)
                    print(f"  🆕 Created: {filename} [{processed}/{total_files}]")
                    
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Failed: {filename} - {e}")
    
    # Process unstructured files (files in directory but not in our structure)
    if unstructured_files:
        print(f"\n📝 Processing {len(unstructured_files)} unstructured files...")
        for filename in unstructured_files:
            filepath = BASE_DIR / filename
            processed += 1
            
            if check_if_updated(filepath):
                skipped_files.append(filename)
                print(f"  ⏭️  Skipped (updated): {filename}")
                continue
            
            try:
                # Generate generic content for unstructured files
                title = filename.replace('.html', '').replace('_', ' ').title()
                description = f"PHP lesson covering {title.lower()} concepts."
                
                # Create generic file info
                file_info = (filename, title, "45 minutes", description)
                session_data = {"title": "PHP Additional Topics", "files": [file_info]}
                
                html_content = generate_html("additional", session_data, 0, file_info)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                updated_files.append(filename)
                print(f"  ✅ Updated: {filename} [{processed}/{total_files}]")
                
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Failed: {filename} - {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Module 2 Complete Update Summary:")
    print(f"  📁 Total files in directory: {len(existing_files)}")
    print(f"  📋 Files in structure: {len(structured_files)}")
    print(f"  🔍 Unstructured files: {len(unstructured_files)}")
    print(f"  ✅ Successfully updated: {len(updated_files)}")
    print(f"  🆕 Newly created: {len(created_files)}")
    print(f"  ⏭️  Already updated: {len(skipped_files) + len(already_updated_files)}")
    print(f"  ❌ Failed: {len(failed_files)}")
    
    if failed_files:
        print(f"\n⚠️ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    if unstructured_files:
        print(f"\n📝 Unstructured files processed:")
        for filename in unstructured_files[:10]:  # Show first 10
            print(f"  - {filename}")
        if len(unstructured_files) > 10:
            print(f"  ... and {len(unstructured_files) - 10} more")
    
    print(f"\n🎉 Module 2 update complete!")
    print(f"📅 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create summary file
    summary_path = BASE_DIR.parent / f"module2_complete_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module 2: PHP Fundamentals - Complete Update Results
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Directory:** {BASE_DIR}

## Summary
- **Total Files in Directory:** {len(existing_files)}
- **Files in Structure Definition:** {len(structured_files)}
- **Unstructured Files:** {len(unstructured_files)}
- **Successfully Updated:** {len(updated_files)}
- **Newly Created:** {len(created_files)}
- **Already Updated:** {len(skipped_files) + len(already_updated_files)}
- **Failed:** {len(failed_files)}

## Module 2 Topics Covered
- PHP Basics & Setup ({len(module2_files.get('php_basics', {}).get('files', []))} files)
- Variables & Data Types ({len(module2_files.get('variables_data_types', {}).get('files', []))} files)
- Operators ({len(module2_files.get('operators', {}).get('files', []))} files)
- Control Structures ({len(module2_files.get('control_structures', {}).get('files', []))} files)
- Loops ({len(module2_files.get('loops', {}).get('files', []))} files)
- Functions ({len(module2_files.get('functions', {}).get('files', []))} files)
- Arrays ({len(module2_files.get('arrays', {}).get('files', []))} files)
- Forms ({len(module2_files.get('forms', {}).get('files', []))} files)
- Sessions & Cookies ({len(module2_files.get('sessions_cookies', {}).get('files', []))} files)
- Object-Oriented PHP ({len(module2_files.get('oop', {}).get('files', []))} files)
- Database Operations ({len(module2_files.get('database', {}).get('files', []))} files)
- APIs & Web Services ({len(module2_files.get('apis', {}).get('files', []))} files)
- Security ({len(module2_files.get('security', {}).get('files', []))} files)
- Frameworks ({len(module2_files.get('frameworks', {}).get('files', []))} files)
- Testing & Debugging ({len(module2_files.get('testing_debugging', {}).get('files', []))} files)
- Advanced Topics ({len(module2_files.get('advanced', {}).get('files', []))} files)
- Projects ({len(module2_files.get('projects', {}).get('files', []))} files)

## Unstructured Files Processed
{chr(10).join(f"- {f}" for f in sorted(unstructured_files)) if unstructured_files else "None"}

## Failed Files
{chr(10).join(f"- {f[0]}: {f[1]}" for f in failed_files) if failed_files else "None"}

## Completion Status
- **Total Progress:** {((len(updated_files) + len(created_files) + len(skipped_files) + len(already_updated_files)) / total_files * 100):.1f}%
- **Module 2 Ready:** {"✅ Yes" if len(failed_files) == 0 else "⚠️ Review failed files"}

## Next Steps
1. Review any failed files
2. Test navigation between lessons
3. Add PHP code examples
4. Deploy Module 2
""")
    
    print(f"\n📝 Summary saved to: {summary_path}")
    return updated_files + created_files, failed_files

if __name__ == "__main__":
    import sys
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    # Run the update
    try:
        successful, failed = main()
        
        # Exit with appropriate code
        if failed:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Update interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
