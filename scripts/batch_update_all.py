#!/usr/bin/env python3
"""
Batch update script for ALL remaining Module 1 HTML files
Fixed with correct Linux paths and skip logic for already updated files
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Base directory - Linux path
BASE_DIR = Path("/home/practicalace/projects/php_wordpress/01module")

# Check if directory exists
if not BASE_DIR.exists():
    print(f"❌ Error: Directory {BASE_DIR} does not exist!")
    print(f"Current working directory: {os.getcwd()}")
    print("\nTrying alternative paths...")
    
    # Try alternative paths
    alt_paths = [
        Path.cwd() / "01module",
        Path.home() / "projects/php_wordpress/01module",
        Path("/mnt/c/Users") / os.environ.get('USER', '') / "projects/php_wordpress/01module"
    ]
    
    for alt_path in alt_paths:
        if alt_path.exists():
            BASE_DIR = alt_path
            print(f"✅ Found directory at: {BASE_DIR}")
            break
    else:
        print("❌ Could not find the 01module directory. Please update BASE_DIR in the script.")
        exit(1)

# Files that have already been updated (will be skipped)
ALREADY_UPDATED = [
    "course_introduction.html",
    "how_web_works.html", 
    "development_environment.html",
    "first_html_page.html",
    "html_structure_syntax.html",
    "essential_html_tags.html",
    "html_forms_inputs.html",
    "introduction_to_css.html"
]

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

# Module 1 complete structure with ALL files
module1_files = {
    "session2": {
        "title": "HTML Fundamentals",
        "files": [
            ("html_validation_practices.html", "HTML Validation and Best Practices", "30 minutes",
             "Master HTML validation techniques, semantic markup, and best practices for clean, maintainable HTML code."),
            ("homework_html_profile.html", "Homework: Create a Personal Profile Page", "60 minutes",
             "Apply your HTML knowledge to build a complete personal profile page with proper structure and semantic markup.")
        ]
    },
    "session3": {
        "title": "CSS Basics",
        "files": [
            ("css_syntax_and_selectors.html", "CSS Syntax and Selectors", "45 minutes",
             "Master CSS syntax, understand different types of selectors, and learn how to target HTML elements effectively."),
            ("css_implementation_methods.html", "Inline, Internal, and External CSS", "30 minutes",
             "Learn the three ways to add CSS to HTML documents and understand when to use each method."),
            ("css_colors_fonts_text.html", "Working with Colors, Fonts, and Text", "45 minutes",
             "Explore CSS properties for colors, typography, and text styling to create visually appealing designs."),
            ("css_box_model.html", "The CSS Box Model", "45 minutes",
             "Understand the CSS box model, including margins, padding, borders, and how elements are sized and spaced."),
            ("homework_css_profile.html", "Homework: Style Your Profile Page", "60 minutes",
             "Apply CSS styling to your HTML profile page to create an attractive, professional design.")
        ]
    },
    "session4": {
        "title": "CSS Layout & Responsive Design",
        "files": [
            ("css_layout_tech.html", "CSS Layout Techniques", "60 minutes",
             "Learn modern CSS layout techniques including Flexbox, Grid, and traditional positioning methods."),
            ("responsive_design.html", "Introduction to Responsive Design", "45 minutes",
             "Understand responsive design principles and create websites that work on all device sizes."),
            ("media_queries.html", "Media Queries", "45 minutes",
             "Master media queries to create responsive designs that adapt to different screen sizes and devices."),
            ("mobile_first.html", "Mobile-First Approach", "30 minutes",
             "Learn the mobile-first design philosophy and how to implement it in your projects."),
            ("homework_responsive_profile.html", "Homework: Make Your Profile Responsive", "60 minutes",
             "Transform your profile page into a fully responsive design that works on all devices.")
        ]
    },
    "session5": {
        "title": "CSS Frameworks & Best Practices",
        "files": [
            ("bootstrap.html", "Introduction to Bootstrap", "45 minutes",
             "Get started with Bootstrap, the world's most popular CSS framework for building responsive websites."),
            ("bootstrap_grid.html", "Using Bootstrap Grid System", "45 minutes",
             "Master Bootstrap's powerful grid system for creating flexible, responsive layouts."),
            ("bootstrap_components.html", "Bootstrap Components", "45 minutes",
             "Explore Bootstrap's pre-built components for navigation, cards, modals, and more."),
            ("bootstrap_utilities.html", "Bootstrap Utilities", "30 minutes",
             "Learn Bootstrap's utility classes for quick styling without writing custom CSS."),
            ("css_organization_best_practices.html", "CSS Organization and Best Practices", "30 minutes",
             "Discover best practices for organizing and maintaining scalable CSS code."),
            ("css_preprocessors.html", "CSS Preprocessors Overview (SASS/SCSS)", "30 minutes",
             "Introduction to CSS preprocessors and how they enhance your styling workflow."),
            ("homework_bootstrap_profile.html", "Homework: Recreate Profile with Bootstrap", "60 minutes",
             "Rebuild your profile page using Bootstrap for a professional, responsive design.")
        ]
    },
    "session6": {
        "title": "JavaScript Fundamentals",
        "files": [
            ("js_intro.html", "Introduction to JavaScript", "45 minutes",
             "Discover JavaScript's role in web development and learn the basics of this powerful programming language."),
            ("js_syntax_fundamentals.html", "JavaScript Syntax, Variables, and Data Types", "45 minutes",
             "Master JavaScript syntax, variables, data types, and basic programming concepts."),
            ("js_operators_and_expressions.html", "Operators and Expressions", "30 minutes",
             "Learn JavaScript operators, expressions, and how to perform calculations and comparisons."),
            ("js_control_flow.html", "Control Flow (Conditionals, Loops)", "45 minutes",
             "Understand conditional statements and loops to control program flow in JavaScript."),
            ("js_functions_and_scope.html", "Functions and Scope", "45 minutes",
             "Master JavaScript functions, scope, and how to write reusable code."),
            ("homework_simple_js_programs.html", "Homework: Create Simple JavaScript Programs", "60 minutes",
             "Practice JavaScript fundamentals by building interactive programs.")
        ]
    },
    "session7": {
        "title": "DOM Manipulation with JavaScript",
        "files": [
            ("understanding_dom.html", "Understanding the Document Object Model (DOM)", "45 minutes",
             "Learn how JavaScript interacts with HTML through the Document Object Model."),
            ("dom_selection_manipulation.html", "Selecting and Manipulating DOM Elements", "45 minutes",
             "Master techniques for selecting and modifying HTML elements with JavaScript."),
            ("event_handling.html", "Event Handling", "45 minutes",
             "Learn to handle user interactions with event listeners and event handlers."),
            ("creating_removing_elements.html", "Creating and Removing Elements", "30 minutes",
             "Dynamically create, modify, and remove HTML elements using JavaScript."),
            ("form_validation.html", "Form Validation with JavaScript", "45 minutes",
             "Implement client-side form validation to improve user experience."),
            ("homework_interactive.html", "Homework: Add Interactivity to Your Page", "60 minutes",
             "Make your profile page interactive with JavaScript DOM manipulation.")
        ]
    },
    "session8": {
        "title": "Modern JavaScript & jQuery",
        "files": [
            ("es6_overview.html", "ES6+ Features Overview", "45 minutes",
             "Explore modern JavaScript features including arrow functions, destructuring, and modules."),
            ("jquery_intro.html", "Introduction to jQuery", "45 minutes",
             "Get started with jQuery, the popular JavaScript library for simplified DOM manipulation."),
            ("jquery_dom_manipulation.html", "DOM Manipulation with jQuery", "45 minutes",
             "Learn jQuery's powerful methods for selecting and manipulating HTML elements."),
            ("jquery_animations_and_effects.html", "jQuery Animations and Effects", "30 minutes",
             "Create smooth animations and visual effects with jQuery."),
            ("jquery_ajax.html", "AJAX Basics with jQuery", "45 minutes",
             "Learn to make asynchronous requests and update pages without reloading."),
            ("homework_jquery_refactor.html", "Homework: Refactor Your Code Using jQuery", "60 minutes",
             "Refactor your JavaScript code using jQuery for cleaner, more efficient code.")
        ]
    },
    "session9": {
        "title": "Introduction to PHP",
        "files": [
            ("php_and_wordpress.html", "What is PHP and Why It's Important for WordPress", "45 minutes",
             "Understand PHP's role in web development and its crucial relationship with WordPress."),
            ("php_setup_xampp_mamp.html", "Setting Up a Local Server (XAMPP/MAMP)", "45 minutes",
             "Install and configure a local development server for PHP development."),
            ("php_syntax.html", "PHP Syntax and Basic Constructs", "45 minutes",
             "Learn PHP syntax, variables, and basic programming constructs."),
            ("php_variables_data_and_operators.html", "Variables, Data Types, and Operators", "45 minutes",
             "Master PHP variables, data types, and operators for dynamic web development."),
            ("php_includes.html", "Including Files and PHP in HTML", "30 minutes",
             "Learn to include PHP files and mix PHP with HTML for dynamic pages."),
            ("homework_simple_php.html", "Homework: Create a Simple PHP Script", "60 minutes",
             "Build your first PHP application with dynamic content generation.")
        ]
    },
    "session10": {
        "title": "Mini-Project: Static Website",
        "files": [
            ("planning_website.html", "Planning a Multi-Page Website", "45 minutes",
             "Learn to plan and structure a complete multi-page website project."),
            ("creating_layout.html", "Creating a Consistent Layout", "60 minutes",
             "Build a consistent layout system for your multi-page website."),
            ("adding_interactivity_with_js.html", "Adding Interactivity with JavaScript", "60 minutes",
             "Enhance your website with JavaScript interactivity and dynamic features."),
            ("php_header_footer.html", "Basic PHP Includes for Header and Footer", "45 minutes",
             "Use PHP includes to maintain consistent headers and footers across pages."),
            ("project_static_site.html", "Final Project: 5-Page Static Website", "180 minutes",
             "Build a complete 5-page website applying all skills learned in Module 1.")
        ]
    }
}

def generate_html(session_key, session_data, file_index, file_info):
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
        prev_sessions = list(module1_files.keys())
        current_session_index = prev_sessions.index(session_key)
        if current_session_index > 0:
            prev_session = module1_files[prev_sessions[current_session_index - 1]]
            if prev_session["files"]:
                prev_file = prev_session["files"][-1]
    
    if file_index < len(all_files) - 1:
        next_file = all_files[file_index + 1]
    else:
        # Link to next session's first file
        next_sessions = list(module1_files.keys())
        current_session_index = next_sessions.index(session_key)
        if current_session_index < len(next_sessions) - 1:
            next_session = module1_files[next_sessions[current_session_index + 1]]
            if next_session["files"]:
                next_file = next_session["files"][0]
    
    # Generate sidebar HTML
    sidebar_html = generate_sidebar(session_title, all_files, file_index)
    
    # Generate navigation HTML
    nav_html = generate_navigation(prev_file, next_file)
    
    # Generate learning objectives based on title
    objectives = generate_objectives(title)
    
    # Generate content based on title
    content = generate_content(title, description)
    
    # Generate homework section
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
        {generate_header()}
        {generate_progress_bar()}
        {generate_breadcrumb(title)}
        
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
                                    <span>Module 1, {session_title}</span>
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

def generate_header():
    """Generate standard header HTML"""
    return """        <!-- Header -->
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
                                    <a href="/module1.html" class="dropdown-item active">Module 1: Web Fundamentals</a>
                                    <a href="/module2.html" class="dropdown-item">Module 2: PHP Fundamentals</a>
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

def generate_breadcrumb(title):
    """Generate breadcrumb HTML"""
    return f"""        <!-- Breadcrumb -->
        <nav class="breadcrumb container" aria-label="Breadcrumb">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <a href="/module1.html">Module 1</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <span aria-current="page">{title}</span>
                </li>
            </ol>
        </nav>"""

def generate_sidebar(session_title, files, current_index):
    """Generate sidebar HTML"""
    sidebar = f"""                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: {session_title}</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Lessons</h4>"""
    
    for i, file_info in enumerate(files):
        filename, title, _, _ = file_info
        active = " active" if i == current_index else ""
        sidebar += f"""
                                <a href="/01module/{filename}" class="sidebar-link{active}">{title}</a>"""
    
    sidebar += """
                            </div>
                        </div>
                    </aside>"""
    
    return sidebar

def generate_navigation(prev_file, next_file):
    """Generate lesson navigation HTML"""
    nav_html = """                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">"""
    
    if prev_file:
        prev_filename, prev_title, _, _ = prev_file
        nav_html += f"""
                            <a href="/01module/{prev_filename}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    {prev_title}
                                </span>
                            </a>"""
    else:
        nav_html += """
                            <a href="/module1.html" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Back to</small><br>
                                    Module 1 Overview
                                </span>
                            </a>"""
    
    nav_html += """
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>"""
    
    if next_file:
        next_filename, next_title, _, _ = next_file
        nav_html += f"""
                            
                            <a href="/01module/{next_filename}" class="lesson-nav-button next">
                                <span>
                                    <small>Next Lesson</small><br>
                                    {next_title}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>"""
    else:
        nav_html += """
                            
                            <a href="/module2.html" class="lesson-nav-button next">
                                <span>
                                    <small>Next Module</small><br>
                                    Module 2: PHP Fundamentals
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
    
    # Add specific objectives based on title keywords
    title_lower = title.lower()
    
    if "validation" in title_lower:
        objectives += """
                                <li>Understand HTML validation and why it matters</li>
                                <li>Learn to use the W3C validator</li>
                                <li>Fix common HTML validation errors</li>
                                <li>Apply best practices for semantic HTML</li>"""
    elif "form" in title_lower:
        objectives += """
                                <li>Create HTML forms with various input types</li>
                                <li>Understand form attributes and validation</li>
                                <li>Build user-friendly forms for data collection</li>
                                <li>Implement accessibility best practices for forms</li>"""
    elif "css" in title_lower and "syntax" in title_lower:
        objectives += """
                                <li>Master CSS syntax and rule structure</li>
                                <li>Understand different types of CSS selectors</li>
                                <li>Learn selector specificity and the cascade</li>
                                <li>Practice writing efficient CSS rules</li>"""
    elif "box model" in title_lower:
        objectives += """
                                <li>Understand the CSS box model concept</li>
                                <li>Master margin, padding, and border properties</li>
                                <li>Control element sizing and spacing</li>
                                <li>Debug layout issues using box model knowledge</li>"""
    elif "javascript" in title_lower or "js" in title_lower:
        objectives += """
                                <li>Understand JavaScript fundamentals</li>
                                <li>Learn programming concepts and syntax</li>
                                <li>Write interactive web applications</li>
                                <li>Debug and troubleshoot JavaScript code</li>"""
    elif "dom" in title_lower:
        objectives += """
                                <li>Understand the Document Object Model</li>
                                <li>Learn to select and manipulate elements</li>
                                <li>Handle events and user interactions</li>
                                <li>Create dynamic web page behavior</li>"""
    elif "jquery" in title_lower:
        objectives += """
                                <li>Understand jQuery fundamentals</li>
                                <li>Simplify DOM manipulation with jQuery</li>
                                <li>Create animations and effects</li>
                                <li>Learn jQuery best practices</li>"""
    elif "bootstrap" in title_lower:
        objectives += """
                                <li>Understand Bootstrap framework fundamentals</li>
                                <li>Use Bootstrap components effectively</li>
                                <li>Create responsive layouts with Bootstrap</li>
                                <li>Customize Bootstrap for your projects</li>"""
    elif "php" in title_lower:
        objectives += """
                                <li>Understand PHP server-side programming</li>
                                <li>Learn PHP syntax and basic constructs</li>
                                <li>Create dynamic web pages with PHP</li>
                                <li>Prepare for WordPress development</li>"""
    elif "responsive" in title_lower:
        objectives += """
                                <li>Understand responsive design principles</li>
                                <li>Create layouts that work on all devices</li>
                                <li>Use media queries effectively</li>
                                <li>Implement mobile-first design approach</li>"""
    elif "layout" in title_lower:
        objectives += """
                                <li>Master CSS layout techniques</li>
                                <li>Understand Flexbox and Grid</li>
                                <li>Create complex page layouts</li>
                                <li>Solve common layout challenges</li>"""
    else:
        objectives += """
                                <li>Master the concepts covered in this lesson</li>
                                <li>Apply knowledge through practical exercises</li>
                                <li>Build confidence with hands-on practice</li>
                                <li>Prepare for advanced topics</li>"""
    
    objectives += """
                            </ul>
                        </div>"""
    
    return objectives

def generate_content(title, description):
    """Generate lesson content based on title - this is placeholder content"""
    content = f"""                            <section>
                                <h2>Introduction</h2>
                                <p class="lead">{description}</p>
                                
                                <div class="alert alert-info">
                                    <div class="alert-icon">💡</div>
                                    <div class="alert-content">
                                        <div class="alert-title">Key Concept</div>
                                        <div class="alert-message">This lesson will build on previous knowledge and prepare you for more advanced topics.</div>
                                    </div>
                                </div>
                            </section>

                            <section>
                                <h2>Main Content</h2>
                                <p>This section contains the main lesson content with examples, code snippets, and explanations.</p>
                                
                                <pre><code>// Example code will go here
// Based on the specific lesson topic</code></pre>
                                
                                <div class="best_practice">
                                    <h3>Best Practices</h3>
                                    <ul>
                                        <li>Follow industry standards</li>
                                        <li>Write clean, maintainable code</li>
                                        <li>Test your work thoroughly</li>
                                        <li>Document your code</li>
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
                                        <div class="alert-message">Practice makes perfect! Complete this exercise to reinforce your learning.</div>
                                    </div>
                                </div>
                            </section>"""
    
    return content

def generate_homework(title):
    """Generate homework section based on title"""
    if "homework" in title.lower():
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Assignment Details</h2>
                                <p>Complete the following tasks to practice what you've learned:</p>
                                <ol>
                                    <li>Review the concepts covered in this session</li>
                                    <li>Complete the practical exercises</li>
                                    <li>Submit your work for review</li>
                                </ol>
                                
                                <p><strong>Submission:</strong> Upload your completed files to the course platform.</p>
                            </div>"""
    else:
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Homework Assignment</h2>
                                <p>Practice what you've learned with these exercises:</p>
                                <ul>
                                    <li>Review the key concepts from this lesson</li>
                                    <li>Complete the practice exercises</li>
                                    <li>Prepare for the next lesson</li>
                                </ul>
                            </div>"""

def generate_resources(title):
    """Generate resources section based on title"""
    return """                            <!-- Resources -->
                            <section class="resources">
                                <h2>Additional Resources</h2>
                                <ul>
                                    <li><a href="https://developer.mozilla.org/" target="_blank">MDN Web Docs</a></li>
                                    <li><a href="https://www.w3schools.com/" target="_blank">W3Schools Tutorials</a></li>
                                    <li><a href="https://css-tricks.com/" target="_blank">CSS-Tricks</a></li>
                                    <li><a href="https://javascript.info/" target="_blank">JavaScript.info</a></li>
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
                            <li><a href="/module1.html">Module 1</a></li>
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
    """Main function to update all files"""
    
    print(f"📁 Working directory: {BASE_DIR}")
    print(f"✅ Directory exists: {BASE_DIR.exists()}")
    print(f"📅 Update started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List existing files
    existing_files = list(BASE_DIR.glob("*.html"))
    print(f"📊 Found {len(existing_files)} HTML files in directory\n")
    
    updated_files = []
    failed_files = []
    skipped_files = []
    already_updated_files = []
    
    # Process all sessions
    total_files = sum(len(session_data["files"]) for session_data in module1_files.values())
    processed = 0
    
    for session_key, session_data in module1_files.items():
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
            
            # Check if file has already been updated
            if filepath.exists() and check_if_updated(filepath):
                skipped_files.append(filename)
                print(f"  ⏭️  Skipped (already updated): {filename}")
                continue
            
            try:
                # Generate HTML content
                html_content = generate_html(session_key, session_data, file_index, file_info)
                
                # Write file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                updated_files.append(filename)
                print(f"  ✅ Updated: {filename} [{processed}/{total_files}]")
                
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Failed: {filename} - {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Update Summary:")
    print(f"  ✅ Successfully updated: {len(updated_files)} files")
    print(f"  ⏭️  Already updated (auto-detected): {len(skipped_files)} files")
    print(f"  ⏭️  Already updated (manual list): {len(already_updated_files)} files")
    print(f"  ❌ Failed: {len(failed_files)} files")
    print(f"  📁 Total processed: {processed}/{total_files} files")
    
    if failed_files:
        print(f"\n⚠️ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    print(f"\n🎉 Batch update complete!")
    print(f"📅 Update finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create summary file
    summary_path = BASE_DIR.parent / f"batch_update_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module 1 Batch Update Results
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Directory:** {BASE_DIR}

## Summary
- **Total Files in Module:** {total_files}
- **Files Processed:** {processed}
- **Successfully Updated:** {len(updated_files)}
- **Already Updated:** {len(skipped_files) + len(already_updated_files)}
- **Failed:** {len(failed_files)}

## Successfully Updated Files ({len(updated_files)})
{chr(10).join(f"- ✅ {f}" for f in sorted(updated_files)) if updated_files else "None"}

## Already Updated - Auto-detected ({len(skipped_files)})
{chr(10).join(f"- ⏭️ {f}" for f in sorted(skipped_files)) if skipped_files else "None"}

## Already Updated - Manual List ({len(already_updated_files)})
{chr(10).join(f"- ⏭️ {f}" for f in sorted(already_updated_files)) if already_updated_files else "None"}

## Failed Files ({len(failed_files)})
{chr(10).join(f"- ❌ {f[0]}: {f[1]}" for f in failed_files) if failed_files else "None"}

## Completion Status
- **Progress:** {((len(updated_files) + len(skipped_files) + len(already_updated_files)) / total_files * 100):.1f}% complete
- **Remaining:** {total_files - len(updated_files) - len(skipped_files) - len(already_updated_files)} files

## Next Steps
1. Review any failed files manually
2. Test navigation links
3. Validate HTML structure
4. Deploy to hosting service
""")
    
    print(f"\n📝 Summary saved to: {summary_path}")
    return updated_files, failed_files

if __name__ == "__main__":
    import sys
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    print("🚀 PHP WordPress Course - Module 1 Batch Update Script")
    print("="*60)
    
    # Run the update
    try:
        updated, failed = main()
        
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
