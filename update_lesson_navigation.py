#!/usr/bin/env python3
"""
Script to update lesson navigation in PHP WordPress course Module 1
Ensures all lesson files have consistent previous/next navigation links
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from bs4 import BeautifulSoup

# Define the lesson order from module1.html
LESSON_ORDER = [
    # Session 1
    'course_introduction.html',
    'how_web_works.html',
    'development_environment.html',
    'first_html_page.html',
    'homework_setup.html',
    # Session 2
    'html_structure_syntax.html',
    'essential_html_tags.html',
    'html_forms_inputs.html',
    'html_validation_practices.html',
    'homework_html_profile.html',
    # Session 3
    'introduction_to_css.html',
    'css_syntax_and_selectors.html',
    'css_implementation_methods.html',
    'css_colors_fonts_text.html',
    'css_box_model.html',
    'homework_css_profile.html',
    # Session 4
    'css_layout_tech.html',
    'responsive_design.html',
    'media_queries.html',
    'mobile_first.html',
    'homework_responsive_profile.html',
    # Session 5
    'bootstrap.html',
    'bootstrap_grid.html',
    'bootstrap_components.html',
    'css_organization_best_practices.html',
    'css_preprocessors.html',
    'homework_bootstrap_profile.html',
    # Session 6
    'js_intro.html',
    'js_syntax_fundamentals.html',
    'js_operators_and_expressions.html',
    'js_control_flow.html',
    'js_functions_and_scope.html',
    'homework_simple_js_programs.html',
    # Session 7
    'understanding_dom.html',
    'dom_selection_manipulation.html',
    'event_handling.html',
    'creating_removing_elements.html',
    'form_validation.html',
    'homework_interactive.html',
    # Session 8
    'es6_overview.html',
    'jquery_intro.html',
    'jquery_dom_manipulation.html',
    'jquery_animations_and_effects.html',
    'jquery_ajax.html',
    'homework_jquery_refactor.html',
    # Session 9
    'php_and_wordpress.html',
    'php_setup_xampp_mamp.html',
    'php_syntax.html',
    'php_variables_data_and_operators.html',
    'php_includes.html',
    'homework_simple_php.html',
    # Session 10
    'planning_website.html',
    'creating_layout.html',
    'adding_interactivity_with_js.html',
    'php_header_footer.html',
    'project_static_site.html'
]

# Map lesson files to their display titles
LESSON_TITLES = {
    'course_introduction.html': 'Course Introduction',
    'how_web_works.html': 'How the Web Works',
    'development_environment.html': 'Development Environment',
    'first_html_page.html': 'Your First HTML Page',
    'homework_setup.html': 'Homework: Setup',
    'html_structure_syntax.html': 'HTML Structure & Syntax',
    'essential_html_tags.html': 'Essential HTML Tags',
    'html_forms_inputs.html': 'HTML Forms & Inputs',
    'html_validation_practices.html': 'HTML Validation & Best Practices',
    'homework_html_profile.html': 'Homework: HTML Profile',
    'introduction_to_css.html': 'Introduction to CSS',
    'css_syntax_and_selectors.html': 'CSS Syntax & Selectors',
    'css_implementation_methods.html': 'CSS Implementation Methods',
    'css_colors_fonts_text.html': 'CSS Colors, Fonts & Text',
    'css_box_model.html': 'The CSS Box Model',
    'homework_css_profile.html': 'Homework: CSS Profile',
    'css_layout_tech.html': 'CSS Layout Techniques',
    'responsive_design.html': 'Responsive Design',
    'media_queries.html': 'Media Queries',
    'mobile_first.html': 'Mobile-First Approach',
    'homework_responsive_profile.html': 'Homework: Responsive Profile',
    'bootstrap.html': 'Introduction to Bootstrap',
    'bootstrap_grid.html': 'Bootstrap Grid System',
    'bootstrap_components.html': 'Bootstrap Components',
    'css_organization_best_practices.html': 'CSS Organization & Best Practices',
    'css_preprocessors.html': 'CSS Preprocessors',
    'homework_bootstrap_profile.html': 'Homework: Bootstrap Profile',
    'js_intro.html': 'Introduction to JavaScript',
    'js_syntax_fundamentals.html': 'JavaScript Syntax & Fundamentals',
    'js_operators_and_expressions.html': 'JavaScript Operators & Expressions',
    'js_control_flow.html': 'JavaScript Control Flow',
    'js_functions_and_scope.html': 'Functions & Scope',
    'homework_simple_js_programs.html': 'Homework: Simple JS Programs',
    'understanding_dom.html': 'Understanding the DOM',
    'dom_selection_manipulation.html': 'DOM Selection & Manipulation',
    'event_handling.html': 'Event Handling',
    'creating_removing_elements.html': 'Creating & Removing Elements',
    'form_validation.html': 'Form Validation',
    'homework_interactive.html': 'Homework: Interactive Page',
    'es6_overview.html': 'ES6+ Features Overview',
    'jquery_intro.html': 'Introduction to jQuery',
    'jquery_dom_manipulation.html': 'jQuery DOM Manipulation',
    'jquery_animations_and_effects.html': 'jQuery Animations & Effects',
    'jquery_ajax.html': 'AJAX with jQuery',
    'homework_jquery_refactor.html': 'Homework: jQuery Refactor',
    'php_and_wordpress.html': 'PHP and WordPress',
    'php_setup_xampp_mamp.html': 'PHP Setup (XAMPP/MAMP)',
    'php_syntax.html': 'PHP Syntax',
    'php_variables_data_and_operators.html': 'PHP Variables & Operators',
    'php_includes.html': 'PHP Includes',
    'homework_simple_php.html': 'Homework: Simple PHP',
    'planning_website.html': 'Planning a Website',
    'creating_layout.html': 'Creating a Layout',
    'adding_interactivity_with_js.html': 'Adding JavaScript Interactivity',
    'php_header_footer.html': 'PHP Header & Footer',
    'project_static_site.html': 'Final Project: Static Site'
}


def get_navigation_html(prev_link: str, prev_title: str,
                        next_link: str, next_title: str) -> str:
    """Generate the navigation HTML with proper structure"""
    return f'''<div class="lesson-navigation">
    <a href="{prev_link}" class="lesson-nav-button prev">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
        </svg>
        <span>
            <small>Previous</small><br>
            {prev_title}
        </span>
    </a>
    
    <button class="complete-lesson-btn">
        Mark as Complete
    </button>
    
    <a href="{next_link}" class="lesson-nav-button next">
        <span>
            <small>Next</small><br>
            {next_title}
        </span>
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
        </svg>
    </a>
</div>'''


def get_navigation_for_lesson(lesson_file: str) -> Tuple[
        Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Get navigation links and titles for a specific lesson"""
    try:
        index = LESSON_ORDER.index(lesson_file)
    except ValueError:
        print(f"Warning: {lesson_file} not found in lesson order")
        return None, None, None, None

    # Previous lesson
    if index == 0:
        prev_link = "/module1.html"
        prev_title = "Module Overview"
    else:
        prev_file = LESSON_ORDER[index - 1]
        prev_link = f"/01module/{prev_file}"
        prev_title = LESSON_TITLES.get(
            prev_file,
            prev_file.replace('.html', '').replace('_', ' ').title()
        )

    # Next lesson
    if index == len(LESSON_ORDER) - 1:
        next_link = "/module2.html"
        next_title = "Module 2: PHP Fundamentals"
    else:
        next_file = LESSON_ORDER[index + 1]
        next_link = f"/01module/{next_file}"
        next_title = LESSON_TITLES.get(
            next_file,
            next_file.replace('.html', '').replace('_', ' ').title()
        )

    return prev_link, prev_title, next_link, next_title


def update_lesson_file(file_path: Path) -> bool:
    """Update the navigation in a single lesson file"""
    lesson_file = file_path.name

    # Get navigation info
    nav_info = get_navigation_for_lesson(lesson_file)
    if nav_info[0] is None:
        return False

    prev_link, prev_title, next_link, next_title = nav_info

    # These should never be None at this point, but add type assertion
    assert prev_link is not None
    assert prev_title is not None
    assert next_link is not None
    assert next_title is not None

    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Find the existing navigation div
        nav_div = soup.find('div', class_='lesson-navigation')

        if nav_div:
            # Create new navigation HTML
            new_nav_html = get_navigation_html(
                prev_link, prev_title, next_link, next_title
            )
            new_nav_soup = BeautifulSoup(new_nav_html, 'html.parser')

            # Get the new navigation div
            new_nav_div = new_nav_soup.find('div', class_='lesson-navigation')
            if new_nav_div:
                # Replace the old navigation with the new one
                nav_div.replace_with(new_nav_div)

                # Write the updated content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Use prettify but maintain original formatting
                    f.write(str(soup))

                print(f"✓ Updated: {lesson_file}")
                return True
            else:
                print(f"✗ Error creating new navigation for: {lesson_file}")
                return False
        else:
            print(f"✗ No navigation found in: {lesson_file}")
            return False

    except IOError as e:
        print(f"✗ Error reading/writing {lesson_file}: {str(e)}")
        return False
    except RuntimeError as e:
        print(f"✗ Unexpected error updating {lesson_file}: {str(e)}")
        return False


def main():
    """Main function to update all lesson files"""
    # Set the path to the 01module directory
    # Using os.path for better compatibility
    module_path = Path(os.path.join(
        "\\\\wsl$", "Ubuntu", "home", "practicalace",
        "projects", "php_wordpress", "01module"
    ))

    if not module_path.exists():
        print(f"Error: Directory not found: {module_path}")
        print("Please update the module_path variable with the correct path.")
        return

    print(f"Processing files in: {module_path}")
    print(f"Total lessons to process: {len(LESSON_ORDER)}")
    print("-" * 50)

    success_count = 0
    skip_count = 0
    error_count = 0

    for lesson_file in LESSON_ORDER:
        file_path = module_path / lesson_file

        if not file_path.exists():
            print(f"⚠ File not found: {lesson_file}")
            skip_count += 1
            continue

        if update_lesson_file(file_path):
            success_count += 1
        else:
            error_count += 1

    print("-" * 50)
    print("Summary:")
    print(f"  Successfully updated: {success_count}")
    print(f"  Skipped (not found): {skip_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {success_count + skip_count + error_count}")


if __name__ == "__main__":
    main()
