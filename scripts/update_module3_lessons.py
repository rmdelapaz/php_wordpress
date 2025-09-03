#!/usr/bin/env python3
"""
Script to update Module 3 lesson files to match the proper template structure
Updates the simplified lesson files to include full page wrapper, header, navigation, footer, etc.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/home/practicalace/projects/php_wordpress")

# Check if directory exists
if not BASE_DIR.exists():
    alt_paths = [
        Path.cwd(),
        Path.home() / "projects/php_wordpress",
    ]
    for alt_path in alt_paths:
        if alt_path.exists():
            BASE_DIR = alt_path
            break
    else:
        print("❌ Could not find the project directory.")
        exit(1)

# Module 3 directory
MODULE3_DIR = BASE_DIR / "03module"

# Session 1 lessons mapping
SESSION1_LESSONS = {
    "database_concepts_terminology.html": {
        "title": "Database Concepts and Terminology",
        "description": "Understanding the Foundation of Data Management",
        "duration": "45 minutes",
        "prev": "/module3.html",
        "prev_title": "Module Overview",
        "next": "/03module/types_of_databases.html",
        "next_title": "Types of Databases"
    },
    "types_of_databases.html": {
        "title": "Types of Databases",
        "description": "Relational vs Non-Relational Database Systems",
        "duration": "45 minutes",
        "prev": "/03module/database_concepts_terminology.html",
        "prev_title": "Database Concepts",
        "next": "/03module/introduction_to_mysql.html",
        "next_title": "Introduction to MySQL"
    },
    "intro_to_databases.html": {
        "title": "Introduction to Databases",
        "description": "Understanding the Foundation of Data Storage and Management",
        "duration": "30 minutes",
        "prev": "/module3.html",
        "prev_title": "Module Overview",
        "next": "/03module/mysql_installation.html",
        "next_title": "MySQL Installation"
    },
    "mysql_installation.html": {
        "title": "MySQL Installation and Setup",
        "description": "Setting Up Your Database Development Environment",
        "duration": "60 minutes",
        "prev": "/03module/intro_to_databases.html",
        "prev_title": "Intro to Databases",
        "next": "/03module/database_design_principles.html",
        "next_title": "Database Design"
    },
    "database_design_principles.html": {
        "title": "Database Design Principles",
        "description": "Building Strong Foundations for Your Data Architecture",
        "duration": "45 minutes",
        "prev": "/03module/mysql_installation.html",
        "prev_title": "MySQL Installation",
        "next": "/03module/creating_databases_tables.html",
        "next_title": "Creating Databases"
    },
    "creating_databases_tables.html": {
        "title": "Creating Databases and Tables",
        "description": "Building Your Data Structure with SQL Commands",
        "duration": "60 minutes",
        "prev": "/03module/database_design_principles.html",
        "prev_title": "Database Design",
        "next": "/03module/data_types.html",
        "next_title": "Data Types"
    },
    "data_types.html": {
        "title": "MySQL Data Types",
        "description": "Choosing the Right Container for Your Data",
        "duration": "45 minutes",
        "prev": "/03module/creating_databases_tables.html",
        "prev_title": "Creating Tables",
        "next": "/03module/homework_database_design.html",
        "next_title": "Homework"
    },
    "homework_database_design.html": {
        "title": "Homework: Design a Database Schema",
        "description": "Design a Complete Database Schema for BookHub",
        "duration": "2-3 hours",
        "prev": "/03module/data_types.html",
        "prev_title": "Data Types",
        "next": "/module3.html",
        "next_title": "Back to Module"
    }
}

def extract_lesson_content(filepath):
    """Extract the main content from existing lesson file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the body content (everything inside <body> tags)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if not body_match:
            return None
            
        body_content = body_match.group(1)
        
        # Try to extract lesson-container content
        container_match = re.search(r'<div class="lesson-container">(.*?)</div>\s*(?:<script|</body)', body_content, re.DOTALL)
        if container_match:
            return container_match.group(1).strip()
        
        # Fallback: try to extract main content sections
        sections = []
        
        # Extract learning objectives
        obj_match = re.search(r'<div class="learning-objectives">(.*?)</div>', body_content, re.DOTALL)
        if obj_match:
            sections.append(obj_match.group(0))
        
        # Extract content sections
        content_matches = re.findall(r'<(?:div|section) class="(?:content-section|lesson-content)">(.*?)</(?:div|section)>', body_content, re.DOTALL)
        for match in content_matches:
            sections.append(f'<section>{match}</section>')
        
        # Extract any canvas elements with their scripts
        canvas_matches = re.findall(r'<canvas[^>]*>.*?</canvas>.*?<script>.*?</script>', body_content, re.DOTALL)
        for match in canvas_matches:
            if match not in '\n'.join(sections):
                sections.append(match)
        
        return '\n'.join(sections) if sections else body_content
        
    except Exception as e:
        print(f"   ⚠️ Error extracting content from {filepath}: {e}")
        return None

def create_proper_lesson_file(filename, lesson_info, content):
    """Create a properly structured lesson file"""
    
    # Generate sidebar links for Session 1
    sidebar_links = """
                                <a href="/module3.html" class="sidebar-link">Module Overview</a>
                                <a href="/03module/database_concepts_terminology.html" class="sidebar-link{active1}">Database Concepts</a>
                                <a href="/03module/types_of_databases.html" class="sidebar-link{active2}">Types of Databases</a>
                                <a href="/03module/introduction_to_mysql.html" class="sidebar-link{active3}">Intro to MySQL</a>
                                <a href="/03module/mysql_xampp_mamp.html" class="sidebar-link{active4}">MySQL in XAMPP/MAMP</a>
                                <a href="/03module/using_phpmyadmin.html" class="sidebar-link{active5}">Using phpMyAdmin</a>
                                <a href="/03module/creating_databases_tables.html" class="sidebar-link{active6}">Creating Databases</a>
                                <a href="/03module/homework_database_schema.html" class="sidebar-link{active7}">Homework</a>"""
    
    # Mark the active link
    active_markers = {
        "active1": "", "active2": "", "active3": "", "active4": "",
        "active5": "", "active6": "", "active7": ""
    }
    
    if "database_concepts" in filename:
        active_markers["active1"] = " active"
    elif "types_of_databases" in filename:
        active_markers["active2"] = " active"
    elif "introduction_to_mysql" in filename or "intro_to_databases" in filename:
        active_markers["active3"] = " active"
    elif "xampp" in filename or "mysql_installation" in filename:
        active_markers["active4"] = " active"
    elif "phpmyadmin" in filename:
        active_markers["active5"] = " active"
    elif "creating_databases" in filename and "homework" not in filename:
        active_markers["active6"] = " active"
    elif "homework" in filename:
        active_markers["active7"] = " active"
    
    sidebar_links = sidebar_links.format(**active_markers)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>{lesson_info['title']} - PHP WordPress Course</title>
    <meta name="description" content="{lesson_info['description']}">
    <meta name="keywords" content="PHP, WordPress, MySQL, database, web development">
    <meta name="author" content="PHP WordPress Course">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/main.css">
    
    <!-- Mermaid for diagrams -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <!-- Skip to main content -->
    <a href="#main-content" class="sr-only">Skip to main content</a>
    
    <div class="page-wrapper">
        <!-- Header -->
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
                                    <a href="/module2.html" class="dropdown-item">Module 2: PHP Fundamentals</a>
                                    <a href="/module3.html" class="dropdown-item active">Module 3: MySQL Database</a>
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
        </header>
        
        <!-- Progress Bar -->
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
        </div>
        
        <!-- Breadcrumb -->
        <nav class="breadcrumb container" aria-label="Breadcrumb">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <a href="/module3.html">Module 3</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <li class="breadcrumb-item">
                    <span aria-current="page">{lesson_info['title']}</span>
                </li>
            </ol>
        </nav>
        
        <!-- Main Content -->
        <main id="main-content" class="main-content" role="main">
            <div class="container">
                <div class="content-with-sidebar">
                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 3: Session 1</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Introduction to Databases</h4>
{sidebar_links}
                            </div>
                        </div>
                    </aside>
                    
                    <!-- Main Lesson Content -->
                    <article class="lesson-content">
                        <header class="lesson-header">
                            <h1>{lesson_info['title']}</h1>
                            <div class="lesson-meta">
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <span>Duration: {lesson_info['duration']}</span>
                                </div>
                                <div class="lesson-meta-item">
                                    <svg width="20" height="20" fill="currentColor">
                                        <path d="M12 14l9-5-9-5-9 5 9 5z"/>
                                    </svg>
                                    <span>Module 3: Session 1</span>
                                </div>
                            </div>
                        </header>

                        <!-- Lesson Body -->
                        <div class="lesson-body">
{content}
                        </div>

                        <!-- Lesson Navigation -->
                        <div class="lesson-navigation">
                            <a href="{lesson_info['prev']}" class="lesson-nav-button prev">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                                </svg>
                                <span>
                                    <small>Previous</small><br>
                                    {lesson_info['prev_title']}
                                </span>
                            </a>
                            
                            <button class="complete-lesson-btn">
                                Mark as Complete
                            </button>
                            
                            <a href="{lesson_info['next']}" class="lesson-nav-button next">
                                <span>
                                    <small>Next</small><br>
                                    {lesson_info['next_title']}
                                </span>
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                                </svg>
                            </a>
                        </div>
                    </article>
                </div>
            </div>
        </main>

        <!-- Footer -->
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
                            <li><a href="/module3.html">Module 3</a></li>
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
        </footer>
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

def main():
    """Update Module 3 lesson files with proper structure"""
    print("🚀 Updating Module 3 Lesson Files")
    print("=" * 60)
    
    # Check if module directory exists
    if not MODULE3_DIR.exists():
        print(f"❌ Module 3 directory not found: {MODULE3_DIR}")
        return
    
    # Process each lesson file
    updated = []
    failed = []
    skipped = []
    
    for filename, lesson_info in SESSION1_LESSONS.items():
        filepath = MODULE3_DIR / filename
        
        if not filepath.exists():
            skipped.append(filename)
            print(f"   ⏭️ Skipped: {filename} (file doesn't exist)")
            continue
        
        try:
            print(f"📝 Processing {filename}...")
            
            # Create backup
            backup_path = filepath.with_suffix('.html.backup')
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"   💾 Backup created: {backup_path.name}")
            
            # Extract existing content
            content = extract_lesson_content(filepath)
            if not content:
                failed.append((filename, "Could not extract content"))
                print(f"   ❌ Failed to extract content")
                continue
            
            # Create new file with proper structure
            new_html = create_proper_lesson_file(filename, lesson_info, content)
            
            # Save updated file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            updated.append(filename)
            print(f"   ✅ Updated successfully")
            
        except Exception as e:
            failed.append((filename, str(e)))
            print(f"   ❌ Failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully updated: {len(updated)} files")
    print(f"   ⏭️ Skipped (not found): {len(skipped)} files")
    print(f"   ❌ Failed: {len(failed)} files")
    print(f"   💾 Backups created for all processed files")
    
    if updated:
        print("\n✅ Updated files:")
        for filename in updated:
            print(f"   - {filename}")
    
    if failed:
        print("\n❌ Failed files:")
        for filename, error in failed:
            print(f"   - {filename}: {error}")
    
    if skipped:
        print("\n⏭️ Skipped files:")
        for filename in skipped:
            print(f"   - {filename}")
    
    print("\n🎉 Update complete!")
    print("💡 Backups saved with .backup extension")
    print("📝 Files now match the proper template structure")

if __name__ == "__main__":
    import sys
    
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Script interrupted")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
