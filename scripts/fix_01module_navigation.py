#!/usr/bin/env python3
"""
Script to fix the side navigation in 01module HTML files to match the consistent
functionality found in 02module and 03module files.
"""

import os
import re
from bs4 import BeautifulSoup
import sys

def get_session_lessons(session_number):
    """Get all lessons for a specific session."""
    session_lessons = {
        1: [
            {'file': '/01module/course_introduction.html', 'title': 'Course Introduction'},
            {'file': '/01module/how_web_works.html', 'title': 'How the Web Works'},
            {'file': '/01module/development_environment.html', 'title': 'Development Environment'},
            {'file': '/01module/first_html_page.html', 'title': 'Your First HTML Page'},
            {'file': '/01module/homework_setup.html', 'title': 'Homework: Setup'},
        ],
        2: [
            {'file': '/01module/html_structure_syntax.html', 'title': 'HTML Structure & Syntax'},
            {'file': '/01module/essential_html_tags.html', 'title': 'Essential HTML Tags'},
            {'file': '/01module/html_forms_inputs.html', 'title': 'HTML Forms & Inputs'},
            {'file': '/01module/html_validation_practices.html', 'title': 'HTML Validation'},
            {'file': '/01module/homework_html_profile.html', 'title': 'Homework: HTML Profile'},
        ],
        3: [
            {'file': '/01module/introduction_to_css.html', 'title': 'Introduction to CSS'},
            {'file': '/01module/css_syntax_and_selectors.html', 'title': 'CSS Syntax & Selectors'},
            {'file': '/01module/css_implementation_methods.html', 'title': 'CSS Implementation'},
            {'file': '/01module/css_colors_fonts_text.html', 'title': 'Colors, Fonts & Text'},
            {'file': '/01module/css_box_model.html', 'title': 'CSS Box Model'},
            {'file': '/01module/homework_css_profile.html', 'title': 'Homework: CSS Profile'},
        ],
        4: [
            {'file': '/01module/css_layout_tech.html', 'title': 'CSS Layout Techniques'},
            {'file': '/01module/responsive_design.html', 'title': 'Responsive Design'},
            {'file': '/01module/media_queries.html', 'title': 'Media Queries'},
            {'file': '/01module/mobile_first.html', 'title': 'Mobile-First Approach'},
            {'file': '/01module/homework_responsive_profile.html', 'title': 'Homework: Responsive'},
        ],
        5: [
            {'file': '/01module/bootstrap.html', 'title': 'Introduction to Bootstrap'},
            {'file': '/01module/bootstrap_grid.html', 'title': 'Bootstrap Grid System'},
            {'file': '/01module/bootstrap_components.html', 'title': 'Bootstrap Components'},
            {'file': '/01module/css_organization_best_practices.html', 'title': 'CSS Best Practices'},
            {'file': '/01module/css_preprocessors.html', 'title': 'CSS Preprocessors'},
            {'file': '/01module/homework_bootstrap_profile.html', 'title': 'Homework: Bootstrap'},
        ],
        6: [
            {'file': '/01module/js_intro.html', 'title': 'Introduction to JavaScript'},
            {'file': '/01module/js_syntax_fundamentals.html', 'title': 'JS Syntax & Variables'},
            {'file': '/01module/js_operators_and_expressions.html', 'title': 'Operators & Expressions'},
            {'file': '/01module/js_control_flow.html', 'title': 'Control Flow'},
            {'file': '/01module/js_functions_and_scope.html', 'title': 'Functions & Scope'},
            {'file': '/01module/homework_simple_js_programs.html', 'title': 'Homework: JS Programs'},
        ],
        7: [
            {'file': '/01module/understanding_dom.html', 'title': 'Understanding the DOM'},
            {'file': '/01module/dom_selection_manipulation.html', 'title': 'DOM Selection'},
            {'file': '/01module/event_handling.html', 'title': 'Event Handling'},
            {'file': '/01module/creating_removing_elements.html', 'title': 'Creating Elements'},
            {'file': '/01module/form_validation.html', 'title': 'Form Validation'},
            {'file': '/01module/homework_interactive.html', 'title': 'Homework: Interactive'},
        ],
        8: [
            {'file': '/01module/es6_overview.html', 'title': 'ES6+ Features'},
            {'file': '/01module/jquery_intro.html', 'title': 'Introduction to jQuery'},
            {'file': '/01module/jquery_dom_manipulation.html', 'title': 'jQuery DOM'},
            {'file': '/01module/jquery_animations_and_effects.html', 'title': 'jQuery Animations'},
            {'file': '/01module/jquery_ajax.html', 'title': 'AJAX with jQuery'},
            {'file': '/01module/homework_jquery_refactor.html', 'title': 'Homework: jQuery'},
        ],
        9: [
            {'file': '/01module/php_and_wordpress.html', 'title': 'PHP and WordPress'},
            {'file': '/01module/php_setup_xampp_mamp.html', 'title': 'PHP Setup'},
            {'file': '/01module/php_syntax.html', 'title': 'PHP Syntax'},
            {'file': '/01module/php_variables_data_and_operators.html', 'title': 'PHP Variables'},
            {'file': '/01module/php_includes.html', 'title': 'PHP Includes'},
            {'file': '/01module/homework_simple_php.html', 'title': 'Homework: PHP Script'},
        ],
        10: [
            {'file': '/01module/planning_website.html', 'title': 'Planning a Website'},
            {'file': '/01module/creating_layout.html', 'title': 'Creating Layout'},
            {'file': '/01module/adding_interactivity_with_js.html', 'title': 'Adding Interactivity'},
            {'file': '/01module/php_header_footer.html', 'title': 'PHP Header/Footer'},
            {'file': '/01module/project_static_site.html', 'title': 'Project: Static Site'},
        ],
    }
    return session_lessons.get(session_number, [])

import os
import re
from bs4 import BeautifulSoup
import sys

def get_module_files(module_dir):
    """Get all HTML files in a module directory."""
    files = []
    if os.path.exists(module_dir):
        for file in os.listdir(module_dir):
            if file.endswith('.html'):
                files.append(os.path.join(module_dir, file))
    return sorted(files)

def extract_navigation_from_reference(reference_file):
    """Extract the navigation structure from a reference file (02 or 03 module)."""
    try:
        with open(reference_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the sidebar navigation
        sidebar_nav = soup.find('div', class_='sidebar-nav')
        if sidebar_nav:
            return str(sidebar_nav)
        else:
            print(f"Warning: Could not find sidebar-nav in {reference_file}")
            return None
    except Exception as e:
        print(f"Error reading reference file {reference_file}: {e}")
        return None

def get_session_navigation_info(current_file):
    """Get the previous and next session links based on current file."""
    # Map files to their sessions based on module1.html structure
    file_to_session = {
        # Session 1: Introduction to Web Development & Setup
        'course_introduction.html': 1,
        'how_web_works.html': 1,
        'development_environment.html': 1,
        'first_html_page.html': 1,
        'homework_setup.html': 1,
        
        # Session 2: HTML Fundamentals
        'html_structure_syntax.html': 2,
        'essential_html_tags.html': 2,
        'html_forms_inputs.html': 2,
        'html_validation_practices.html': 2,
        'homework_html_profile.html': 2,
        
        # Session 3: CSS Basics
        'introduction_to_css.html': 3,
        'css_syntax_and_selectors.html': 3,
        'css_implementation_methods.html': 3,
        'css_colors_fonts_text.html': 3,
        'css_box_model.html': 3,
        'homework_css_profile.html': 3,
        
        # Session 4: CSS Layout & Responsive Design
        'css_layout_tech.html': 4,
        'responsive_design.html': 4,
        'media_queries.html': 4,
        'mobile_first.html': 4,
        'homework_responsive_profile.html': 4,
        
        # Session 5: CSS Frameworks & Best Practices
        'bootstrap.html': 5,
        'bootstrap_grid.html': 5,
        'bootstrap_components.html': 5,
        'bootstrap_utilities.html': 5,  # Added missing file
        'css_organization_best_practices.html': 5,
        'css_preprocessors.html': 5,
        'homework_bootstrap_profile.html': 5,
        
        # Session 6: JavaScript Fundamentals
        'js_intro.html': 6,
        'js_syntax_fundamentals.html': 6,
        'js_operators_and_expressions.html': 6,
        'js_control_flow.html': 6,
        'js_functions_and_scope.html': 6,
        'homework_simple_js_programs.html': 6,
        
        # Session 7: DOM Manipulation with JavaScript
        'understanding_dom.html': 7,
        'dom_selection_manipulation.html': 7,
        'event_handling.html': 7,
        'creating_removing_elements.html': 7,
        'form_validation.html': 7,
        'homework_interactive.html': 7,
        
        # Session 8: Modern JavaScript & jQuery
        'es6_overview.html': 8,
        'jquery_intro.html': 8,
        'jquery_dom_manipulation.html': 8,
        'jquery_animations_and_effects.html': 8,
        'jquery_ajax.html': 8,
        'homework_jquery_refactor.html': 8,
        
        # Session 9: Introduction to PHP
        'php_and_wordpress.html': 9,
        'php_setup_xampp_mamp.html': 9,
        'php_syntax.html': 9,
        'php_variables_data_and_operators.html': 9,
        'php_includes.html': 9,
        'homework_simple_php.html': 9,
        
        # Session 10: Mini-Project: Static Website
        'planning_website.html': 10,
        'creating_layout.html': 10,
        'adding_interactivity_with_js.html': 10,
        'php_header_footer.html': 10,
        'project_static_site.html': 10,
    }
    
    # First lesson of each session - VERIFIED from module1.html
    session_first_lessons = {
        1: {'file': '/01module/course_introduction.html', 'title': 'Session 1: Setup'},
        2: {'file': '/01module/html_structure_syntax.html', 'title': 'Session 2: HTML'},
        3: {'file': '/01module/introduction_to_css.html', 'title': 'Session 3: CSS'},
        4: {'file': '/01module/css_layout_tech.html', 'title': 'Session 4: Layout'},
        5: {'file': '/01module/bootstrap.html', 'title': 'Session 5: Bootstrap'},
        6: {'file': '/01module/js_intro.html', 'title': 'Session 6: JavaScript'},
        7: {'file': '/01module/understanding_dom.html', 'title': 'Session 7: DOM'},
        8: {'file': '/01module/es6_overview.html', 'title': 'Session 8: Modern JS'},
        9: {'file': '/01module/php_and_wordpress.html', 'title': 'Session 9: PHP'},
        10: {'file': '/01module/planning_website.html', 'title': 'Session 10: Project'},
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
    
    # Get next session link (if not last session)  
    if current_session < 10:
        next_session = current_session + 1
        result['next'] = session_first_lessons[next_session]['file']
        result['next_title'] = session_first_lessons[next_session]['title']
    elif current_session == 10:
        # Last session links to Module 2 first lesson
        result['next'] = '/02module/review_php_setup.html'
        result['next_title'] = 'Module 2: PHP Setup'
    
    return result

def create_01module_navigation(current_file=None):
    """Create the proper navigation structure for Module 1."""
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
        session_lessons_html = '''                                    <li><a href="/01module/course_introduction.html" class="sidebar-link">Session 1: Setup</a></li>
                                    <li><a href="/01module/html_structure_syntax.html" class="sidebar-link">Session 2: HTML</a></li>
                                    <li><a href="/01module/introduction_to_css.html" class="sidebar-link">Session 3: CSS Basics</a></li>
                                    <li><a href="/01module/css_layout_tech.html" class="sidebar-link">Session 4: CSS Layout</a></li>
                                    <li><a href="/01module/bootstrap.html" class="sidebar-link">Session 5: Bootstrap</a></li>
                                    <li><a href="/01module/js_intro.html" class="sidebar-link">Session 6: JavaScript</a></li>
                                    <li><a href="/01module/understanding_dom.html" class="sidebar-link">Session 7: DOM</a></li>
                                    <li><a href="/01module/es6_overview.html" class="sidebar-link">Session 8: Modern JS</a></li>
                                    <li><a href="/01module/php_and_wordpress.html" class="sidebar-link">Session 9: PHP Intro</a></li>
                                    <li><a href="/01module/planning_website.html" class="sidebar-link">Session 10: Project</a></li>'''
    
    navigation_html = f'''<div class="sidebar-nav">
                            <h3 class="sidebar-title">Module 1: Web Fundamentals</h3>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">{current_session_num}</h4>
                                <ul class="sidebar-menu">
{session_lessons_html}
                                </ul>
                            </div>
                            <div class="sidebar-section">
                                <h4 class="sidebar-section-title">Quick Links</h4>
                                <ul class="sidebar-menu">
                                    <li><a href="/module1.html" class="sidebar-link">Module Overview</a></li>
{prev_session_html}{next_session_html}                                    <li><a href="/" class="sidebar-link">← Course Home</a></li>
                                    <li><a href="/module2.html" class="sidebar-link">Next Module →</a></li>
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
        'course_introduction.html': 'Course Introduction',
        'how_web_works.html': 'How the Web Works',
        'development_environment.html': 'Development Environment',
        'first_html_page.html': 'Your First HTML Page',
        'homework_setup.html': 'Homework: Setup',
        
        # Session 2
        'html_structure_syntax.html': 'HTML Structure & Syntax',
        'essential_html_tags.html': 'Essential HTML Tags',
        'html_forms_inputs.html': 'HTML Forms & Inputs',
        'html_validation_practices.html': 'HTML Validation',
        'homework_html_profile.html': 'Homework: HTML Profile',
        
        # Session 3
        'introduction_to_css.html': 'Introduction to CSS',
        'css_syntax_and_selectors.html': 'CSS Syntax & Selectors',
        'css_implementation_methods.html': 'CSS Implementation',
        'css_colors_fonts_text.html': 'Colors, Fonts & Text',
        'css_box_model.html': 'CSS Box Model',
        'homework_css_profile.html': 'Homework: CSS Profile',
        
        # Session 4
        'css_layout_tech.html': 'CSS Layout Techniques',
        'responsive_design.html': 'Responsive Design',
        'media_queries.html': 'Media Queries',
        'mobile_first.html': 'Mobile-First Approach',
        'homework_responsive_profile.html': 'Homework: Responsive',
        
        # Session 5
        'bootstrap.html': 'Introduction to Bootstrap',
        'bootstrap_grid.html': 'Bootstrap Grid System',
        'bootstrap_components.html': 'Bootstrap Components',
        'bootstrap_utilities.html': 'Bootstrap Utilities',
        'css_organization_best_practices.html': 'CSS Best Practices',
        'css_preprocessors.html': 'CSS Preprocessors',
        'homework_bootstrap_profile.html': 'Homework: Bootstrap',
        
        # Session 6
        'js_intro.html': 'Introduction to JavaScript',
        'js_syntax_fundamentals.html': 'JS Syntax & Variables',
        'js_operators_and_expressions.html': 'Operators & Expressions',
        'js_control_flow.html': 'Control Flow',
        'js_functions_and_scope.html': 'Functions & Scope',
        'homework_simple_js_programs.html': 'Homework: JS Programs',
        
        # Session 7
        'understanding_dom.html': 'Understanding the DOM',
        'dom_selection_manipulation.html': 'DOM Selection',
        'event_handling.html': 'Event Handling',
        'creating_removing_elements.html': 'Creating Elements',
        'form_validation.html': 'Form Validation',
        'homework_interactive.html': 'Homework: Interactive',
        
        # Session 8
        'es6_overview.html': 'ES6+ Features',
        'jquery_intro.html': 'Introduction to jQuery',
        'jquery_dom_manipulation.html': 'jQuery DOM',
        'jquery_animations_and_effects.html': 'jQuery Animations',
        'jquery_ajax.html': 'AJAX with jQuery',
        'homework_jquery_refactor.html': 'Homework: jQuery',
        
        # Session 9
        'php_and_wordpress.html': 'PHP and WordPress',
        'php_setup_xampp_mamp.html': 'PHP Setup',
        'php_syntax.html': 'PHP Syntax',
        'php_variables_data_and_operators.html': 'PHP Variables',
        'php_includes.html': 'PHP Includes',
        'homework_simple_php.html': 'Homework: PHP Script',
        
        # Session 10
        'planning_website.html': 'Planning a Website',
        'creating_layout.html': 'Creating Layout',
        'adding_interactivity_with_js.html': 'Adding Interactivity',
        'php_header_footer.html': 'PHP Header/Footer',
        'project_static_site.html': 'Project: Static Site',
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
        print(f"Processing: {filepath}")
        
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
                print(f"  ⚠ Warning: No sidebar found in {filepath}")
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

def analyze_current_navigation(module_dir):
    """Analyze the current state of navigation in module files."""
    print("\n=== Analyzing Current Navigation Structure ===\n")
    
    files = get_module_files(module_dir)
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"\n{filename}:")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for sidebar
            sidebar = soup.find('aside', class_='sidebar')
            if sidebar:
                print("  ✓ Has sidebar")
                
                # Check for sidebar-nav
                sidebar_nav = soup.find('div', class_='sidebar-nav')
                if sidebar_nav:
                    print("  ✓ Has sidebar-nav")
                    
                    # Check for proper structure
                    sidebar_title = sidebar_nav.find('h3', class_='sidebar-title')
                    if sidebar_title:
                        print(f"    Title: {sidebar_title.get_text(strip=True)}")
                    
                    # Count sidebar sections
                    sections = sidebar_nav.find_all('div', class_='sidebar-section')
                    print(f"    Sections: {len(sections)}")
                    
                    # Count links
                    links = sidebar_nav.find_all('a', class_='sidebar-link')
                    print(f"    Links: {len(links)}")
                    
                    # Check for active link
                    active_links = sidebar_nav.find_all('a', class_='sidebar-link active')
                    if active_links:
                        for link in active_links:
                            print(f"    Active: {link.get_text(strip=True)}")
                    else:
                        print("    ⚠ No active link")
                else:
                    print("  ⚠ Missing sidebar-nav structure")
            else:
                print("  ✗ No sidebar found")
                
        except Exception as e:
            print(f"  ✗ Error analyzing: {e}")

def main():
    """Main function to fix navigation in all 01module files."""
    
    # Define paths - handle both Windows and WSL paths
    if os.path.exists(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module"):
        # Windows path to WSL
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
        print(f"Using Windows WSL path: {base_path}")
    elif os.path.exists("/home/practicalace/projects/php_wordpress/01module"):
        # Direct WSL/Linux path
        base_path = "/home/practicalace/projects/php_wordpress"
        print(f"Using Linux path: {base_path}")
    else:
        # Try current directory
        base_path = os.getcwd()
        print(f"Using current directory: {base_path}")
        
    module01_dir = os.path.join(base_path, "01module")
    module02_dir = os.path.join(base_path, "02module")
    module03_dir = os.path.join(base_path, "03module")
    
    print(f"\nLooking for Module 1 files in: {module01_dir}")
    print(f"Directory exists: {os.path.exists(module01_dir)}")
    
    if os.path.exists(module01_dir):
        files_in_dir = os.listdir(module01_dir)
        print(f"Files found in directory: {len(files_in_dir)}")
        html_files = [f for f in files_in_dir if f.endswith('.html')]
        print(f"HTML files found: {len(html_files)}")
        if html_files:
            print(f"First few HTML files: {html_files[:3]}...")
    
    print("=" * 60)
    print("Module 1 Navigation Fixer")
    print("=" * 60)
    
    # First, analyze current state
    print("\nStep 1: Analyzing current Module 1 navigation...")
    analyze_current_navigation(str(module01_dir))
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("\nDo you want to proceed with fixing the navigation? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Process all Module 1 HTML files
    print("\n" + "=" * 60)
    print("\nStep 2: Updating Module 1 files...")
    print("=" * 60 + "\n")
    
    files = get_module_files(str(module01_dir))
    
    if not files:
        print(f"No HTML files found in {module01_dir}")
        return
    
    success_count = 0
    fail_count = 0
    
    for filepath in files:
        # Get the current page for this file
        current_page = get_current_page_from_file(filepath)
        
        # Create navigation with active state AND next session link for this specific file
        nav_template = create_01module_navigation(filepath)
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
    print("\n✅ Navigation fix complete!")
    
    # Final analysis
    print("\n" + "=" * 60)
    print("\nStep 4: Verifying changes...")
    analyze_current_navigation(str(module01_dir))

if __name__ == "__main__":
    main()
