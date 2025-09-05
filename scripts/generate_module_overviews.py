#!/usr/bin/env python3
"""
Script to update all module overview pages (module1-9.html) with consistent modern design
"""

import os
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

# Module data structure
modules_data = {
    1: {
        "title": "Web Development Fundamentals",
        "subtitle": "HTML, CSS, JavaScript & Introduction to PHP",
        "description": "Start your journey into web development with the foundational technologies. Learn HTML for structure, CSS for styling, JavaScript for interactivity, and get introduced to PHP.",
        "duration": "10 Sessions",
        "lessons": 57,
        "color_primary": "#667eea",
        "color_secondary": "#764ba2",
        "topics": [
            ("Introduction to Web Development", "How the web works, development environment setup"),
            ("HTML Fundamentals", "HTML structure, tags, forms, and best practices"),
            ("CSS Basics", "Styling, selectors, box model, and layouts"),
            ("Responsive Design", "Mobile-first approach, media queries, flexbox, and grid"),
            ("CSS Frameworks", "Bootstrap, utility classes, and CSS preprocessors"),
            ("JavaScript Fundamentals", "Variables, functions, control flow, and scope"),
            ("DOM Manipulation", "Selecting elements, events, and dynamic content"),
            ("jQuery & Modern JS", "jQuery basics, ES6+, AJAX"),
            ("Introduction to PHP", "PHP basics, syntax, and server setup"),
            ("Mini-Project", "Build a complete 5-page static website")
        ],
        "skills": [
            "HTML5 & Semantic Markup",
            "CSS3 & Modern Layouts",
            "Responsive Web Design",
            "JavaScript Programming",
            "jQuery Library",
            "Basic PHP Syntax",
            "Git Version Control",
            "Web Development Tools"
        ],
        "projects": [
            "Personal Portfolio Website",
            "Responsive Landing Page",
            "Interactive JavaScript Apps",
            "Bootstrap Website",
            "Static Multi-page Site"
        ]
    },
    2: {
        "title": "PHP Fundamentals",
        "subtitle": "Master Server-Side Programming with PHP",
        "description": "Deep dive into PHP programming. Learn everything from basic syntax to advanced object-oriented programming, database integration, and security best practices.",
        "duration": "17 Topics",
        "lessons": 122,
        "color_primary": "#8b5cf6",
        "color_secondary": "#ec4899",
        "topics": [
            ("PHP Basics & Setup", "Installation, syntax, variables, and data types"),
            ("Operators & Control Structures", "All operators, conditionals, and loops"),
            ("Functions", "Creating functions, scope, parameters, and closures"),
            ("Arrays & Data Manipulation", "Indexed, associative, multidimensional arrays"),
            ("Working with Forms", "Form handling, validation, and file uploads"),
            ("Sessions & Cookies", "User sessions, cookies, and state management"),
            ("Object-Oriented PHP", "Classes, objects, inheritance, interfaces"),
            ("Database Operations", "MySQL, PDO, CRUD operations, prepared statements"),
            ("APIs & Web Services", "JSON, REST APIs, creating endpoints"),
            ("Security & Testing", "Security practices, debugging, unit testing")
        ],
        "skills": [
            "PHP Programming",
            "Object-Oriented PHP",
            "Database Integration",
            "Form Processing",
            "API Development",
            "Security Best Practices",
            "Error Handling",
            "Testing & Debugging"
        ],
        "projects": [
            "PHP Calculator",
            "Contact Form System",
            "User Management System",
            "Weather App with API",
            "Blog CMS"
        ]
    },
    3: {
        "title": "MySQL Database Management",
        "subtitle": "Master Database Design and SQL",
        "description": "Learn professional database management with MySQL. Cover everything from basic SQL queries to advanced database design, optimization, and integration with PHP.",
        "duration": "8 Sessions",
        "lessons": 45,
        "color_primary": "#f97316",
        "color_secondary": "#ea580c",
        "topics": [
            ("Database Fundamentals", "RDBMS concepts, MySQL setup, and tools"),
            ("SQL Basics", "SELECT, INSERT, UPDATE, DELETE operations"),
            ("Database Design", "Normalization, relationships, and ER diagrams"),
            ("Advanced SQL", "Joins, subqueries, views, and stored procedures"),
            ("Indexes & Optimization", "Query optimization, indexes, and performance"),
            ("Transactions & Security", "ACID properties, transactions, user privileges"),
            ("PHP Integration", "PDO, MySQLi, prepared statements"),
            ("Database Project", "Design and implement a complete database system")
        ],
        "skills": [
            "SQL Query Writing",
            "Database Design",
            "Normalization",
            "Query Optimization",
            "Stored Procedures",
            "Database Security",
            "Backup & Recovery",
            "PHP Integration"
        ],
        "projects": [
            "E-commerce Database",
            "Library Management System",
            "Social Media Database",
            "Inventory System",
            "Analytics Dashboard"
        ]
    },
    4: {
        "title": "WordPress & Docker Setup",
        "subtitle": "Professional WordPress Development Environment",
        "description": "Set up a professional WordPress development environment using Docker. Understand WordPress architecture, core concepts, and development workflow.",
        "duration": "6 Sessions",
        "lessons": 35,
        "color_primary": "#0891b2",
        "color_secondary": "#0e7490",
        "topics": [
            ("Docker Fundamentals", "Containers, images, Docker Compose"),
            ("WordPress Installation", "Setup, configuration, and administration"),
            ("WordPress Architecture", "File structure, database, and core files"),
            ("The WordPress Loop", "Template hierarchy and content display"),
            ("WordPress APIs", "Options, Settings, Metadata APIs"),
            ("Development Tools", "Debugging, WP-CLI, version control"),
            ("Security Basics", "Hardening WordPress, security plugins"),
            ("Performance", "Caching, optimization, and best practices")
        ],
        "skills": [
            "Docker & Containerization",
            "WordPress Installation",
            "WordPress Configuration",
            "Development Workflow",
            "Debugging Tools",
            "Version Control",
            "Security Hardening",
            "Performance Tuning"
        ],
        "projects": [
            "Local Development Setup",
            "Multi-site Installation",
            "Staging Environment",
            "Automated Backup System",
            "Security Audit"
        ]
    },
    5: {
        "title": "WordPress Theme Development",
        "subtitle": "Create Professional Custom Themes",
        "description": "Master WordPress theme development from scratch. Learn template hierarchy, custom post types, theme customization, and modern development practices.",
        "duration": "10 Sessions",
        "lessons": 52,
        "color_primary": "#10b981",
        "color_secondary": "#059669",
        "topics": [
            ("Theme Structure", "Template files, functions.php, style.css"),
            ("Template Hierarchy", "Page templates, post formats, archives"),
            ("The Loop & WP_Query", "Custom queries, pagination, filtering"),
            ("Custom Post Types & Taxonomies", "Creating custom content types"),
            ("Menus & Widgets", "Navigation menus, widget areas, custom widgets"),
            ("Theme Customizer", "Live preview, custom controls, selective refresh"),
            ("Advanced Custom Fields", "ACF integration, flexible content"),
            ("WooCommerce Integration", "E-commerce theme development"),
            ("Responsive Themes", "Mobile-first, accessibility, performance"),
            ("Theme Deployment", "Child themes, updates, distribution")
        ],
        "skills": [
            "Theme Architecture",
            "Template Development",
            "Custom Post Types",
            "Theme Customizer API",
            "WooCommerce Themes",
            "Responsive Design",
            "Theme Security",
            "Performance Optimization"
        ],
        "projects": [
            "Blog Theme",
            "Business Theme",
            "Portfolio Theme",
            "E-commerce Theme",
            "Magazine Theme"
        ]
    },
    6: {
        "title": "WordPress Plugin Development",
        "subtitle": "Extend WordPress with Custom Plugins",
        "description": "Learn to build WordPress plugins from simple to complex. Master hooks, filters, database operations, admin interfaces, and plugin security.",
        "duration": "8 Sessions",
        "lessons": 48,
        "color_primary": "#dc2626",
        "color_secondary": "#b91c1c",
        "topics": [
            ("Plugin Architecture", "Structure, headers, activation/deactivation"),
            ("Hooks & Filters", "Actions, filters, custom hooks, priorities"),
            ("Database Operations", "Custom tables, queries, migrations"),
            ("Admin Interfaces", "Settings pages, custom menus, options API"),
            ("Shortcodes & Widgets", "Creating shortcodes, custom widgets"),
            ("AJAX in Plugins", "Admin AJAX, frontend AJAX, REST API"),
            ("Plugin Security", "Nonces, capabilities, data validation"),
            ("OOP Plugin Development", "Classes, namespaces, autoloading"),
            ("Testing & Debugging", "Unit tests, integration tests, debugging"),
            ("Distribution", "WordPress.org repository, licensing, updates")
        ],
        "skills": [
            "Plugin Architecture",
            "WordPress Hooks",
            "Database Management",
            "Admin UI Development",
            "AJAX Implementation",
            "Security Practices",
            "OOP in WordPress",
            "Plugin Distribution"
        ],
        "projects": [
            "Contact Form Plugin",
            "Custom Post Type Plugin",
            "Social Share Plugin",
            "Backup Plugin",
            "SEO Plugin"
        ]
    },
    7: {
        "title": "Advanced WordPress Development",
        "subtitle": "REST API, Gutenberg & Modern WordPress",
        "description": "Master advanced WordPress features including REST API development, Gutenberg block creation, React integration, and headless WordPress.",
        "duration": "7 Sessions",
        "lessons": 42,
        "color_primary": "#7c3aed",
        "color_secondary": "#6d28d9",
        "topics": [
            ("WordPress REST API", "Endpoints, authentication, custom routes"),
            ("Gutenberg Blocks", "Block development, Block API, patterns"),
            ("React for WordPress", "React basics, JSX, components, state"),
            ("Dynamic Blocks", "Server-side rendering, attributes, controls"),
            ("Block Patterns & Styles", "Reusable patterns, block styles, variations"),
            ("Headless WordPress", "Decoupled architecture, JAMstack"),
            ("GraphQL", "WPGraphQL, queries, mutations"),
            ("Performance", "Caching, CDN, lazy loading, optimization"),
            ("Multisite", "Network setup, management, development"),
            ("Enterprise WordPress", "Scaling, security, deployment strategies")
        ],
        "skills": [
            "REST API Development",
            "Gutenberg Development",
            "React.js",
            "Headless CMS",
            "GraphQL",
            "Performance Tuning",
            "Multisite Management",
            "Enterprise Solutions"
        ],
        "projects": [
            "Custom Gutenberg Blocks",
            "REST API Application",
            "Headless Blog",
            "Block Pattern Library",
            "React Dashboard"
        ]
    },
    8: {
        "title": "Deployment & DevOps",
        "subtitle": "Professional WordPress Hosting & Deployment",
        "description": "Learn to deploy WordPress professionally. Cover hosting options, server management, CI/CD pipelines, monitoring, and maintenance strategies.",
        "duration": "5 Sessions",
        "lessons": 30,
        "color_primary": "#0ea5e9",
        "color_secondary": "#0284c7",
        "topics": [
            ("Hosting Options", "Shared, VPS, dedicated, managed WordPress"),
            ("Server Setup", "Linux, Apache/Nginx, PHP, MySQL configuration"),
            ("SSL & Security", "SSL certificates, firewalls, security headers"),
            ("Performance", "Caching strategies, CDN setup, optimization"),
            ("CI/CD Pipelines", "Git workflows, automated testing, deployment"),
            ("Backup & Recovery", "Backup strategies, disaster recovery"),
            ("Monitoring", "Uptime, performance, error tracking, analytics"),
            ("Maintenance", "Updates, security patches, database optimization"),
            ("Scaling", "Load balancing, database replication, caching"),
            ("Migration", "Site migration, domain transfer, data migration")
        ],
        "skills": [
            "Server Management",
            "DevOps Practices",
            "CI/CD Implementation",
            "Security Hardening",
            "Performance Optimization",
            "Backup Strategies",
            "Monitoring Setup",
            "Scaling Applications"
        ],
        "projects": [
            "Production Deployment",
            "CI/CD Pipeline",
            "Monitoring Dashboard",
            "Backup System",
            "Load Testing"
        ]
    },
    9: {
        "title": "Final Project",
        "subtitle": "Build a Complete WordPress Application",
        "description": "Apply everything you've learned by building a complete, production-ready WordPress application from concept to deployment.",
        "duration": "Capstone Project",
        "lessons": 25,
        "color_primary": "#f59e0b",
        "color_secondary": "#d97706",
        "topics": [
            ("Project Planning", "Requirements, scope, timeline, architecture"),
            ("Design Phase", "Wireframes, mockups, user experience"),
            ("Database Design", "Schema design, relationships, optimization"),
            ("Theme Development", "Custom theme from scratch"),
            ("Plugin Development", "Custom functionality plugins"),
            ("Content Strategy", "Content types, taxonomies, workflows"),
            ("E-commerce Integration", "WooCommerce setup and customization"),
            ("Testing", "Unit tests, integration tests, user testing"),
            ("Deployment", "Production setup, launch checklist"),
            ("Documentation", "User docs, developer docs, maintenance guide")
        ],
        "skills": [
            "Project Management",
            "Full-Stack Development",
            "System Architecture",
            "Quality Assurance",
            "Documentation",
            "Client Communication",
            "Problem Solving",
            "Professional Delivery"
        ],
        "projects": [
            "Complete WordPress Site",
            "Custom Theme",
            "Custom Plugins",
            "E-commerce Solution",
            "Full Documentation"
        ]
    }
}

def generate_module_html(module_num, data):
    """Generate HTML for a module overview page"""
    
    # Generate session/topic cards
    topic_cards = ""
    for i, (topic_title, topic_desc) in enumerate(data["topics"], 1):
        topic_cards += f"""
                <div class="session-card">
                    <div class="session-number">Session {i}</div>
                    <h3 class="session-title">{topic_title}</h3>
                    <p class="session-description">{topic_desc}</p>
                    <a href="/0{module_num}module/" class="session-link">
                        View Lessons
                        <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                        </svg>
                    </a>
                </div>"""
    
    # Generate skills badges
    skills_html = ""
    for skill in data["skills"]:
        skills_html += f"""<span class="skill-badge">{skill}</span>
                        """
    
    # Generate project list
    projects_html = ""
    for project in data["projects"]:
        projects_html += f"""<li class="project-item">
                                <svg width="20" height="20" fill="currentColor" class="project-icon">
                                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                                    <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 1 1 0 000 2H6a2 2 0 00-2 2v6a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-1a1 1 0 100-2h1a4 4 0 014 4v6a4 4 0 01-4 4H6a4 4 0 01-4-4V7a4 4 0 014-4z" clip-rule="evenodd"/>
                                </svg>
                                {project}
                            </li>
                            """
    
    # Navigation links
    prev_module = module_num - 1 if module_num > 1 else None
    next_module = module_num + 1 if module_num < 9 else None
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>Module {module_num}: {data['title']} - PHP WordPress Course</title>
    <meta name="description" content="{data['description']}">
    <meta name="keywords" content="PHP, WordPress, {data['title']}, web development, programming">
    <meta name="author" content="PHP WordPress Course">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Module {module_num}: {data['title']}">
    <meta property="og:description" content="{data['description']}">
    <meta property="og:type" content="website">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/main.css">
    
    <!-- Module-specific styles -->
    <style>
        /* Module Hero Section */
        .module-hero {{
            background: linear-gradient(135deg, {data['color_primary']} 0%, {data['color_secondary']} 100%);
            color: white;
            padding: 80px 0 60px;
            position: relative;
            overflow: hidden;
        }}
        
        .module-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -50%;
            width: 200%;
            height: 100%;
            background: url('/assets/images/pattern.svg') repeat;
            opacity: 0.1;
            animation: float 20s infinite linear;
        }}
        
        @keyframes float {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(25%); }}
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .module-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 1rem;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .module-title {{
            font-size: 3rem;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .module-subtitle {{
            font-size: 1.5rem;
            opacity: 0.95;
            margin-bottom: 25px;
        }}
        
        .module-meta {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 30px;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1.1rem;
        }}
        
        .meta-item svg {{
            width: 24px;
            height: 24px;
            opacity: 0.9;
        }}
        
        /* Module Stats */
        .module-stats {{
            background: white;
            padding: 40px 0;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .stats-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            text-align: center;
        }}
        
        .stat {{
            padding: 20px;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {data['color_primary']};
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #6b7280;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Module Content */
        .module-content {{
            padding: 60px 0;
            background: #f9fafb;
        }}
        
        .content-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .content-header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .content-title {{
            font-size: 2rem;
            margin-bottom: 15px;
            color: #1f2937;
        }}
        
        .content-description {{
            font-size: 1.1rem;
            color: #6b7280;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        /* Sessions Grid */
        .sessions-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 60px;
        }}
        
        .session-card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 1px solid #e5e7eb;
        }}
        
        .session-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border-color: {data['color_primary']};
        }}
        
        .session-number {{
            display: inline-block;
            background: {data['color_primary']}15;
            color: {data['color_primary']};
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .session-title {{
            font-size: 1.25rem;
            margin-bottom: 10px;
            color: #1f2937;
        }}
        
        .session-description {{
            color: #6b7280;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        
        .session-link {{
            display: inline-flex;
            align-items: center;
            color: {data['color_primary']};
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .session-link:hover {{
            gap: 5px;
            color: {data['color_secondary']};
        }}
        
        /* Skills Section */
        .skills-section {{
            background: white;
            padding: 60px 0;
        }}
        
        .skills-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .skills-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin-top: 30px;
        }}
        
        .skill-badge {{
            background: {data['color_primary']}10;
            color: {data['color_primary']};
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.95rem;
            font-weight: 500;
            border: 1px solid {data['color_primary']}30;
            transition: all 0.3s ease;
        }}
        
        .skill-badge:hover {{
            background: {data['color_primary']};
            color: white;
            transform: translateY(-2px);
        }}
        
        /* Projects Section */
        .projects-section {{
            background: #f9fafb;
            padding: 60px 0;
        }}
        
        .projects-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .projects-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .project-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }}
        
        .project-item:hover {{
            border-color: {data['color_primary']};
            transform: translateX(5px);
        }}
        
        .project-icon {{
            color: {data['color_primary']};
            flex-shrink: 0;
        }}
        
        /* Navigation */
        .module-navigation {{
            background: white;
            padding: 40px 0;
            border-top: 1px solid #e5e7eb;
        }}
        
        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-button {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 24px;
            background: #f3f4f6;
            color: #374151;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        
        .nav-button:hover {{
            background: {data['color_primary']};
            color: white;
            transform: translateY(-2px);
        }}
        
        .nav-button.next {{
            flex-direction: row-reverse;
        }}
        
        .start-module-btn {{
            padding: 15px 40px;
            background: {data['color_primary']};
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            display: inline-block;
        }}
        
        .start-module-btn:hover {{
            background: {data['color_secondary']};
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .module-title {{
                font-size: 2rem;
            }}
            
            .module-subtitle {{
                font-size: 1.2rem;
            }}
            
            .sessions-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav-container {{
                flex-direction: column;
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
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
                                <a href="/module1.html" class="dropdown-item {'active' if module_num == 1 else ''}">Module 1: Web Fundamentals</a>
                                <a href="/module2.html" class="dropdown-item {'active' if module_num == 2 else ''}">Module 2: PHP Fundamentals</a>
                                <a href="/module3.html" class="dropdown-item {'active' if module_num == 3 else ''}">Module 3: MySQL Database</a>
                                <a href="/module4.html" class="dropdown-item {'active' if module_num == 4 else ''}">Module 4: WordPress & Docker</a>
                                <a href="/module5.html" class="dropdown-item {'active' if module_num == 5 else ''}">Module 5: Theme Development</a>
                                <a href="/module6.html" class="dropdown-item {'active' if module_num == 6 else ''}">Module 6: Plugin Development</a>
                                <a href="/module7.html" class="dropdown-item {'active' if module_num == 7 else ''}">Module 7: Advanced WordPress</a>
                                <a href="/module8.html" class="dropdown-item {'active' if module_num == 8 else ''}">Module 8: Deployment</a>
                                <a href="/module9.html" class="dropdown-item {'active' if module_num == 9 else ''}">Module 9: Final Project</a>
                            </div>
                        </li>
                        <li class="nav-item"><a href="/resources.html" class="nav-link">Resources</a></li>
                        <li class="nav-item"><a href="/about.html" class="nav-link">About</a></li>
                    </ul>
                </div>
            </nav>
        </div>
    </header>

    <!-- Module Hero -->
    <section class="module-hero">
        <div class="hero-content">
            <div class="module-badge">Module {module_num}</div>
            <h1 class="module-title">{data['title']}</h1>
            <p class="module-subtitle">{data['subtitle']}</p>
            <div class="module-meta">
                <div class="meta-item">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z"/>
                    </svg>
                    <span>{data['lessons']} Lessons</span>
                </div>
                <div class="meta-item">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                    </svg>
                    <span>{data['duration']}</span>
                </div>
                <div class="meta-item">
                    <svg fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                    </svg>
                    <span>{len(data['projects'])} Projects</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Module Stats -->
    <section class="module-stats">
        <div class="stats-container">
            <div class="stat">
                <div class="stat-number">{len(data['topics'])}</div>
                <div class="stat-label">Topics</div>
            </div>
            <div class="stat">
                <div class="stat-number">{data['lessons']}</div>
                <div class="stat-label">Lessons</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(data['skills'])}</div>
                <div class="stat-label">Skills</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(data['projects'])}</div>
                <div class="stat-label">Projects</div>
            </div>
        </div>
    </section>

    <!-- Module Content -->
    <section class="module-content">
        <div class="content-container">
            <div class="content-header">
                <h2 class="content-title">What You'll Learn</h2>
                <p class="content-description">{data['description']}</p>
            </div>
            
            <div class="sessions-grid">
                {topic_cards}
            </div>
            
            <div style="text-align: center;">
                <a href="/0{module_num}module/" class="start-module-btn">Start Learning Module {module_num}</a>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section class="skills-section">
        <div class="skills-container">
            <div class="content-header">
                <h2 class="content-title">Skills You'll Gain</h2>
                <p class="content-description">Master these essential skills through hands-on practice and real projects</p>
            </div>
            
            <div class="skills-grid">
                {skills_html}
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section class="projects-section">
        <div class="projects-container">
            <div class="content-header">
                <h2 class="content-title">Projects You'll Build</h2>
                <p class="content-description">Apply your knowledge by building real-world projects</p>
            </div>
            
            <ul class="projects-list">
                {projects_html}
            </ul>
        </div>
    </section>

    <!-- Navigation -->
    <section class="module-navigation">
        <div class="nav-container">
            {f'''<a href="/module{prev_module}.html" class="nav-button prev">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                </svg>
                <span>Module {prev_module}</span>
            </a>''' if prev_module else '<div></div>'}
            
            <a href="/0{module_num}module/" class="start-module-btn">Start Module {module_num}</a>
            
            {f'''<a href="/module{next_module}.html" class="nav-button next">
                <span>Module {next_module}</span>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                </svg>
            </a>''' if next_module else '<div></div>'}
        </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer" role="contentinfo">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section footer-about">
                    <h3>PHP WordPress Development</h3>
                    <p>Your path to becoming a professional WordPress developer.</p>
                </div>
                
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul class="footer-links">
                        <li><a href="/">Home</a></li>
                        <li><a href="/module1.html">Start Course</a></li>
                        <li><a href="/resources.html">Resources</a></li>
                        <li><a href="/about.html">About</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Modules</h4>
                    <ul class="footer-links">
                        <li><a href="/module1.html">Web Fundamentals</a></li>
                        <li><a href="/module2.html">PHP Programming</a></li>
                        <li><a href="/module5.html">Theme Development</a></li>
                        <li><a href="/module6.html">Plugin Development</a></li>
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
                    <p class="copyright">&copy; 2025 PHP WordPress Development Course. All rights reserved.</p>
                    <nav class="footer-bottom-links">
                        <a href="/privacy.html">Privacy Policy</a>
                        <span class="separator">|</span>
                        <a href="/terms.html">Terms of Service</a>
                    </nav>
                </div>
            </div>
        </div>
    </footer>

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
    """Generate all module overview pages"""
    print("🚀 Generating Module Overview Pages")
    print("=" * 60)
    
    updated = []
    failed = []
    
    for module_num, data in modules_data.items():
        filename = f"module{module_num}.html"
        filepath = BASE_DIR / filename
        
        try:
            print(f"📝 Generating {filename}...")
            html_content = generate_module_html(module_num, data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated.append(filename)
            print(f"   ✅ Created: {filename}")
            
        except Exception as e:
            failed.append((filename, str(e)))
            print(f"   ❌ Failed: {filename} - {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully created: {len(updated)} files")
    print(f"   ❌ Failed: {len(failed)} files")
    
    if failed:
        print("\n⚠️ Failed files:")
        for filename, error in failed:
            print(f"   - {filename}: {error}")
    
    print(f"\n🎉 Module overview pages generation complete!")
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create report
    report_path = BASE_DIR / f"module_pages_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module Overview Pages Generation Report
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Modules:** 9
- **Successfully Created:** {len(updated)}
- **Failed:** {len(failed)}

## Files Created
{chr(10).join(f"- ✅ {f}" for f in updated)}

## Module Details
1. **Web Fundamentals** - 57 lessons, 10 sessions
2. **PHP Fundamentals** - 122 lessons, 17 topics  
3. **MySQL Database** - 45 lessons, 8 sessions
4. **WordPress & Docker** - 35 lessons, 6 sessions
5. **Theme Development** - 52 lessons, 10 sessions
6. **Plugin Development** - 48 lessons, 8 sessions
7. **Advanced WordPress** - 42 lessons, 7 sessions
8. **Deployment & DevOps** - 30 lessons, 5 sessions
9. **Final Project** - 25 lessons, Capstone

## Features
- Unique color schemes per module
- Complete topic breakdowns
- Skills and projects listings
- Responsive design
- Consistent navigation
- Modern, professional layout

**Status:** {"✅ Complete" if not failed else "⚠️ Review needed"}
""")
    
    print(f"\n📝 Report saved to: {report_path}")

if __name__ == "__main__":
    import sys
    
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Script interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
