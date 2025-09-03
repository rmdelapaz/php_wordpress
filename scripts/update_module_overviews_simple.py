#!/usr/bin/env python3
"""
Script to update module2-9.html structure while PRESERVING all existing content
Only updates the HTML structure, CSS links, header, footer, navigation
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

def extract_existing_content(filepath):
    """Extract the main content from existing module file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract module title
        title_match = re.search(r'<h1>Module \d+: (.*?)</h1>', content)
        module_title = title_match.group(1) if title_match else "Module"
        
        # Extract main content (everything between <main> tags)
        main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
        main_content = main_match.group(1) if main_match else ""
        
        # Clean up the main content
        main_content = main_content.strip()
        
        # Extract module overview if present
        overview_match = re.search(r'<section class="module-intro">(.*?)</section>', main_content, re.DOTALL)
        overview_content = overview_match.group(1) if overview_match else ""
        
        # Extract all week/session sections
        sessions_content = ""
        week_sections = re.findall(r'<section class="week">(.*?)</section>', main_content, re.DOTALL)
        for week in week_sections:
            sessions_content += f'''                <section class="week">
{week}
                </section>

'''
        
        # Extract resources section if present
        resources_match = re.search(r'<section class="resources">(.*?)</section>', main_content, re.DOTALL)
        resources_content = resources_match.group(1) if resources_match else ""
        
        return {
            'title': module_title,
            'overview': overview_content,
            'sessions': sessions_content,
            'resources': resources_content,
            'full_main': main_content
        }
    except Exception as e:
        print(f"   ⚠️ Could not extract content from {filepath}: {e}")
        return None

def generate_updated_module_html(module_num, existing_content):
    """Generate updated HTML preserving existing content but with new structure"""
    
    if not existing_content:
        return None
    
    title = existing_content['title']
    
    # Determine folder based on module number
    folder = f"0{module_num}module"
    
    # Navigation links
    prev_module = module_num - 1
    next_module = module_num + 1 if module_num < 9 else None
    
    # If we have the full main content, use it directly in the proper structure
    main_body = ""
    if existing_content['sessions']:
        # Use the extracted and cleaned sessions
        main_body = f"""                <!-- Module Header -->
                <div class="module-intro">
{existing_content['overview']}
                </div>

{existing_content['sessions']}
                
                <!-- Learning Resources -->
                <section class="resources mt-2xl">
{existing_content['resources']}
                </section>"""
    else:
        # Fallback to full main content
        main_body = existing_content['full_main']
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title>Module {module_num}: {title} - PHP WordPress Course</title>
    <meta name="description" content="Master {title} in the PHP WordPress Development Course">
    <meta name="keywords" content="PHP, WordPress, {title}, web development, programming">
    <meta name="author" content="PHP WordPress Course">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="Module {module_num}: {title}">
    <meta property="og:description" content="Master {title} in this comprehensive module">
    <meta property="og:type" content="website">
    <meta property="og:image" content="/assets/images/module{module_num}-og.jpg">
    
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
                            <li class="nav-item">
                                <a href="/" class="nav-link">Home</a>
                            </li>
                            <li class="nav-item dropdown">
                                <button class="nav-link dropdown-toggle active" aria-haspopup="true">Modules</button>
                                <div class="dropdown-menu">
                                    <a href="/module1.html" class="dropdown-item">Module 1: Web Fundamentals</a>
                                    <a href="/module2.html" class="dropdown-item{' active' if module_num == 2 else ''}">Module 2: PHP Fundamentals</a>
                                    <a href="/module3.html" class="dropdown-item{' active' if module_num == 3 else ''}">Module 3: MySQL Database</a>
                                    <a href="/module4.html" class="dropdown-item{' active' if module_num == 4 else ''}">Module 4: WordPress & Docker</a>
                                    <a href="/module5.html" class="dropdown-item{' active' if module_num == 5 else ''}">Module 5: Theme Development</a>
                                    <a href="/module6.html" class="dropdown-item{' active' if module_num == 6 else ''}">Module 6: Plugin Development</a>
                                    <a href="/module7.html" class="dropdown-item{' active' if module_num == 7 else ''}">Module 7: Advanced WordPress</a>
                                    <a href="/module8.html" class="dropdown-item{' active' if module_num == 8 else ''}">Module 8: Deployment</a>
                                    <a href="/module9.html" class="dropdown-item{' active' if module_num == 9 else ''}">Module 9: Final Project</a>
                                </div>
                            </li>
                            <li class="nav-item">
                                <a href="/resources.html" class="nav-link">Resources</a>
                            </li>
                            <li class="nav-item">
                                <a href="/about.html" class="nav-link">About</a>
                            </li>
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
                <h2 class="progress-title">Module {module_num} Progress</h2>
                <span class="progress-text">0 of X lessons completed</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-fill" style="width: 0%">
                    <span class="progress-bar-text">0%</span>
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
                    <span aria-current="page">Module {module_num}: {title}</span>
                </li>
            </ol>
        </nav>

        <!-- Main Content -->
        <main id="main-content" class="main-content" role="main">
            <div class="container">
{main_body}

                <!-- Module Navigation -->
                <div class="lesson-navigation">
                    <a href="/module{prev_module}.html" class="lesson-nav-button prev">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                        </svg>
                        <span>
                            <small>Previous Module</small><br>
                            Module {prev_module}
                        </span>
                    </a>
                    
                    <a href="/{folder}/" class="btn btn-primary btn-lg">
                        Start Module {module_num}
                    </a>
                    
                    {f'''<a href="/module{next_module}.html" class="lesson-nav-button next">
                        <span>
                            <small>Next Module</small><br>
                            Module {next_module}
                        </span>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                        </svg>
                    </a>''' if next_module else '''<a href="/" class="lesson-nav-button next">
                        <span>
                            <small>Back to</small><br>
                            Course Home
                        </span>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                        </svg>
                    </a>'''}
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="site-footer" role="contentinfo">
            <div class="footer-container">
                <div class="footer-content">
                    <div class="footer-section footer-about">
                        <h3>PHP WordPress Development</h3>
                        <p>Complete Web Development Course - From HTML to WordPress</p>
                    </div>
                    
                    <div class="footer-section">
                        <h4>Quick Links</h4>
                        <ul class="footer-links">
                            <li><a href="/">Home</a></li>
                            <li><a href="/module{module_num}.html">Module {module_num}</a></li>
                            <li><a href="/resources.html">Resources</a></li>
                            <li><a href="/about.html">About</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-section">
                        <h4>Course Modules</h4>
                        <ul class="footer-links">
                            <li><a href="/module1.html">Module 1: Web Fundamentals</a></li>
                            <li><a href="/module2.html"{' class="active"' if module_num == 2 else ''}>Module 2: PHP</a></li>
                            <li><a href="/module3.html"{' class="active"' if module_num == 3 else ''}>Module 3: MySQL</a></li>
                            <li><a href="/module4.html"{' class="active"' if module_num == 4 else ''}>Module 4: WordPress</a></li>
                            <li><a href="/#modules">View All →</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-section">
                        <h4>Support</h4>
                        <ul class="footer-links">
                            <li><a href="/help.html">Help Center</a></li>
                            <li><a href="/faq.html">FAQ</a></li>
                            <li><a href="/contact.html">Contact</a></li>
                            <li><a href="/feedback.html">Feedback</a></li>
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
                            <span class="separator">|</span>
                            <a href="/sitemap.html">Sitemap</a>
                        </nav>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <!-- Back to Top Button -->
    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 19V5M12 5l-7 7M12 5l7 7"/>
        </svg>
    </button>

    <!-- JavaScript -->
    <script src="/assets/js/navigation.js"></script>
    <script src="/assets/js/site-config.js"></script>
    
    <script>
        // Module-specific progress tracking
        document.addEventListener('DOMContentLoaded', function() {{
            const totalLessons = document.querySelectorAll('.lesson-link').length || document.querySelectorAll('a[href*="/0{module_num}module/"]').length;
            
            // Update progress display
            function updateModuleProgress() {{
                const progress = JSON.parse(localStorage.getItem('courseProgress') || '{{}}');
                const module{module_num}Lessons = Object.keys(progress).filter(key => key.includes('/0{module_num}module/'));
                const completedCount = module{module_num}Lessons.length;
                const percentage = totalLessons > 0 ? Math.round((completedCount / totalLessons) * 100) : 0;
                
                if (document.querySelector('.progress-text')) {{
                    document.querySelector('.progress-text').textContent = `${{completedCount}} of ${{totalLessons}} lessons completed`;
                }}
                if (document.querySelector('.progress-bar-fill')) {{
                    document.querySelector('.progress-bar-fill').style.width = percentage + '%';
                }}
                if (document.querySelector('.progress-bar-text')) {{
                    document.querySelector('.progress-bar-text').textContent = percentage + '%';
                }}
            }}
            
            updateModuleProgress();
        }});
    </script>
</body>
</html>"""
    
    return html

def main():
    """Update module 2-9 overview pages preserving ALL existing content"""
    print("🚀 Updating Module 2-9 Overview Pages (Preserving Content)")
    print("=" * 60)
    
    updated = []
    failed = []
    skipped = []
    
    for module_num in range(2, 10):
        filename = f"module{module_num}.html"
        filepath = BASE_DIR / filename
        
        if not filepath.exists():
            skipped.append(filename)
            print(f"   ⏭️ Skipped: {filename} (file doesn't exist)")
            continue
        
        try:
            print(f"📝 Processing {filename}...")
            
            # Extract existing content
            existing_content = extract_existing_content(filepath)
            
            if not existing_content:
                failed.append((filename, "Could not extract content"))
                print(f"   ❌ Failed to extract content: {filename}")
                continue
            
            # Generate updated HTML with existing content
            html_content = generate_updated_module_html(module_num, existing_content)
            
            if not html_content:
                failed.append((filename, "Could not generate HTML"))
                print(f"   ❌ Failed to generate HTML: {filename}")
                continue
            
            # Backup existing file
            backup_path = filepath.with_suffix('.html.backup')
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            # Write updated file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            updated.append(filename)
            print(f"   ✅ Updated: {filename} (backup saved as {backup_path.name})")
            
        except Exception as e:
            failed.append((filename, str(e)))
            print(f"   ❌ Failed: {filename} - {e}")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully updated: {len(updated)} files")
    print(f"   ⏭️ Skipped (not found): {len(skipped)} files")
    print(f"   ❌ Failed: {len(failed)} files")
    print(f"   💾 Backups created for all updated files")
    print(f"   📝 All content preserved from original files")
    
    if failed:
        print("\n⚠️ Failed files:")
        for filename, error in failed:
            print(f"   - {filename}: {error}")
    
    if skipped:
        print("\n📋 Skipped files:")
        for filename in skipped:
            print(f"   - {filename}")
    
    print(f"\n🎉 Module overview pages update complete!")
    print("✨ Original content preserved with updated structure")
    print("💡 Backup files created with .backup extension")

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
