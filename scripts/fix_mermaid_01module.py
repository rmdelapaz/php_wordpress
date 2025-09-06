#!/usr/bin/env python3
"""
Script to fix Mermaid diagram support in all 01module HTML files.
This will ensure Mermaid is properly initialized for files that contain diagrams.
"""

import os
import re
from pathlib import Path

def check_needs_mermaid(file_path):
    """Check if the HTML file contains Mermaid diagrams."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for various indicators of Mermaid usage
    indicators = [
        'class="mermaid"',
        'class=\'mermaid\'',
        '<div class="mermaid">',
        'graph LR',
        'graph TD',
        'graph TB',
        'sequenceDiagram',
        'flowchart',
        'mindmap',
        'pie title',
        'gantt',
        'erDiagram',
        'stateDiagram',
        'gitGraph',
        'journey'
    ]
    
    return any(indicator in content for indicator in indicators)

def add_mermaid_support(file_path):
    """Add or fix Mermaid support in the HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Mermaid script already exists (old or new style)
    has_mermaid_script = ('mermaid' in content and '<script' in content and 'mermaid.min.js' in content) or \
                         ('mermaid' in content and '<script' in content and 'mermaid.esm.min.mjs' in content)
    
    if not has_mermaid_script:
        # Add Mermaid initialization script before </head>
        mermaid_script = '''    <!-- Mermaid for diagrams -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            },
            securityLevel: 'loose'
        });
    </script>
'''
        content = content.replace('</head>', mermaid_script + '</head>')
    
    # Also ensure we have the fallback script at the bottom if needed
    if 'mermaid.min.js' not in content and '</body>' in content:
        fallback_script = '''
    <!-- Mermaid fallback -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.0.2/dist/mermaid.min.js"></script>
    <script>
        // Initialize mermaid if not already initialized
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true
                },
                securityLevel: 'loose'
            });
            // Manually render any mermaid diagrams
            mermaid.init();
        }
    </script>
'''
        content = content.replace('</body>', fallback_script + '</body>')
    
    # Fix any mermaid_container divs to ensure they have the right class
    content = re.sub(
        r'<div class="mermaid_container">\s*<div class="mermaid">',
        '<div class="mermaid-container">\n                    <div class="mermaid">',
        content,
        flags=re.DOTALL
    )
    
    return content

def process_file(file_path):
    """Process a single HTML file."""
    filename = file_path.name
    
    try:
        if check_needs_mermaid(file_path):
            updated_content = add_mermaid_support(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            return True, f"Added/fixed Mermaid support in {filename}"
        else:
            return False, f"No Mermaid content found in {filename}"
    
    except Exception as e:
        return False, f"Error processing {filename}: {str(e)}"

def main():
    """Main function to process all HTML files in 01module."""
    module_dir = Path("/home/practicalace/projects/php_wordpress/01module")
    
    # Check if directory exists
    if not module_dir.exists():
        print(f"Error: Directory not found: {module_dir}")
        return
    
    # Get all HTML files
    html_files = list(module_dir.glob("*.html"))
    
    print(f"Checking and fixing Mermaid support in {len(html_files)} HTML files...")
    print("=" * 60)
    
    fixed = 0
    skipped = 0
    failed = 0
    
    # Files specifically mentioned as having issues
    priority_files = [
        'bootstrap_components.html',
        'first_html_page.html', 
        'how_web_works.html',
        'introduction_to_css.html',
        'planning_website.html',
        'html_structure_syntax.html',
        'css_syntax_and_selectors.html',
        'css_box_model.html',
        'css_layout_tech.html',
        'understanding_dom.html',
        'responsive_design.html'
    ]
    
    # Process priority files first
    print("Processing files known to have Mermaid diagrams...")
    print("-" * 40)
    
    for filename in priority_files:
        file_path = module_dir / filename
        if file_path.exists():
            success, message = process_file(file_path)
            if success:
                if "Added/fixed" in message:
                    print(f"✓ {message}")
                    fixed += 1
                else:
                    skipped += 1
            else:
                if "No Mermaid" not in message:
                    print(f"✗ {message}")
                    failed += 1
                else:
                    skipped += 1
    
    print("\n" + "-" * 40)
    print("Processing remaining files...")
    print("-" * 40)
    
    # Process all other files
    for file_path in html_files:
        if file_path.name not in priority_files:
            success, message = process_file(file_path)
            if success:
                if "Added/fixed" in message:
                    print(f"✓ {message}")
                    fixed += 1
                else:
                    skipped += 1
            else:
                if "No Mermaid" not in message:
                    print(f"✗ {message}")
                    failed += 1
                else:
                    skipped += 1
    
    print("=" * 60)
    print(f"Processing complete!")
    print(f"  Fixed: {fixed} files")
    print(f"  Skipped (no Mermaid): {skipped} files")
    print(f"  Failed: {failed} files")
    print(f"  Total: {fixed + skipped + failed} files")
    
    if fixed > 0:
        print("\n✨ Mermaid support has been added/fixed in the affected files.")
        print("   Please refresh your browser to see the diagrams.")

if __name__ == "__main__":
    main()
