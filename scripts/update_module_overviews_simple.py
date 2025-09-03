#!/usr/bin/env python3
"""
Script to update module2-9.html overview pages to match module1.html structure
Uses a simpler, consistent design based on existing module1.html
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

# Module data - simplified structure matching module1.html style
modules_data = {
    2: {
        "title": "PHP Fundamentals",
        "description": "Master PHP programming from basics to advanced concepts. Learn syntax, functions, OOP, database integration, and build dynamic web applications.",
        "folder": "02module",
        "sessions": [
            {
                "title": "PHP Language Basics",
                "lessons": [
                    "PHP Setup and Syntax",
                    "Variables and Data Types", 
                    "Operators and Expressions",
                    "Control Structures",
                    "Loops in PHP"
                ]
            },
            {
                "title": "Functions and Arrays",
                "lessons": [
                    "Creating Functions",
                    "Function Parameters",
                    "Arrays and Manipulation",
                    "Array Functions",
                    "Multi-dimensional Arrays"
                ]
            },
            {
                "title": "Working with Forms",
                "lessons": [
                    "HTML Forms Review",
                    "Handling Form Data",
                    "Form Validation",
                    "File Uploads",
                    "Sessions and Cookies"
                ]
            },
            {
                "title": "Object-Oriented PHP",
                "lessons": [
                    "Introduction to OOP",
                    "Classes and Objects",
                    "Inheritance",
                    "Interfaces and Abstract Classes",
                    "Traits and Namespaces"
                ]
            },
            {
                "title": "Database Operations",
                "lessons": [
                    "MySQL Connection",
                    "CRUD Operations",
                    "Prepared Statements",
                    "Database Security",
                    "Transactions"
                ]
            }
        ]
    },
    3: {
        "title": "MySQL Database Management",
        "description": "Learn database design, SQL queries, normalization, and how to integrate MySQL with PHP for dynamic web applications.",
        "folder": "03module",
        "sessions": [
            {
                "title": "Database Fundamentals",
                "lessons": [
                    "Introduction to Databases",
                    "MySQL Installation",
                    "Database Design Principles",
                    "Creating Databases and Tables",
                    "Data Types"
                ]
            },
            {
                "title": "SQL Queries",
                "lessons": [
                    "SELECT Statements",
                    "INSERT, UPDATE, DELETE",
                    "WHERE Clauses and Operators",
                    "Sorting and Grouping",
                    "Aggregate Functions"
                ]
            },
            {
                "title": "Advanced SQL",
                "lessons": [
                    "Table Joins",
                    "Subqueries",
                    "Views",
                    "Stored Procedures",
                    "Triggers"
                ]
            },
            {
                "title": "Database Optimization",
                "lessons": [
                    "Indexes",
                    "Query Optimization",
                    "Performance Tuning",
                    "Backup and Recovery",
                    "Security Best Practices"
                ]
            }
        ]
    },
    4: {
        "title": "WordPress & Docker Setup",
        "description": "Set up a professional WordPress development environment using Docker. Understand WordPress architecture and core concepts.",
        "folder": "04module",
        "sessions": [
            {
                "title": "Docker Fundamentals",
                "lessons": [
                    "Introduction to Docker",
                    "Containers and Images",
                    "Docker Compose",
                    "Docker for WordPress",
                    "Managing Containers"
                ]
            },
            {
                "title": "WordPress Setup",
                "lessons": [
                    "WordPress Installation",
                    "Configuration",
                    "File Structure",
                    "Database Structure",
                    "Admin Dashboard"
                ]
            },
            {
                "title": "WordPress Core",
                "lessons": [
                    "The WordPress Loop",
                    "Template Hierarchy",
                    "Hooks and Filters",
                    "WordPress APIs",
                    "WP_Query"
                ]
            },
            {
                "title": "Development Tools",
                "lessons": [
                    "Debugging WordPress",
                    "WP-CLI",
                    "Version Control",
                    "Local Development",
                    "Deployment Basics"
                ]
            }
        ]
    },
    5: {
        "title": "WordPress Theme Development",
        "description": "Create professional WordPress themes from scratch. Master template files, custom post types, and modern theme development.",
        "folder": "05module",
        "sessions": [
            {
                "title": "Theme Basics",
                "lessons": [
                    "Theme Structure",
                    "Template Files",
                    "Functions.php",
                    "Style.css",
                    "Screenshot and Headers"
                ]
            },
            {
                "title": "Template Development",
                "lessons": [
                    "Header and Footer",
                    "Single and Page Templates",
                    "Archive Templates",
                    "Custom Page Templates",
                    "Template Parts"
                ]
            },
            {
                "title": "Theme Features",
                "lessons": [
                    "Menus and Navigation",
                    "Sidebars and Widgets",
                    "Featured Images",
                    "Comments Template",
                    "Search Functionality"
                ]
            },
            {
                "title": "Advanced Theming",
                "lessons": [
                    "Custom Post Types",
                    "Custom Taxonomies",
                    "Theme Customizer",
                    "Custom Fields",
                    "WooCommerce Support"
                ]
            },
            {
                "title": "Theme Optimization",
                "lessons": [
                    "Responsive Design",
                    "Performance Optimization",
                    "SEO Best Practices",
                    "Accessibility",
                    "Theme Testing"
                ]
            }
        ]
    },
    6: {
        "title": "WordPress Plugin Development",
        "description": "Build custom WordPress plugins to extend functionality. Learn hooks, database operations, admin pages, and security.",
        "folder": "06module",
        "sessions": [
            {
                "title": "Plugin Fundamentals",
                "lessons": [
                    "Plugin Structure",
                    "Headers and Activation",
                    "Hooks and Filters",
                    "Actions vs Filters",
                    "Plugin Security"
                ]
            },
            {
                "title": "Plugin Features",
                "lessons": [
                    "Admin Menu Pages",
                    "Settings API",
                    "Options API",
                    "Custom Database Tables",
                    "Shortcodes"
                ]
            },
            {
                "title": "Advanced Plugin Development",
                "lessons": [
                    "AJAX in Plugins",
                    "REST API Integration",
                    "Custom Widgets",
                    "Gutenberg Blocks",
                    "Plugin Localization"
                ]
            },
            {
                "title": "Plugin Best Practices",
                "lessons": [
                    "Object-Oriented Plugins",
                    "Plugin Testing",
                    "Documentation",
                    "Distribution",
                    "Updates and Versioning"
                ]
            }
        ]
    },
    7: {
        "title": "Advanced WordPress Development",
        "description": "Master REST API, Gutenberg blocks, React integration, and modern WordPress development techniques.",
        "folder": "07module",
        "sessions": [
            {
                "title": "WordPress REST API",
                "lessons": [
                    "REST API Basics",
                    "Custom Endpoints",
                    "Authentication",
                    "CRUD Operations",
                    "API Security"
                ]
            },
            {
                "title": "Gutenberg Development",
                "lessons": [
                    "Block Editor Overview",
                    "Creating Custom Blocks",
                    "Block Attributes",
                    "Dynamic Blocks",
                    "Block Patterns"
                ]
            },
            {
                "title": "React and WordPress",
                "lessons": [
                    "React Fundamentals",
                    "JSX and Components",
                    "State Management",
                    "React in WordPress",
                    "Building Admin Interfaces"
                ]
            },
            {
                "title": "Modern WordPress",
                "lessons": [
                    "Headless WordPress",
                    "JAMstack Integration",
                    "GraphQL and WordPress",
                    "Progressive Web Apps",
                    "Performance Optimization"
                ]
            }
        ]
    },
    8: {
        "title": "Deployment & DevOps",
        "description": "Learn professional WordPress deployment, hosting, security, performance optimization, and maintenance strategies.",
        "folder": "08module",
        "sessions": [
            {
                "title": "Hosting and Servers",
                "lessons": [
                    "Hosting Options",
                    "Server Requirements",
                    "SSL Certificates",
                    "Domain Configuration",
                    "Email Setup"
                ]
            },
            {
                "title": "Deployment",
                "lessons": [
                    "Git Workflows",
                    "CI/CD Pipelines",
                    "Automated Testing",
                    "Staging Environments",
                    "Production Deployment"
                ]
            },
            {
                "title": "Security and Performance",
                "lessons": [
                    "Security Hardening",
                    "Firewall Configuration",
                    "Caching Strategies",
                    "CDN Integration",
                    "Database Optimization"
                ]
            },
            {
                "title": "Maintenance",
                "lessons": [
                    "Backup Strategies",
                    "Update Management",
                    "Monitoring",
                    "Error Tracking",
                    "Disaster Recovery"
                ]
            }
        ]
    },
    9: {
        "title": "Final Project",
        "description": "Apply everything you've learned by building a complete WordPress project from planning to deployment.",
        "folder": "09module",
        "sessions": [
            {
                "title": "Project Planning",
                "lessons": [
                    "Requirements Analysis",
                    "Project Scope",
                    "Technical Architecture",
                    "Timeline and Milestones",
                    "Resource Planning"
                ]
            },
            {
                "title": "Design and Development",
                "lessons": [
                    "Wireframing",
                    "Design Mockups",
                    "Database Design",
                    "Theme Development",
                    "Plugin Development"
                ]
            },
            {
                "title": "Implementation",
                "lessons": [
                    "Content Strategy",
                    "E-commerce Integration",
                    "User Management",
                    "SEO Implementation",
                    "Performance Optimization"
                ]
            },
            {
                "title": "Launch and Documentation",
                "lessons": [
                    "Testing and QA",
                    "Deployment Process",
                    "User Documentation",
                    "Developer Documentation",
                    "Project Handoff"
                ]
            }
        ]
    }
}

def generate_module_overview_html(module_num, data):
    """Generate HTML for a module overview page matching module1.html style"""
    
    # Generate session cards HTML
    sessions_html = ""
    for i, session in enumerate(data["sessions"], 1):
        lessons_list = "\n".join([f'<li>{lesson}</li>' for lesson in session["lessons"]])
        sessions_html += f"""
            <div class="module-session">
                <h3>Session {i}: {session["title"]}</h3>
                <ul>
                    {lessons_list}
                </ul>
            </div>"""
    
    # Determine navigation
    prev_link = f'<a href="/module{module_num-1}.html" class="btn btn-outline">← Previous Module</a>' if module_num > 1 else ''
    next_link = f'<a href="/module{module_num+1}.html" class="btn btn-outline">Next Module →</a>' if module_num < 9 else ''
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Module {module_num}: {data['title']} - PHP WordPress Course</title>
    <meta name="description" content="{data['description']}">
    <link rel="stylesheet" href="/assets/css/style.css">
    <style>
        .module-overview {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .module-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .module-header h1 {{
            margin: 0 0 1rem 0;
            font-size: 2.5rem;
        }}
        .module-description {{
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
        }}
        .module-meta {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }}
        .module-meta span {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .module-content {{
            display: grid;
            gap: 2rem;
        }}
        .module-session {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .module-session h3 {{
            margin: 0 0 1rem 0;
            color: #1f2937;
            font-size: 1.3rem;
        }}
        .module-session ul {{
            margin: 0;
            padding-left: 1.5rem;
        }}
        .module-session li {{
            padding: 0.25rem 0;
            color: #4b5563;
        }}
        .module-navigation {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e5e7eb;
        }}
        .start-module-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin: 2rem 0;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        .start-module-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        .btn-outline {{
            border: 2px solid #667eea;
            color: #667eea;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }}
        .btn-outline:hover {{
            background: #667eea;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="module-overview">
        <div class="module-header">
            <h1>Module {module_num}: {data['title']}</h1>
            <p class="module-description">{data['description']}</p>
            <div class="module-meta">
                <span>📚 {len(data['sessions'])} Sessions</span>
                <span>📝 {sum(len(s['lessons']) for s in data['sessions'])} Lessons</span>
                <span>📁 /{data['folder']}/</span>
            </div>
        </div>

        <div class="module-content">
            <h2>Course Content</h2>
            {sessions_html}
        </div>

        <div style="text-align: center;">
            <a href="/{data['folder']}/" class="start-module-btn">Start Module {module_num}</a>
        </div>

        <div class="module-navigation">
            {prev_link}
            <a href="/" class="btn btn-outline">Back to Home</a>
            {next_link}
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    """Update module 2-9 overview pages"""
    print("🚀 Updating Module 2-9 Overview Pages")
    print("=" * 60)
    
    updated = []
    failed = []
    
    for module_num, data in modules_data.items():
        filename = f"module{module_num}.html"
        filepath = BASE_DIR / filename
        
        try:
            print(f"📝 Updating {filename}...")
            html_content = generate_module_overview_html(module_num, data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated.append(filename)
            print(f"   ✅ Updated: {filename}")
            
        except Exception as e:
            failed.append((filename, str(e)))
            print(f"   ❌ Failed: {filename} - {e}")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully updated: {len(updated)} files")
    print(f"   ❌ Failed: {len(failed)} files")
    
    if failed:
        print("\n⚠️ Failed files:")
        for filename, error in failed:
            print(f"   - {filename}: {error}")
    
    print(f"\n🎉 Module overview pages update complete!")
    print("📅 All modules now have consistent structure matching module1.html")

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
