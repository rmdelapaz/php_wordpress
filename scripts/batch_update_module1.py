#!/usr/bin/env python3
"""
Batch update script for Module 1 HTML files
Applies the new template structure to all remaining files
"""

import os
import re

# Template for the updated HTML structure
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>{title} - PHP WordPress Course</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
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
        {header}
        {progress_bar}
        {breadcrumb}
        
        <!-- Main Content -->
        <main id="main-content" class="main-content" role="main">
            <div class="container">
                <div class="content-with-sidebar">
                    {sidebar}
                    
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
                                    <span>Module 1, {session}</span>
                                </div>
                            </div>
                        </header>

                        {learning_objectives}
                        
                        <!-- Lesson Body -->
                        <div class="lesson-body">
                            {content}
                            
                            {homework}
                            
                            {resources}
                        </div>

                        {lesson_navigation}
                    </article>
                </div>
            </div>
        </main>

        {footer}
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

# Common header HTML
HEADER_HTML = """        <!-- Header -->
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

# Progress bar HTML
PROGRESS_BAR_HTML = """        <!-- Progress Bar -->
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

# Common footer HTML
FOOTER_HTML = """        <!-- Footer -->
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
                        <h4>Current Module</h4>
                        <ul class="footer-links">
                            {footer_links}
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

# Module 1 structure
module1_structure = {
    "session3": {
        "title": "CSS Basics",
        "files": [
            ("introduction_to_css.html", "Introduction to CSS and Its Purpose", "45 minutes"),
            ("css_syntax_and_selectors.html", "CSS Syntax and Selectors", "45 minutes"),
            ("css_implementation_methods.html", "Inline, Internal, and External CSS", "30 minutes"),
            ("css_colors_fonts_text.html", "Working with Colors, Fonts, and Text", "45 minutes"),
            ("css_box_model.html", "The CSS Box Model", "45 minutes"),
            ("homework_css_profile.html", "Homework: Style Your Profile Page", "60 minutes")
        ]
    },
    "session6": {
        "title": "JavaScript Fundamentals",
        "files": [
            ("js_intro.html", "Introduction to JavaScript", "45 minutes"),
            ("js_syntax_fundamentals.html", "JavaScript Syntax and Variables", "45 minutes"),
            ("js_operators_and_expressions.html", "Operators and Expressions", "30 minutes"),
            ("js_control_flow.html", "Control Flow", "45 minutes"),
            ("js_functions_and_scope.html", "Functions and Scope", "45 minutes"),
            ("homework_simple_js_programs.html", "Homework: Simple JS Programs", "60 minutes")
        ]
    }
}

def create_breadcrumb(title):
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

def create_sidebar(session_title, files, current_index):
    """Generate sidebar HTML"""
    sidebar = f"""                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: {session_title}</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Lessons</h4>"""
    
    for i, (filename, title, _) in enumerate(files):
        active = " active" if i == current_index else ""
        sidebar += f"""
                                <a href="/01module/{filename}" class="sidebar-link{active}">{title}</a>"""
    
    sidebar += """
                            </div>
                        </div>
                    </aside>"""
    
    return sidebar

def create_lesson_navigation(files, current_index):
    """Generate lesson navigation HTML"""
    nav_html = """                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">"""
    
    # Previous button
    if current_index > 0:
        prev_file, prev_title, _ = files[current_index - 1]
        nav_html += f"""
                            <a href="/01module/{prev_file}" class="lesson-nav-button prev">
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
    
    # Next button
    if current_index < len(files) - 1:
        next_file, next_title, _ = files[current_index + 1]
        nav_html += f"""
                            
                            <a href="/01module/{next_file}" class="lesson-nav-button next">
                                <span>
                                    <small>Next Lesson</small><br>
                                    {next_title}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>"""
    
    nav_html += """
                        </div>"""
    
    return nav_html

def create_learning_objectives(title):
    """Generate learning objectives based on title"""
    objectives_html = """                        <!-- Learning Objectives -->
                        <div class="lesson-objectives">
                            <h2>Learning Objectives</h2>
                            <ul>"""
    
    # Add appropriate objectives based on title
    if "CSS" in title:
        objectives_html += """
                                <li>Understand CSS fundamentals and syntax</li>
                                <li>Learn how to style HTML elements</li>
                                <li>Apply CSS to create visually appealing pages</li>
                                <li>Master CSS selectors and properties</li>"""
    elif "JavaScript" in title or "JS" in title:
        objectives_html += """
                                <li>Understand JavaScript basics</li>
                                <li>Learn programming fundamentals</li>
                                <li>Write interactive web applications</li>
                                <li>Master JavaScript syntax and concepts</li>"""
    else:
        objectives_html += """
                                <li>Master the concepts covered in this lesson</li>
                                <li>Apply knowledge to practical examples</li>
                                <li>Build confidence with hands-on practice</li>
                                <li>Prepare for more advanced topics</li>"""
    
    objectives_html += """
                            </ul>
                        </div>"""
    
    return objectives_html

# Print file update list
print("Files to update:")
for session_key, session_data in module1_structure.items():
    print(f"\n{session_data['title']}:")
    for filename, title, duration in session_data['files']:
        print(f"  - {filename}: {title}")

print("\n✅ Batch update script ready!")
print("This script will help update the remaining Module 1 files with the new template structure.")