#!/usr/bin/env python3
"""
Fix all diagrams and SVGs in 02module files
- Centers diagrams horizontally and vertically
- Removes excessive spacing below diagrams
- Fixes diamond shapes for decision symbols
- Ensures no container overlaps
- Works with Windows WSL paths
"""

import os
import re
import sys
from pathlib import Path

def get_base_path():
    """Get the correct base path for WSL or Windows environment."""
    if sys.platform == "win32" or os.path.exists(r"\\wsl$"):
        # Windows environment - use WSL path
        return r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
    else:
        # Linux/WSL environment
        return "/home/practicalace/projects/php_wordpress"

def fix_diamond_shapes(svg_content):
    """Convert rotated rectangles to proper diamond shapes for decision symbols."""
    
    # Pattern to find rotated rectangles (typical for decision nodes)
    # These are usually rectangles with rotation transform
    rotated_rect_pattern = r'<rect([^>]*?)transform="rotate\(45[^"]*\)"([^>]*?)/?>'
    
    def replace_with_diamond(match):
        attrs = match.group(1) + match.group(2)
        
        # Extract position and size attributes
        x_match = re.search(r'x="([^"]*)"', attrs)
        y_match = re.search(r'y="([^"]*)"', attrs)
        width_match = re.search(r'width="([^"]*)"', attrs)
        height_match = re.search(r'height="([^"]*)"', attrs)
        
        if x_match and y_match and width_match and height_match:
            try:
                x = float(x_match.group(1))
                y = float(y_match.group(1))
                width = float(width_match.group(1))
                height = float(height_match.group(1))
                
                # Calculate diamond points
                cx = x + width / 2
                cy = y + height / 2
                
                # Create diamond path
                points = f"{cx},{y} {x + width},{cy} {cx},{y + height} {x},{cy}"
                
                # Extract other attributes like fill, stroke, etc.
                fill = re.search(r'fill="([^"]*)"', attrs)
                stroke = re.search(r'stroke="([^"]*)"', attrs)
                stroke_width = re.search(r'stroke-width="([^"]*)"', attrs)
                class_attr = re.search(r'class="([^"]*)"', attrs)
                
                polygon_attrs = ""
                if fill:
                    polygon_attrs += f' fill="{fill.group(1)}"'
                if stroke:
                    polygon_attrs += f' stroke="{stroke.group(1)}"'
                if stroke_width:
                    polygon_attrs += f' stroke-width="{stroke_width.group(1)}"'
                if class_attr:
                    polygon_attrs += f' class="{class_attr.group(1)}"'
                
                return f'<polygon points="{points}"{polygon_attrs}/>'
            except:
                return match.group(0)  # Return original if conversion fails
        
        return match.group(0)
    
    # Replace rotated rectangles with diamonds
    svg_content = re.sub(rotated_rect_pattern, replace_with_diamond, svg_content)
    
    # Also look for rectangles that are meant to be decision nodes (usually have specific classes)
    decision_rect_pattern = r'<rect([^>]*?class="[^"]*decision[^"]*"[^>]*?)>'
    
    def make_diamond(match):
        attrs = match.group(1)
        
        # Extract attributes
        x_match = re.search(r'x="([^"]*)"', attrs)
        y_match = re.search(r'y="([^"]*)"', attrs)
        width_match = re.search(r'width="([^"]*)"', attrs)
        height_match = re.search(r'height="([^"]*)"', attrs)
        
        if x_match and y_match and width_match and height_match:
            try:
                x = float(x_match.group(1))
                y = float(y_match.group(1))
                width = float(width_match.group(1))
                height = float(height_match.group(1))
                
                # Create diamond shape
                cx = x + width / 2
                cy = y + height / 2
                half_w = width / 2
                half_h = height / 2
                
                points = f"{cx},{y} {x + width},{cy} {cx},{y + height} {x},{cy}"
                
                # Copy all other attributes
                other_attrs = re.sub(r'(x|y|width|height)="[^"]*"\s*', '', attrs)
                
                return f'<polygon points="{points}" {other_attrs}>'
            except:
                return match.group(0)
        
        return match.group(0)
    
    svg_content = re.sub(decision_rect_pattern, make_diamond, svg_content)
    
    return svg_content

def fix_svg_container(content):
    """Fix SVG container spacing and centering."""
    
    # Pattern for SVG containers
    patterns = [
        # Mermaid-converted containers
        (r'<div class="mermaid-converted"[^>]*>(.*?)</div>(?=\s*(?:<|$))', 'mermaid-converted'),
        # Regular SVG containers
        (r'<div class="svg-container"[^>]*>(.*?)</div>(?=\s*(?:<|$))', 'svg-container'),
        # Diagram containers
        (r'<div class="diagram"[^>]*>(.*?)</div>(?=\s*(?:<|$))', 'diagram'),
    ]
    
    for pattern, container_class in patterns:
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in reversed(list(matches)):
            original = match.group(0)
            inner_content = match.group(1)
            
            # Fix the SVG content
            inner_content = fix_diamond_shapes(inner_content)
            
            # Add proper styling to container
            styled_container = f'''<div class="{container_class}" style="margin: 1.5rem auto; padding: 1rem; text-align: center; overflow: hidden; max-width: 100%;">
{inner_content.strip()}
</div>'''
            
            content = content[:match.start()] + styled_container + content[match.end():]
    
    return content

def fix_svg_elements(content):
    """Fix individual SVG elements for proper display."""
    
    # Find all SVG elements
    svg_pattern = r'<svg([^>]*?)>(.*?)</svg>'
    
    def fix_svg(match):
        attrs = match.group(1)
        inner = match.group(2)
        
        # Fix diamond shapes in the SVG content
        inner = fix_diamond_shapes(inner)
        
        # Ensure SVG has proper attributes for centering
        if 'style=' not in attrs:
            attrs += ' style="max-width: 100%; height: auto; display: block; margin: 0 auto;"'
        else:
            # Add to existing style
            attrs = re.sub(
                r'style="([^"]*)"',
                r'style="\1; max-width: 100%; height: auto; display: block; margin: 0 auto;"',
                attrs
            )
        
        # Ensure viewBox is set for responsive sizing
        if 'viewBox=' not in attrs:
            # Try to extract width and height to create viewBox
            width_match = re.search(r'width="(\d+)"', attrs)
            height_match = re.search(r'height="(\d+)"', attrs)
            
            if width_match and height_match:
                width = width_match.group(1)
                height = height_match.group(1)
                attrs += f' viewBox="0 0 {width} {height}"'
        
        return f'<svg{attrs}>{inner}</svg>'
    
    content = re.sub(svg_pattern, fix_svg, content, flags=re.DOTALL)
    
    return content

def remove_excessive_spacing(content):
    """Remove excessive spacing around diagrams and SVGs."""
    
    # Remove multiple consecutive newlines around diagram containers
    content = re.sub(r'(\n\s*){3,}(<div class="(?:mermaid-converted|svg-container|diagram)")', r'\n\n\2', content)
    content = re.sub(r'(</div>)(\s*\n){3,}', r'\1\n\n', content)
    
    # Remove excessive spacing within SVG elements
    content = re.sub(r'(<svg[^>]*>)\s*\n\s*\n+', r'\1\n', content)
    content = re.sub(r'\n\s*\n+\s*(</svg>)', r'\n\1', content)
    
    # Clean up spacing between SVG elements
    content = re.sub(r'(</(?:rect|circle|path|polygon|text|g)>)\s*\n\s*\n+\s*(<(?:rect|circle|path|polygon|text|g))', r'\1\n\2', content)
    
    return content

def add_global_diagram_styles(content):
    """Add or update global styles for diagrams."""
    
    diagram_styles = '''
<style>
/* Global diagram and SVG styles */
.mermaid-converted,
.svg-container,
.diagram {
    margin: 1.5rem auto !important;
    padding: 1rem !important;
    text-align: center !important;
    overflow: hidden !important;
    max-width: 100% !important;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.mermaid-converted svg,
.svg-container svg,
.diagram svg {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
}

/* Fix for decision diamonds */
.decision-node polygon,
polygon.decision {
    fill: #fff3cd !important;
    stroke: #856404 !important;
    stroke-width: 2px !important;
}

/* Remove excessive bottom margins */
.mermaid-converted + *,
.svg-container + *,
.diagram + * {
    margin-top: 1.5rem !important;
}

/* Center content vertically in containers */
.mermaid-converted > *,
.svg-container > *,
.diagram > * {
    vertical-align: middle;
}
</style>
'''
    
    # Add styles before closing </head> tag if not already present
    if 'Global diagram and SVG styles' not in content:
        content = content.replace('</head>', diagram_styles + '\n</head>')
    
    return content

def process_file(filepath):
    """Process a single HTML file to fix diagrams."""
    
    try:
        print(f"Processing: {os.path.basename(filepath)}")
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has any diagrams/SVGs
        if not any(x in content for x in ['<svg', 'mermaid-converted', 'svg-container', 'class="diagram"']):
            print(f"  No diagrams found in {os.path.basename(filepath)}")
            return False
        
        # Create backup
        backup_path = filepath + '.diagram_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created backup: {os.path.basename(backup_path)}")
        
        # Apply all fixes
        original_length = len(content)
        
        content = fix_svg_container(content)
        content = fix_svg_elements(content)
        content = remove_excessive_spacing(content)
        content = add_global_diagram_styles(content)
        
        # Write the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        new_length = len(content)
        print(f"  ✓ Fixed diagrams (size: {original_length:,} → {new_length:,} bytes)")
        
        # Count what was fixed
        svg_count = content.count('<svg')
        diamond_count = content.count('<polygon')
        
        print(f"    - SVG elements: {svg_count}")
        print(f"    - Diamond shapes: {diamond_count}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all 02module files."""
    
    print("Diagram Fix Script for 02module Files")
    print("=" * 60)
    
    # Get base path
    base_path = get_base_path()
    module_path = os.path.join(base_path, "02module")
    
    print(f"Base path: {base_path}")
    print(f"Module path: {module_path}")
    
    if not os.path.exists(module_path):
        print(f"\nError: Module path not found: {module_path}")
        return
    
    # Get all HTML files in 02module
    html_files = [f for f in os.listdir(module_path) if f.endswith('.html') and not f.endswith('.backup')]
    
    print(f"\nFound {len(html_files)} HTML files in 02module")
    print("-" * 60)
    
    fixed_count = 0
    files_with_diagrams = []
    
    for filename in html_files:
        filepath = os.path.join(module_path, filename)
        
        # Quick check for diagram content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if any(x in content for x in ['<svg', 'mermaid-converted', 'svg-container', 'class="diagram"']):
            files_with_diagrams.append(filename)
            if process_file(filepath):
                fixed_count += 1
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Total files scanned: {len(html_files)}")
    print(f"  Files with diagrams: {len(files_with_diagrams)}")
    print(f"  Files successfully fixed: {fixed_count}")
    
    if files_with_diagrams:
        print(f"\nFiles with diagrams:")
        for fname in files_with_diagrams:
            print(f"  - {fname}")
    
    print("\n✓ Diagram fixing complete!")
    print("\nNext steps:")
    print("1. Check the files in your browser")
    print("2. Verify diagrams are centered and properly spaced")
    print("3. Confirm decision symbols appear as diamonds")
    print("4. If any issues remain, check the browser console for errors")

if __name__ == "__main__":
    main()
