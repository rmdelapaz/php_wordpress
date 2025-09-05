#!/usr/bin/env python3
"""
Batch update script for ALL Module 1 HTML files
Ensures every single file in 01module directory is updated with new template
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

def check_if_updated(filepath):
    """
    Check if a file has already been updated with the new template
    by looking for specific markers in the file content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # Read first 2000 chars for better detection
            
            # Check for new template markers (must have most of these)
            markers = [
                'class="site-header"',
                'class="lesson-objectives"',
                'class="lesson-navigation"',
                'PHP WordPress Course',
                'class="sidebar-nav"',
                'class="lesson-content"',
                'class="progress-container"',
                'class="breadcrumb container"'
            ]
            
            # If 5 or more markers are found, file is likely updated
            found_markers = sum(1 for marker in markers if marker in content)
            return found_markers >= 5
            
    except Exception as e:
        print(f"    ⚠️ Could not check file: {e}")
        return False

# Define all known Module 1 files with metadata
module1_structure = {
    # Introduction
    "course_introduction.html": ("Course Introduction", "30 minutes", "Welcome to the PHP WordPress Development course. Learn what you'll build and the skills you'll gain."),
    "homework_setup.html": ("Homework: Development Setup", "45 minutes", "Set up your development environment for the course."),
    
    # Session 1: Introduction to Web Development
    "how_web_works.html": ("How the Web Works", "45 minutes", "Understand the fundamentals of how websites and the internet work together."),
    "development_environment.html": ("Setting Up Development Environment", "60 minutes", "Install and configure the tools you'll need for web development."),
    
    # Session 2: HTML Fundamentals
    "first_html_page.html": ("Creating Your First HTML Page", "30 minutes", "Build your very first webpage using HTML."),
    "html_structure_syntax.html": ("HTML Structure and Syntax", "45 minutes", "Learn the fundamental structure and syntax of HTML documents."),
    "essential_html_tags.html": ("Essential HTML Tags", "45 minutes", "Master the most important HTML tags for structuring content."),
    "html_forms_inputs.html": ("HTML Forms and Inputs", "45 minutes", "Create interactive forms for user input."),
    "html_validation_practices.html": ("HTML Validation and Best Practices", "30 minutes", "Learn to write valid, semantic HTML following best practices."),
    "homework_html_profile.html": ("Homework: Create a Personal Profile Page", "60 minutes", "Build a complete personal profile page using HTML."),
    
    # Session 3: CSS Basics
    "introduction_to_css.html": ("Introduction to CSS", "30 minutes", "Discover how CSS transforms HTML into beautiful web pages."),
    "css_syntax_and_selectors.html": ("CSS Syntax and Selectors", "45 minutes", "Master CSS syntax and learn to target HTML elements."),
    "css_implementation_methods.html": ("CSS Implementation Methods", "30 minutes", "Learn different ways to add CSS to HTML documents."),
    "css_colors_fonts_text.html": ("CSS Colors, Fonts, and Text", "45 minutes", "Style text with colors, fonts, and typography properties."),
    "css_box_model.html": ("The CSS Box Model", "45 minutes", "Understand how elements are sized and spaced with the box model."),
    "homework_css_profile.html": ("Homework: Style Your Profile Page", "60 minutes", "Apply CSS to create an attractive profile page design."),
    
    # Session 4: CSS Layout & Responsive Design
    "css_layout_tech.html": ("CSS Layout Techniques", "60 minutes", "Learn modern CSS layout methods including Flexbox and Grid."),
    "responsive_design.html": ("Introduction to Responsive Design", "45 minutes", "Create websites that work perfectly on all devices."),
    "media_queries.html": ("Media Queries", "45 minutes", "Use media queries to create responsive designs."),
    "mobile_first.html": ("Mobile-First Approach", "30 minutes", "Design for mobile devices first, then scale up."),
    "homework_responsive_profile.html": ("Homework: Make Your Profile Responsive", "60 minutes", "Transform your profile into a responsive design."),
    
    # Session 5: CSS Frameworks
    "bootstrap.html": ("Introduction to Bootstrap", "45 minutes", "Get started with the Bootstrap CSS framework."),
    "bootstrap_grid.html": ("Bootstrap Grid System", "45 minutes", "Master Bootstrap's powerful grid system."),
    "bootstrap_components.html": ("Bootstrap Components", "45 minutes", "Use Bootstrap's pre-built UI components."),
    "bootstrap_utilities.html": ("Bootstrap Utilities", "30 minutes", "Apply Bootstrap utility classes for quick styling."),
    "css_organization_best_practices.html": ("CSS Organization Best Practices", "30 minutes", "Organize and maintain scalable CSS code."),
    "css_preprocessors.html": ("CSS Preprocessors Overview", "30 minutes", "Introduction to SASS and CSS preprocessing."),
    "homework_bootstrap_profile.html": ("Homework: Bootstrap Profile", "60 minutes", "Rebuild your profile using Bootstrap."),
    
    # Session 6: JavaScript Fundamentals
    "js_intro.html": ("Introduction to JavaScript", "45 minutes", "Discover JavaScript and its role in web development."),
    "js_syntax_fundamentals.html": ("JavaScript Syntax Fundamentals", "45 minutes", "Learn JavaScript syntax and basic concepts."),
    "js_syntaxx1.html": ("JavaScript Syntax Extended", "45 minutes", "Deep dive into JavaScript syntax patterns."),
    "js_operators_and_expressions.html": ("Operators and Expressions", "30 minutes", "Master JavaScript operators and expressions."),
    "js_control_flow.html": ("Control Flow", "45 minutes", "Implement conditional logic and loops."),
    "js_functions_and_scope.html": ("Functions and Scope", "45 minutes", "Create functions and understand scope."),
    "homework_simple_js_programs.html": ("Homework: Simple JavaScript Programs", "60 minutes", "Build interactive JavaScript programs."),
    
    # Session 7: DOM Manipulation
    "understanding_dom.html": ("Understanding the DOM", "45 minutes", "Learn how JavaScript interacts with HTML."),
    "dom_selection_manipulation.html": ("DOM Selection and Manipulation", "45 minutes", "Select and modify HTML elements with JavaScript."),
    "event_handling.html": ("Event Handling", "45 minutes", "Handle user interactions with events."),
    "creating_removing_elements.html": ("Creating and Removing Elements", "30 minutes", "Dynamically modify page content."),
    "form_validation.html": ("Form Validation", "45 minutes", "Validate forms with JavaScript."),
    "homework_interactive.html": ("Homework: Add Interactivity", "60 minutes", "Make your page interactive with JavaScript."),
    
    # Session 8: Modern JavaScript & jQuery
    "es6_overview.html": ("ES6+ Features Overview", "45 minutes", "Explore modern JavaScript features."),
    "jquery_intro.html": ("Introduction to jQuery", "45 minutes", "Get started with the jQuery library."),
    "jquery_dom_manipulation.html": ("jQuery DOM Manipulation", "45 minutes", "Simplify DOM manipulation with jQuery."),
    "jquery_animations_and_effects.html": ("jQuery Animations", "30 minutes", "Create animations with jQuery."),
    "jquery_ajax.html": ("AJAX with jQuery", "45 minutes", "Make asynchronous requests with jQuery."),
    "homework_jquery_refactor.html": ("Homework: jQuery Refactor", "60 minutes", "Refactor your code using jQuery."),
    
    # Session 9: Introduction to PHP
    "php_and_wordpress.html": ("PHP and WordPress", "45 minutes", "Understand PHP's role in WordPress."),
    "php_setup_xampp_mamp.html": ("Setting Up XAMPP/MAMP", "45 minutes", "Install a local PHP server."),
    "php_syntax.html": ("PHP Syntax", "45 minutes", "Learn PHP syntax basics."),
    "php_variables_data_and_operators.html": ("PHP Variables and Operators", "45 minutes", "Work with PHP variables and operators."),
    "php_includes.html": ("PHP Includes", "30 minutes", "Include PHP files in HTML."),
    "homework_simple_php.html": ("Homework: Simple PHP Script", "60 minutes", "Create your first PHP application."),
    
    # Session 10: Mini-Project
    "planning_website.html": ("Planning a Website", "45 minutes", "Plan a multi-page website project."),
    "creating_layout.html": ("Creating a Layout", "60 minutes", "Build a consistent website layout."),
    "adding_interactivity_with_js.html": ("Adding Interactivity", "60 minutes", "Enhance your site with JavaScript."),
    "php_header_footer.html": ("PHP Headers and Footers", "45 minutes", "Use PHP for consistent headers/footers."),
    "project_static_site.html": ("Final Project: Static Website", "180 minutes", "Build a complete 5-page website.")
}

def generate_html(filename, title, duration, description):
    """Generate complete HTML for a lesson file"""
    
    # Determine session based on filename patterns
    session_title = determine_session(filename)
    
    # Generate navigation URLs
    prev_url, next_url = generate_nav_urls(filename)
    
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
                    {generate_sidebar(session_title, filename)}
                    
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
                                    <span>Module 1: {session_title}</span>
                                </div>
                            </div>
                        </header>

                        {generate_objectives(title)}
                        
                        <!-- Lesson Body -->
                        <div class="lesson-body">
                            {generate_content(title, description)}
                            {generate_homework(title)}
                            {generate_resources(title)}
                        </div>

                        {generate_navigation(prev_url, next_url)}
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

def determine_session(filename):
    """Determine the session title based on filename"""
    if "introduction" in filename or "homework_setup" in filename:
        return "Course Introduction"
    elif "how_web" in filename or "development_environment" in filename:
        return "Web Development Basics"
    elif any(x in filename for x in ["html_", "first_html"]):
        return "HTML Fundamentals"
    elif "css_" in filename and "layout" not in filename and "bootstrap" not in filename:
        return "CSS Basics"
    elif any(x in filename for x in ["layout", "responsive", "media", "mobile"]):
        return "CSS Layout & Responsive Design"
    elif "bootstrap" in filename or "preprocessor" in filename:
        return "CSS Frameworks"
    elif any(x in filename for x in ["js_", "javascript"]) and "jquery" not in filename and "dom" not in filename:
        return "JavaScript Fundamentals"
    elif "dom" in filename or "event" in filename or "form_validation" in filename:
        return "DOM Manipulation"
    elif "jquery" in filename or "es6" in filename or "ajax" in filename:
        return "Modern JavaScript & jQuery"
    elif "php" in filename:
        return "Introduction to PHP"
    elif any(x in filename for x in ["planning", "creating_layout", "project", "adding_interactivity"]):
        return "Mini-Project"
    else:
        return "Web Development"

def generate_nav_urls(filename):
    """Generate previous and next URLs based on logical flow"""
    # This is simplified - you can expand this based on actual course flow
    return ("/module1.html", "/module1.html")

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

def generate_sidebar(session_title, current_file):
    """Generate sidebar HTML"""
    sidebar = f"""                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: {session_title}</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Quick Navigation</h4>
                                <a href="/module1.html" class="sidebar-link">Module Overview</a>
                                <a href="/01module/course_introduction.html" class="sidebar-link">Course Introduction</a>
                                <a href="/01module/first_html_page.html" class="sidebar-link">HTML Basics</a>
                                <a href="/01module/introduction_to_css.html" class="sidebar-link">CSS Fundamentals</a>
                                <a href="/01module/js_intro.html" class="sidebar-link">JavaScript Intro</a>
                                <a href="/01module/php_and_wordpress.html" class="sidebar-link">PHP & WordPress</a>
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
    
    if any(word in title_lower for word in ["html", "tag", "form", "validation"]):
        objectives += """
                                <li>Understand HTML structure and semantics</li>
                                <li>Create well-formed HTML documents</li>
                                <li>Use HTML tags effectively</li>
                                <li>Build accessible web content</li>"""
    elif any(word in title_lower for word in ["css", "style", "color", "font", "box"]):
        objectives += """
                                <li>Master CSS styling techniques</li>
                                <li>Control visual presentation</li>
                                <li>Create attractive designs</li>
                                <li>Understand CSS best practices</li>"""
    elif any(word in title_lower for word in ["javascript", "js", "dom", "event", "jquery"]):
        objectives += """
                                <li>Understand JavaScript fundamentals</li>
                                <li>Add interactivity to web pages</li>
                                <li>Manipulate page elements dynamically</li>
                                <li>Handle user interactions</li>"""
    elif "php" in title_lower:
        objectives += """
                                <li>Understand PHP basics</li>
                                <li>Set up PHP development environment</li>
                                <li>Write server-side code</li>
                                <li>Prepare for WordPress development</li>"""
    elif any(word in title_lower for word in ["responsive", "mobile", "bootstrap", "layout"]):
        objectives += """
                                <li>Create responsive layouts</li>
                                <li>Design for multiple devices</li>
                                <li>Use modern CSS techniques</li>
                                <li>Build flexible designs</li>"""
    else:
        objectives += """
                                <li>Master the concepts in this lesson</li>
                                <li>Apply knowledge through practice</li>
                                <li>Build practical skills</li>
                                <li>Prepare for next topics</li>"""
    
    objectives += """
                            </ul>
                        </div>"""
    
    return objectives

def generate_content(title, description):
    """Generate lesson content"""
    return f"""                            <section>
                                <h2>Introduction</h2>
                                <p class="lead">{description}</p>
                                
                                <div class="alert alert-info">
                                    <div class="alert-icon">💡</div>
                                    <div class="alert-content">
                                        <div class="alert-title">Key Concept</div>
                                        <div class="alert-message">This lesson builds on previous knowledge and prepares you for advanced topics.</div>
                                    </div>
                                </div>
                            </section>

                            <section>
                                <h2>Main Content</h2>
                                <p>This section contains the main lesson content with examples and explanations.</p>
                                
                                <pre><code>// Example code
// Specific to lesson topic</code></pre>
                                
                                <div class="best_practice">
                                    <h3>Best Practices</h3>
                                    <ul>
                                        <li>Follow industry standards</li>
                                        <li>Write clean, maintainable code</li>
                                        <li>Test thoroughly</li>
                                        <li>Document your work</li>
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
                                        <div class="alert-message">Practice makes perfect! Complete this exercise.</div>
                                    </div>
                                </div>
                            </section>"""

def generate_homework(title):
    """Generate homework section"""
    if "homework" in title.lower():
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Assignment Details</h2>
                                <p>Complete the following tasks:</p>
                                <ol>
                                    <li>Review lesson concepts</li>
                                    <li>Complete practical exercises</li>
                                    <li>Submit your work</li>
                                </ol>
                                
                                <p><strong>Submission:</strong> Upload completed files to the course platform.</p>
                            </div>"""
    else:
        return """                            <!-- Homework -->
                            <div class="homework">
                                <h2>Practice Assignment</h2>
                                <p>Reinforce your learning:</p>
                                <ul>
                                    <li>Review key concepts</li>
                                    <li>Complete exercises</li>
                                    <li>Prepare for next lesson</li>
                                </ul>
                            </div>"""

def generate_resources(title):
    """Generate resources section"""
    return """                            <!-- Resources -->
                            <section class="resources">
                                <h2>Additional Resources</h2>
                                <ul>
                                    <li><a href="https://developer.mozilla.org/" target="_blank">MDN Web Docs</a></li>
                                    <li><a href="https://www.w3schools.com/" target="_blank">W3Schools</a></li>
                                    <li><a href="https://css-tricks.com/" target="_blank">CSS-Tricks</a></li>
                                    <li><a href="https://javascript.info/" target="_blank">JavaScript.info</a></li>
                                </ul>
                            </section>"""

def generate_navigation(prev_url, next_url):
    """Generate lesson navigation"""
    return f"""                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">
                            <a href="{prev_url}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    Back to Overview
                                </span>
                            </a>
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>
                            
                            <a href="{next_url}" class="lesson-nav-button next">
                                <span>
                                    <small>Next</small><br>
                                    Continue Learning
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>
                        </div>"""

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
    """Main function to update ALL files in 01module"""
    
    print(f"🚀 Module 1 Complete Update Script")
    print("="*60)
    print(f"📁 Working directory: {BASE_DIR}")
    print(f"✅ Directory exists: {BASE_DIR.exists()}")
    print(f"📅 Update started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get ALL HTML files in directory
    all_files = list(BASE_DIR.glob("*.html"))
    all_filenames = [f.name for f in all_files]
    
    print(f"\n📊 Found {len(all_files)} HTML files in directory")
    print(f"📋 Structure contains {len(module1_structure)} defined files")
    
    # Find files not in structure
    unstructured_files = [f for f in all_filenames if f not in module1_structure]
    if unstructured_files:
        print(f"🔍 Found {len(unstructured_files)} unstructured files:")
        for f in unstructured_files:
            print(f"  - {f}")
    
    updated_files = []
    skipped_files = []
    failed_files = []
    processed = 0
    total_files = len(all_files)
    
    print(f"\n📝 Processing ALL {total_files} files...")
    print("-" * 60)
    
    # Process each file in directory
    for filepath in all_files:
        filename = filepath.name
        processed += 1
        
        # Check if already updated
        if check_if_updated(filepath):
            skipped_files.append(filename)
            print(f"[{processed:3}/{total_files}] ⏭️  Already updated: {filename}")
            continue
        
        try:
            # Get metadata from structure or create generic
            if filename in module1_structure:
                title, duration, description = module1_structure[filename]
            else:
                # Create generic metadata for unstructured files
                title = filename.replace('.html', '').replace('_', ' ').title()
                duration = "45 minutes"
                description = f"Learn about {title.lower()} in this comprehensive lesson."
            
            # Generate HTML content
            html_content = generate_html(filename, title, duration, description)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated_files.append(filename)
            print(f"[{processed:3}/{total_files}] ✅ Updated: {filename}")
            
        except Exception as e:
            failed_files.append((filename, str(e)))
            print(f"[{processed:3}/{total_files}] ❌ Failed: {filename} - {e}")
    
    # Summary
    print("-" * 60)
    print(f"\n📊 Update Complete Summary:")
    print(f"  📁 Total files in directory: {total_files}")
    print(f"  ✅ Successfully updated: {len(updated_files)}")
    print(f"  ⏭️  Already up-to-date: {len(skipped_files)}")
    print(f"  ❌ Failed: {len(failed_files)}")
    
    # Show details if needed
    if failed_files:
        print(f"\n⚠️ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    # Calculate completion
    completion = ((len(updated_files) + len(skipped_files)) / total_files * 100) if total_files > 0 else 0
    print(f"\n📈 Module 1 Completion: {completion:.1f}%")
    
    if completion == 100:
        print("🎉 All Module 1 files are now updated!")
    else:
        print(f"⚠️  {total_files - len(updated_files) - len(skipped_files)} files still need attention")
    
    print(f"\n📅 Update finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create detailed report
    report_path = BASE_DIR.parent / f"module1_complete_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module 1 Complete Update Report
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Directory:** {BASE_DIR}

## Summary
- **Total Files:** {total_files}
- **Updated:** {len(updated_files)}
- **Already Current:** {len(skipped_files)}
- **Failed:** {len(failed_files)}
- **Completion:** {completion:.1f}%

## Files Status

### ✅ Successfully Updated ({len(updated_files)})
{chr(10).join(f"- {f}" for f in sorted(updated_files)) if updated_files else "None"}

### ⏭️ Already Up-to-Date ({len(skipped_files)})
{chr(10).join(f"- {f}" for f in sorted(skipped_files)) if skipped_files else "None"}

### ❌ Failed ({len(failed_files)})
{chr(10).join(f"- {f[0]}: {f[1]}" for f in failed_files) if failed_files else "None"}

### 🔍 Unstructured Files ({len(unstructured_files)})
{chr(10).join(f"- {f}" for f in sorted(unstructured_files)) if unstructured_files else "None"}

## Next Steps
1. Review any failed files manually
2. Test navigation and links
3. Verify all content displays correctly
4. Deploy Module 1

## Module 1 Topics Covered
- Course Introduction & Setup
- HTML Fundamentals
- CSS Basics & Layout
- Responsive Design
- Bootstrap Framework
- JavaScript Programming
- DOM Manipulation
- jQuery & Modern JS
- PHP Introduction
- Final Project

**Status:** {"✅ Ready for deployment" if completion == 100 else "⚠️ Review needed"}
""")
    
    print(f"\n📝 Detailed report saved to: {report_path}")
    
    return updated_files, failed_files

if __name__ == "__main__":
    import sys
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    try:
        updated, failed = main()
        
        # Exit with appropriate code
        if failed:
            sys.exit(1)  # Error if files failed
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
