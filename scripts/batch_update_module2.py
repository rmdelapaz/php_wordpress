#!/usr/bin/env python3
"""
Batch update script for Module 2: PHP Fundamentals
Updates all Module 2 HTML files with the new template structure
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

# Module 2 complete structure - PHP Fundamentals
module2_files = {
    "session1": {
        "title": "PHP Language Basics",
        "files": [
            ("php_fundamentals_review.html", "PHP Fundamentals Review", "45 minutes",
             "Review PHP basics including syntax, variables, and data types to build a strong foundation."),
            ("control_structures_deep_dive.html", "Control Structures Deep Dive", "60 minutes",
             "Master PHP control structures including if/else, switch, loops, and advanced flow control."),
            ("functions_in_php.html", "Functions in PHP", "45 minutes",
             "Learn to create and use functions, understand scope, and work with built-in PHP functions."),
            ("arrays_and_data_manipulation.html", "Arrays and Data Manipulation", "60 minutes",
             "Master PHP arrays, array functions, and data manipulation techniques."),
            ("homework_php_calculator.html", "Homework: Build a PHP Calculator", "90 minutes",
             "Apply PHP fundamentals to build a functional calculator application.")
        ]
    },
    "session2": {
        "title": "Working with Forms and Data",
        "files": [
            ("handling_form_data.html", "Handling Form Data in PHP", "45 minutes",
             "Learn to process form submissions, handle GET and POST data, and validate user input."),
            ("form_validation_sanitization.html", "Form Validation and Sanitization", "60 minutes",
             "Implement secure form validation and data sanitization to prevent security vulnerabilities."),
            ("file_uploads.html", "File Uploads in PHP", "45 minutes",
             "Handle file uploads safely, validate file types, and manage uploaded files."),
            ("sessions_and_cookies.html", "Sessions and Cookies", "60 minutes",
             "Understand PHP sessions and cookies for maintaining user state and data persistence."),
            ("homework_contact_form.html", "Homework: Create a Contact Form", "90 minutes",
             "Build a complete contact form with validation, sanitization, and email functionality.")
        ]
    },
    "session3": {
        "title": "Object-Oriented PHP",
        "files": [
            ("intro_to_oop.html", "Introduction to Object-Oriented Programming", "60 minutes",
             "Understand OOP concepts including classes, objects, properties, and methods in PHP."),
            ("classes_and_objects.html", "Classes and Objects in PHP", "60 minutes",
             "Create PHP classes, instantiate objects, and work with constructors and destructors."),
            ("inheritance_and_polymorphism.html", "Inheritance and Polymorphism", "45 minutes",
             "Master inheritance, method overriding, and polymorphism in PHP OOP."),
            ("interfaces_and_abstract_classes.html", "Interfaces and Abstract Classes", "45 minutes",
             "Learn to use interfaces and abstract classes for better code architecture."),
            ("homework_oop_project.html", "Homework: OOP Mini-Project", "120 minutes",
             "Build a small project using object-oriented PHP principles.")
        ]
    },
    "session4": {
        "title": "Working with Databases",
        "files": [
            ("intro_to_mysql.html", "Introduction to MySQL", "45 minutes",
             "Learn MySQL basics, database design principles, and SQL fundamentals."),
            ("php_mysql_connection.html", "Connecting PHP to MySQL", "45 minutes",
             "Establish database connections using MySQLi and PDO in PHP."),
            ("crud_operations.html", "CRUD Operations", "90 minutes",
             "Implement Create, Read, Update, and Delete operations with PHP and MySQL."),
            ("prepared_statements.html", "Prepared Statements and Security", "60 minutes",
             "Use prepared statements to prevent SQL injection and secure database operations."),
            ("homework_user_management.html", "Homework: User Management System", "120 minutes",
             "Build a user management system with registration, login, and profile features.")
        ]
    },
    "session5": {
        "title": "PHP and Web APIs",
        "files": [
            ("working_with_json.html", "Working with JSON in PHP", "45 minutes",
             "Parse and generate JSON data, work with JSON APIs in PHP applications."),
            ("consuming_apis.html", "Consuming REST APIs", "60 minutes",
             "Learn to consume external APIs using cURL and PHP's HTTP functions."),
            ("creating_api_endpoints.html", "Creating API Endpoints", "60 minutes",
             "Build RESTful API endpoints with PHP to serve data to applications."),
            ("api_authentication.html", "API Authentication", "45 minutes",
             "Implement API authentication using tokens and API keys."),
            ("homework_weather_app.html", "Homework: Weather App with API", "90 minutes",
             "Create a weather application that consumes external weather APIs.")
        ]
    },
    "session6": {
        "title": "PHP Security Best Practices",
        "files": [
            ("common_vulnerabilities.html", "Common PHP Security Vulnerabilities", "60 minutes",
             "Understand common security vulnerabilities in PHP applications and how to prevent them."),
            ("input_validation_techniques.html", "Input Validation Techniques", "45 minutes",
             "Master comprehensive input validation strategies for secure PHP applications."),
            ("password_hashing.html", "Password Hashing and Encryption", "45 minutes",
             "Implement secure password storage using modern hashing algorithms."),
            ("secure_file_handling.html", "Secure File Handling", "45 minutes",
             "Handle files securely, prevent directory traversal, and validate uploads."),
            ("homework_secure_app.html", "Homework: Secure Application", "90 minutes",
             "Refactor an application to implement security best practices.")
        ]
    },
    "session7": {
        "title": "PHP Frameworks Introduction",
        "files": [
            ("mvc_architecture.html", "Understanding MVC Architecture", "60 minutes",
             "Learn the Model-View-Controller pattern and its implementation in PHP."),
            ("intro_to_composer.html", "Introduction to Composer", "45 minutes",
             "Use Composer for dependency management and autoloading in PHP projects."),
            ("laravel_basics.html", "Laravel Framework Basics", "90 minutes",
             "Get started with Laravel, understanding routing, controllers, and views."),
            ("symfony_overview.html", "Symfony Framework Overview", "60 minutes",
             "Explore Symfony components and framework fundamentals."),
            ("homework_framework_project.html", "Homework: Framework Mini-Project", "120 minutes",
             "Build a small application using a PHP framework.")
        ]
    },
    "session8": {
        "title": "Testing and Debugging",
        "files": [
            ("debugging_techniques.html", "PHP Debugging Techniques", "45 minutes",
             "Master debugging tools and techniques for PHP development."),
            ("error_handling.html", "Error Handling and Logging", "45 minutes",
             "Implement proper error handling and logging strategies."),
            ("unit_testing_basics.html", "Unit Testing with PHPUnit", "60 minutes",
             "Write and run unit tests for PHP code using PHPUnit."),
            ("code_quality_tools.html", "Code Quality Tools", "45 minutes",
             "Use tools like PHP CodeSniffer and PHPStan for code quality."),
            ("homework_add_tests.html", "Homework: Add Tests to Project", "90 minutes",
             "Add comprehensive tests to an existing PHP project.")
        ]
    },
    "session9": {
        "title": "Advanced PHP Topics",
        "files": [
            ("namespaces_autoloading.html", "Namespaces and Autoloading", "45 minutes",
             "Organize code with namespaces and implement PSR-4 autoloading."),
            ("traits_and_generators.html", "Traits and Generators", "45 minutes",
             "Use traits for code reuse and generators for memory-efficient iterations."),
            ("regex_in_php.html", "Regular Expressions in PHP", "60 minutes",
             "Master regular expressions for pattern matching and text processing."),
            ("performance_optimization.html", "PHP Performance Optimization", "60 minutes",
             "Optimize PHP applications for better performance and scalability."),
            ("homework_optimization.html", "Homework: Optimize an Application", "90 minutes",
             "Apply optimization techniques to improve application performance.")
        ]
    },
    "session10": {
        "title": "PHP Project",
        "files": [
            ("project_planning.html", "Project Planning and Architecture", "60 minutes",
             "Plan and architect a complete PHP application from scratch."),
            ("database_design.html", "Database Design for Project", "60 minutes",
             "Design an efficient database schema for the project."),
            ("implementing_features.html", "Implementing Core Features", "120 minutes",
             "Build the core features of the PHP application."),
            ("testing_deployment.html", "Testing and Deployment Preparation", "60 minutes",
             "Test the application and prepare it for deployment."),
            ("final_project_blog_cms.html", "Final Project: Blog CMS", "240 minutes",
             "Build a complete blog content management system with PHP.")
        ]
    }
}

def generate_html(session_key, session_data, file_index, file_info, module_num="2"):
    """Generate complete HTML for a lesson file with proper navigation"""
    
    filename, title, duration, description = file_info
    session_title = session_data["title"]
    
    # Get all files in session for navigation
    all_files = session_data["files"]
    
    # Determine previous and next files
    prev_file = None
    next_file = None
    
    if file_index > 0:
        prev_file = all_files[file_index - 1]
    else:
        # Link to previous session's last file
        prev_sessions = list(module2_files.keys())
        current_session_index = prev_sessions.index(session_key)
        if current_session_index > 0:
            prev_session = module2_files[prev_sessions[current_session_index - 1]]
            if prev_session["files"]:
                prev_file = prev_session["files"][-1]
    
    if file_index < len(all_files) - 1:
        next_file = all_files[file_index + 1]
    else:
        # Link to next session's first file
        next_sessions = list(module2_files.keys())
        current_session_index = next_sessions.index(session_key)
        if current_session_index < len(next_sessions) - 1:
            next_session = module2_files[next_sessions[current_session_index + 1]]
            if next_session["files"]:
                next_file = next_session["files"][0]
    
    # Generate components
    sidebar_html = generate_sidebar(session_title, all_files, file_index, module_num)
    nav_html = generate_navigation(prev_file, next_file, module_num)
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
                                    <span>Module {module_num}, {session_title}</span>
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

def generate_navigation(prev_file, next_file, module_num="2"):
    """Generate lesson navigation HTML"""
    nav_html = """                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">"""
    
    if prev_file:
        prev_filename, prev_title, _, _ = prev_file
        nav_html += f"""
                            <a href="/0{module_num}module/{prev_filename}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    {prev_title}
                                </span>
                            </a>"""
    else:
        nav_html += f"""
                            <a href="/module{module_num}.html" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Back to</small><br>
                                    Module {module_num} Overview
                                </span>
                            </a>"""
    
    nav_html += """
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>"""
    
    if next_file:
        next_filename, next_title, _, _ = next_file
        nav_html += f"""
                            
                            <a href="/0{module_num}module/{next_filename}" class="lesson-nav-button next">
                                <span>
                                    <small>Next Lesson</small><br>
                                    {next_title}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>"""
    else:
        next_module = int(module_num) + 1
        nav_html += f"""
                            
                            <a href="/module{next_module}.html" class="lesson-nav-button next">
                                <span>
                                    <small>Next Module</small><br>
                                    Module {next_module}: MySQL Database
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>"""
    
    nav_html += """
                        </div>"""
    
    return nav_html

def generate_objectives(title):
    """Generate learning objectives based on title"""
    objectives = """                        <!-- Learning Objectives -->
                        <div class="lesson-objectives">
                            <h2>Learning Objectives</h2>
                            <ul>"""
    
    title_lower = title.lower()
    
    # PHP-specific objectives based on title
    if "oop" in title_lower or "object" in title_lower:
        objectives += """
                                <li>Understand object-oriented programming principles</li>
                                <li>Create and use classes and objects in PHP</li>
                                <li>Implement inheritance and polymorphism</li>
                                <li>Apply OOP best practices in PHP development</li>"""
    elif "database" in title_lower or "mysql" in title_lower:
        objectives += """
                                <li>Connect PHP applications to MySQL databases</li>
                                <li>Execute SQL queries from PHP code</li>
                                <li>Implement CRUD operations</li>
                                <li>Secure database operations against SQL injection</li>"""
    elif "form" in title_lower:
        objectives += """
                                <li>Process form data with PHP</li>
                                <li>Validate and sanitize user input</li>
                                <li>Handle file uploads securely</li>
                                <li>Implement form security best practices</li>"""
    elif "api" in title_lower:
        objectives += """
                                <li>Work with JSON data in PHP</li>
                                <li>Consume external REST APIs</li>
                                <li>Create API endpoints with PHP</li>
                                <li>Implement API authentication</li>"""
    elif "security" in title_lower:
        objectives += """
                                <li>Identify common PHP security vulnerabilities</li>
                                <li>Implement secure coding practices</li>
                                <li>Validate and sanitize all user input</li>
                                <li>Protect against common attacks</li>"""
    elif "session" in title_lower or "cookie" in title_lower:
        objectives += """
                                <li>Understand PHP sessions and cookies</li>
                                <li>Implement user authentication</li>
                                <li>Maintain user state across pages</li>
                                <li>Handle session security properly</li>"""
    elif "framework" in title_lower:
        objectives += """
                                <li>Understand PHP framework concepts</li>
                                <li>Learn MVC architecture</li>
                                <li>Use Composer for dependency management</li>
                                <li>Build applications with modern PHP frameworks</li>"""
    elif "test" in title_lower:
        objectives += """
                                <li>Write unit tests for PHP code</li>
                                <li>Use PHPUnit testing framework</li>
                                <li>Implement test-driven development</li>
                                <li>Debug PHP applications effectively</li>"""
    else:
        objectives += """
                                <li>Master PHP programming fundamentals</li>
                                <li>Write clean, maintainable PHP code</li>
                                <li>Apply best practices in PHP development</li>
                                <li>Build dynamic web applications with PHP</li>"""
    
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
                                        <div class="alert-message">PHP is the foundation of WordPress development. Mastering PHP will enable you to create powerful WordPress themes and plugins.</div>
                                    </div>
                                </div>
                            </section>

                            <section>
                                <h2>Core Concepts</h2>
                                <p>This lesson covers essential PHP concepts that you'll use throughout your WordPress development journey.</p>
                                
                                <pre><code class="language-php">&lt;?php
// Example PHP code
// Specific to the lesson topic
?&gt;</code></pre>
                                
                                <div class="best_practice">
                                    <h3>Best Practices</h3>
                                    <ul>
                                        <li>Always validate and sanitize user input</li>
                                        <li>Use prepared statements for database queries</li>
                                        <li>Follow PSR coding standards</li>
                                        <li>Implement proper error handling</li>
                                        <li>Keep security as a top priority</li>
                                    </ul>
                                </div>
                            </section>

                            <section>
                                <h2>Practical Examples</h2>
                                <p>Let's explore practical examples that demonstrate these concepts in action.</p>
                                
                                <div class="example-code">
                                    <h3>Example Implementation</h3>
                                    <pre><code class="language-php">&lt;?php
// Practical example code
// Will be customized based on lesson content
?&gt;</code></pre>
                                </div>
                            </section>

                            <section>
                                <h2>WordPress Context</h2>
                                <div class="real_world_example">
                                    <h3>How This Applies to WordPress</h3>
                                    <p>Understanding these PHP concepts is crucial for WordPress development:</p>
                                    <ul>
                                        <li>WordPress core is built with PHP</li>
                                        <li>Themes use PHP for dynamic content</li>
                                        <li>Plugins extend WordPress using PHP</li>
                                        <li>Custom functionality requires PHP knowledge</li>
                                    </ul>
                                </div>
                            </section>

                            <section>
                                <h2>Practice Exercise</h2>
                                <p>Apply what you've learned with this hands-on exercise.</p>
                                
                                <div class="alert alert-success">
                                    <div class="alert-icon">💻</div>
                                    <div class="alert-content">
                                        <div class="alert-title">Try It Now</div>
                                        <div class="alert-message">Set up your local PHP environment and practice these concepts with real code!</div>
                                    </div>
                                </div>
                            </section>"""
    
    return content

def generate_homework(title):
    """Generate homework section based on title"""
    if "homework" in title.lower():
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Project Requirements</h2>
                                <p>Complete this project to demonstrate your understanding of the concepts covered in this session:</p>
                                <ol>
                                    <li>Set up your development environment</li>
                                    <li>Implement the required functionality</li>
                                    <li>Test your code thoroughly</li>
                                    <li>Follow PHP best practices</li>
                                    <li>Document your code</li>
                                </ol>
                                
                                <h3>Submission Guidelines</h3>
                                <ul>
                                    <li>Upload your PHP files to GitHub</li>
                                    <li>Include a README with setup instructions</li>
                                    <li>Ensure code is properly commented</li>
                                    <li>Test on XAMPP/MAMP before submission</li>
                                </ul>
                                
                                <p><strong>Due Date:</strong> Before the next session</p>
                            </div>"""
    else:
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Practice Assignment</h2>
                                <p>Reinforce your learning with these practice exercises:</p>
                                <ul>
                                    <li>Review the code examples from this lesson</li>
                                    <li>Complete the practice exercises</li>
                                    <li>Experiment with variations of the examples</li>
                                    <li>Research additional PHP functions related to this topic</li>
                                </ul>
                                
                                <p><strong>Challenge:</strong> Try to implement a small project using the concepts learned in this lesson.</p>
                            </div>"""

def generate_resources(title):
    """Generate resources section based on title"""
    return """                            <!-- Resources -->
                            <section class="resources">
                                <h2>Additional Resources</h2>
                                <ul>
                                    <li><a href="https://www.php.net/manual/en/" target="_blank">PHP Official Documentation</a></li>
                                    <li><a href="https://phptherightway.com/" target="_blank">PHP: The Right Way</a></li>
                                    <li><a href="https://www.w3schools.com/php/" target="_blank">W3Schools PHP Tutorial</a></li>
                                    <li><a href="https://laracasts.com/topics/php" target="_blank">Laracasts PHP Series</a></li>
                                    <li><a href="https://developer.wordpress.org/apis/" target="_blank">WordPress Developer Resources</a></li>
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
    
    print(f"🚀 PHP WordPress Course - Module 2 Batch Update Script")
    print("="*60)
    print(f"📁 Working directory: {BASE_DIR}")
    print(f"✅ Directory exists: {BASE_DIR.exists()}")
    print(f"📅 Update started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create directory if it doesn't exist
    if not BASE_DIR.exists():
        print(f"📁 Creating directory: {BASE_DIR}")
        BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # List existing files
    existing_files = list(BASE_DIR.glob("*.html"))
    print(f"📊 Found {len(existing_files)} existing HTML files in directory\n")
    
    updated_files = []
    created_files = []
    failed_files = []
    skipped_files = []
    already_updated_files = []
    
    # Process all sessions
    total_files = sum(len(session_data["files"]) for session_data in module2_files.values())
    processed = 0
    
    for session_key, session_data in module2_files.items():
        print(f"\n📁 Processing {session_data['title']}...")
        
        for file_index, file_info in enumerate(session_data["files"]):
            filename = file_info[0]
            filepath = BASE_DIR / filename
            processed += 1
            
            # Check if file is in the manually updated list
            if filename in ALREADY_UPDATED:
                already_updated_files.append(filename)
                print(f"  ⏭️  Skipped (manually updated): {filename}")
                continue
            
            # Check if file exists and has already been updated
            if filepath.exists():
                if check_if_updated(filepath):
                    skipped_files.append(filename)
                    print(f"  ⏭️  Skipped (already updated): {filename}")
                    continue
                
                # File exists but needs updating
                action = "Updated"
                updated_files.append(filename)
            else:
                # File doesn't exist, will be created
                action = "Created"
                created_files.append(filename)
            
            try:
                # Generate HTML content
                html_content = generate_html(session_key, session_data, file_index, file_info)
                
                # Write file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"  ✅ {action}: {filename} [{processed}/{total_files}]")
                
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Failed: {filename} - {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Update Summary for Module 2:")
    print(f"  ✅ Successfully updated: {len(updated_files)} files")
    print(f"  🆕 Newly created: {len(created_files)} files")
    print(f"  ⏭️  Already updated (auto-detected): {len(skipped_files)} files")
    print(f"  ⏭️  Already updated (manual list): {len(already_updated_files)} files")
    print(f"  ❌ Failed: {len(failed_files)} files")
    print(f"  📁 Total processed: {processed}/{total_files} files")
    
    if failed_files:
        print(f"\n⚠️ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    print(f"\n🎉 Module 2 batch update complete!")
    print(f"📅 Update finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create summary file
    summary_path = BASE_DIR.parent / f"module2_update_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module 2: PHP Fundamentals - Batch Update Results
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Directory:** {BASE_DIR}

## Summary
- **Total Files in Module:** {total_files}
- **Files Processed:** {processed}
- **Successfully Updated:** {len(updated_files)}
- **Newly Created:** {len(created_files)}
- **Already Updated:** {len(skipped_files) + len(already_updated_files)}
- **Failed:** {len(failed_files)}

## Successfully Updated Files ({len(updated_files)})
{chr(10).join(f"- ✅ {f}" for f in sorted(updated_files)) if updated_files else "None"}

## Newly Created Files ({len(created_files)})
{chr(10).join(f"- 🆕 {f}" for f in sorted(created_files)) if created_files else "None"}

## Already Updated - Auto-detected ({len(skipped_files)})
{chr(10).join(f"- ⏭️ {f}" for f in sorted(skipped_files)) if skipped_files else "None"}

## Already Updated - Manual List ({len(already_updated_files)})
{chr(10).join(f"- ⏭️ {f}" for f in sorted(already_updated_files)) if already_updated_files else "None"}

## Failed Files ({len(failed_files)})
{chr(10).join(f"- ❌ {f[0]}: {f[1]}" for f in failed_files) if failed_files else "None"}

## Module 2 Structure
- **Sessions:** 10
- **Topics Covered:**
  - PHP Language Basics
  - Working with Forms and Data
  - Object-Oriented PHP
  - Working with Databases
  - PHP and Web APIs
  - PHP Security Best Practices
  - PHP Frameworks Introduction
  - Testing and Debugging
  - Advanced PHP Topics
  - PHP Project

## Completion Status
- **Progress:** {((len(updated_files) + len(created_files) + len(skipped_files) + len(already_updated_files)) / total_files * 100):.1f}% complete
- **Remaining:** {total_files - len(updated_files) - len(created_files) - len(skipped_files) - len(already_updated_files)} files

## Next Steps
1. Review any failed files manually
2. Test navigation links between lessons
3. Validate HTML structure
4. Add specific PHP code examples to each lesson
5. Deploy to hosting service
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
            sys.exit(1)  # Exit with error if any files failed
        else:
            sys.exit(0)  # Success
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Update interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
