#!/usr/bin/env python3
"""
Script to transfer content from 01module_old HTML files to 01module files
while preserving the new template structure.
"""

import os
import re
from pathlib import Path

def extract_main_content(old_file_path):
    """Extract the main content from the old HTML file."""
    with open(old_file_path, 'r', encoding='utf-8') as f:
        old_html = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', old_html, re.DOTALL)
    title = title_match.group(1) if title_match else "Untitled"
    
    # Extract main content
    main_match = re.search(r'<main>(.*?)</main>', old_html, re.DOTALL)
    main_content = main_match.group(1) if main_match else ""
    
    # Check if mermaid is used
    has_mermaid = 'mermaid' in old_html.lower()
    
    return {
        'title': title.strip(),
        'content': main_content,
        'has_mermaid': has_mermaid
    }

def update_new_file(new_file_path, old_content):
    """Update the new file with content from the old file."""
    with open(new_file_path, 'r', encoding='utf-8') as f:
        new_html = f.read()
    
    # Update title
    new_html = re.sub(
        r'<title>.*?</title>',
        f'<title>{old_content["title"]}</title>',
        new_html
    )
    
    # Update meta description
    desc_text = old_content['title'].replace(' - ', '. ').replace(':', '.')
    new_html = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{desc_text}">',
        new_html
    )
    
    # Extract the lesson title from the full title
    lesson_title = old_content['title']
    if ' - ' in lesson_title:
        lesson_title = lesson_title.split(' - ')[-1]
    elif ': ' in lesson_title:
        parts = lesson_title.split(': ')
        if len(parts) > 1:
            lesson_title = ': '.join(parts[1:])
    
    # Update the h1 in lesson header
    new_html = re.sub(
        r'(<header class="lesson-header">.*?<h1>)(.*?)(</h1>)',
        r'\1' + lesson_title + r'\3',
        new_html,
        flags=re.DOTALL
    )
    
    # Replace lesson body content
    # First, fix class names in old content (underscore to hyphen)
    fixed_content = old_content['content']
    fixed_content = re.sub(r'class="([^"]*?)_([^"]*?)"', r'class="\1-\2"', fixed_content)
    fixed_content = re.sub(r"class='([^']*?)_([^']*?)'", r"class='\1-\2'", fixed_content)
    
    # Replace the lesson body content
    new_html = re.sub(
        r'(<div class="lesson-body">)(.*?)(</div>\s*<!-- Lesson Navigation -->)',
        r'\1\n' + fixed_content + '\n            \3',
        new_html,
        flags=re.DOTALL
    )
    
    # Add mermaid script if needed and not already present
    if old_content['has_mermaid'] and 'mermaid' not in new_html:
        mermaid_script = '''    <!-- Mermaid for diagrams -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            }
        });
    </script>
'''
        new_html = new_html.replace('</head>', mermaid_script + '</head>')
    
    return new_html

def process_file(filename, old_dir, new_dir):
    """Process a single file."""
    old_file = old_dir / filename
    new_file = new_dir / filename
    
    if not old_file.exists():
        return False, f"Old file doesn't exist: {filename}"
    
    if not new_file.exists():
        return False, f"New file doesn't exist: {filename}"
    
    try:
        # Extract content from old file
        old_content = extract_main_content(old_file)
        
        # Update new file with old content
        updated_html = update_new_file(new_file, old_content)
        
        # Write updated content
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        return True, f"Successfully updated {filename}"
        
    except Exception as e:
        return False, f"Error processing {filename}: {str(e)}"

def main():
    """Main function to process all files."""
    old_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module_old")
    new_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module")
    
    # List of files to process (all HTML files in 01module)
    files_to_process = [
        'course_introduction.html',  # Already done, but we can re-process
        'how_web_works.html',
        'development_environment.html',
        'first_html_page.html',
        'planning_website.html',
        'html_structure_syntax.html',
        'essential_html_tags.html',
        'html_forms_inputs.html',
        'html_validation_practices.html',
        'homework_html_profile.html',
        'introduction_to_css.html',
        'css_syntax_and_selectors.html',
        'css_implementation_methods.html',
        'css_box_model.html',
        'css_colors_fonts_text.html',
        'css_layout_tech.html',
        'creating_layout.html',
        'css_organization_best_practices.html',
        'homework_css_profile.html',
        'js_intro.html',
        'js_syntax_fundamentals.html',
        'js_operators_and_expressions.html',
        'js_control_flow.html',
        'js_functions_and_scope.html',
        'understanding_dom.html',
        'dom_selection_manipulation.html',
        'creating_removing_elements.html',
        'event_handling.html',
        'adding_interactivity_with_js.html',
        'form_validation.html',
        'homework_simple_js_programs.html',
        'homework_interactive.html',
        'jquery_intro.html',
        'jquery_dom_manipulation.html',
        'jquery_animations_and_effects.html',
        'jquery_ajax.html',
        'homework_jquery_refactor.html',
        'es6_overview.html',
        'responsive_design.html',
        'mobile_first.html',
        'media_queries.html',
        'homework_responsive_profile.html',
        'bootstrap.html',
        'bootstrap_grid.html',
        'bootstrap_components.html',
        'bootstrap_utilities.html',
        'homework_bootstrap_profile.html',
        'css_preprocessors.html',
        'php_and_wordpress.html',
        'php_setup_xampp_mamp.html',
        'php_syntax.html',
        'php_variables_data_and_operators.html',
        'php_includes.html',
        'php_header_footer.html',
        'homework_simple_php.html',
        'homework_setup.html',
        'project_static_site.html',
    ]
    
    print("Starting content transfer from 01module_old to 01module...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for filename in files_to_process:
        success, message = process_file(filename, old_dir, new_dir)
        
        if success:
            print(f"✓ {message}")
            successful += 1
        else:
            print(f"✗ {message}")
            failed += 1
    
    print("=" * 60)
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {successful + failed}")

if __name__ == "__main__":
    main()
