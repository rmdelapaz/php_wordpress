#!/usr/bin/env python3
"""
Script to transfer content from 01module_old HTML files to 01module files
while preserving the new template structure.
This version handles regex escape sequence issues.
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

def fix_class_names(content):
    """Fix class names by replacing underscores with hyphens."""
    # Process the content in chunks to avoid regex issues
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Only process lines that contain class attributes
        if 'class=' in line:
            # Replace underscores in class names
            line = re.sub(r'class="([^"]*)"', lambda m: 'class="' + m.group(1).replace('_', '-') + '"', line)
            line = re.sub(r"class='([^']*)'", lambda m: "class='" + m.group(1).replace('_', '-') + "'", line)
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def update_new_file(new_file_path, old_content):
    """Update the new file with content from the old file."""
    with open(new_file_path, 'r', encoding='utf-8') as f:
        new_html = f.read()
    
    # Escape special characters in the title for regex
    escaped_title = re.escape(old_content['title'])
    
    # Update title
    new_html = re.sub(
        r'<title>.*?</title>',
        f'<title>{old_content["title"]}</title>',
        new_html
    )
    
    # Update meta description
    desc_text = old_content['title'].replace(' - ', '. ').replace(':', '.')
    # Escape special characters for use in HTML attribute
    desc_text = desc_text.replace('"', '&quot;')
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
    # Escape the lesson title for use in regex replacement
    escaped_lesson_title = lesson_title.replace('\\', '\\\\').replace('$', '\\$')
    new_html = re.sub(
        r'(<header class="lesson-header">.*?<h1>)(.*?)(</h1>)',
        r'\1' + escaped_lesson_title + r'\3',
        new_html,
        flags=re.DOTALL
    )
    
    # Fix class names in old content
    fixed_content = fix_class_names(old_content['content'])
    
    # Find and replace the lesson body content
    # Using a simpler approach to avoid regex issues
    start_marker = '<div class="lesson-body">'
    end_marker = '</div>\n                        <!-- Lesson Navigation -->'
    
    start_index = new_html.find(start_marker)
    end_index = new_html.find(end_marker, start_index)
    
    if start_index != -1 and end_index != -1:
        # Replace the content between the markers
        new_html = (new_html[:start_index + len(start_marker)] + 
                   '\n' + fixed_content + '\n            ' + 
                   new_html[end_index:])
    
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
    # Use absolute paths - works from any directory
    old_dir = Path("/home/practicalace/projects/php_wordpress/01module_old")
    new_dir = Path("/home/practicalace/projects/php_wordpress/01module")
    
    # Check if directories exist
    if not old_dir.exists():
        print(f"Error: Directory not found: {old_dir}")
        print("Please make sure you're running this on the correct system.")
        return
    
    if not new_dir.exists():
        print(f"Error: Directory not found: {new_dir}")
        print("Please make sure you're running this on the correct system.")
        return
    
    # List of files that failed in the previous run
    failed_files = [
        'html_forms_inputs.html',
        'css_organization_best_practices.html',
        'js_intro.html',
        'js_syntax_fundamentals.html',
        'js_operators_and_expressions.html',
        'js_control_flow.html',
        'js_functions_and_scope.html',
        'understanding_dom.html',
        'adding_interactivity_with_js.html',
        'form_validation.html',
        'homework_simple_js_programs.html',
        'homework_interactive.html',
        'jquery_dom_manipulation.html',
        'homework_jquery_refactor.html',
        'php_and_wordpress.html',
        'php_setup_xampp_mamp.html',
        'php_includes.html',
        'homework_simple_php.html',
        'project_static_site.html',
    ]
    
    print("Processing files that failed in the previous run...")
    print(f"Old directory: {old_dir}")
    print(f"New directory: {new_dir}")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for filename in failed_files:
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
    print(f"\nOverall status: {38 + successful} files successfully processed out of 57 total")

if __name__ == "__main__":
    main()
