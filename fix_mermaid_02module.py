#!/usr/bin/env python3
"""
Fix Mermaid diagrams in 02module files
- Only processes files with Mermaid diagrams
- Makes decision blocks consistent in size
- Prevents overlapping elements
- Removes excessive bottom spacing
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

def has_mermaid_content(content):
    """Check if the file contains Mermaid diagrams."""
    mermaid_indicators = [
        'class="mermaid"',
        'mermaid-converted',
        'class="mermaid-container"',
        'class="mermaid-diagram"',
        '<!-- Mermaid',
        'mermaid.initialize',
        'graph TD',
        'graph LR',
        'flowchart',
        'sequenceDiagram'
    ]
    
    return any(indicator in content for indicator in mermaid_indicators)

def standardize_decision_blocks(svg_content):
    """Make all decision blocks consistent in size and convert to diamonds."""
    
    # Standard size for decision blocks
    DECISION_WIDTH = 120
    DECISION_HEIGHT = 80
    
    # Find all potential decision blocks (rotated rectangles or those with decision-related classes)
    decision_patterns = [
        # Rotated rectangles
        r'<rect([^>]*?)transform="rotate\(45[^"]*\)"([^>]*?)/>',
        # Rectangles with decision-related classes
        r'<rect([^>]*?class="[^"]*(?:decision|choice|condition|branch)[^"]*"[^>]*?)/>',
        # Rectangles with rhombus or diamond references
        r'<rect([^>]*?class="[^"]*(?:rhombus|diamond)[^"]*"[^>]*?)/>',
    ]
    
    def create_standard_diamond(x, y, fill="#fff3cd", stroke="#856404", stroke_width="2", label="", extra_attrs=""):
        """Create a standardized diamond shape."""
        # Calculate diamond points with consistent size
        cx = x + DECISION_WIDTH / 2
        cy = y + DECISION_HEIGHT / 2
        
        # Diamond points (top, right, bottom, left)
        points = [
            f"{cx},{y}",  # Top
            f"{x + DECISION_WIDTH},{cy}",  # Right
            f"{cx},{y + DECISION_HEIGHT}",  # Bottom
            f"{x},{cy}"  # Left
        ]
        
        points_str = " ".join(points)
        
        return f'<polygon points="{points_str}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" {extra_attrs}/>'
    
    for pattern in decision_patterns:
        matches = list(re.finditer(pattern, svg_content))
        
        for match in reversed(matches):  # Process in reverse to maintain positions
            full_match = match.group(0)
            attrs = match.group(1) + (match.group(2) if match.lastindex >= 2 else "")
            
            # Extract position
            x_match = re.search(r'x="([^"]*)"', attrs)
            y_match = re.search(r'y="([^"]*)"', attrs)
            
            if x_match and y_match:
                try:
                    x = float(x_match.group(1))
                    y = float(y_match.group(1))
                    
                    # Extract styling attributes
                    fill_match = re.search(r'fill="([^"]*)"', attrs)
                    stroke_match = re.search(r'stroke="([^"]*)"', attrs)
                    stroke_width_match = re.search(r'stroke-width="([^"]*)"', attrs)
                    class_match = re.search(r'class="([^"]*)"', attrs)
                    id_match = re.search(r'id="([^"]*)"', attrs)
                    
                    fill = fill_match.group(1) if fill_match else "#fff3cd"
                    stroke = stroke_match.group(1) if stroke_match else "#856404"
                    stroke_width = stroke_width_match.group(1) if stroke_width_match else "2"
                    
                    extra_attrs = ""
                    if class_match:
                        extra_attrs += f' class="{class_match.group(1)}"'
                    if id_match:
                        extra_attrs += f' id="{id_match.group(1)}"'
                    
                    # Create standardized diamond
                    diamond = create_standard_diamond(x, y, fill, stroke, stroke_width, extra_attrs=extra_attrs)
                    
                    # Replace in content
                    svg_content = svg_content[:match.start()] + diamond + svg_content[match.end():]
                    
                except (ValueError, AttributeError):
                    continue  # Skip if we can't parse the values
    
    return svg_content

def fix_overlapping_elements(svg_content):
    """Fix overlapping elements by adjusting spacing and positions."""
    
    # Find all shape elements and their positions
    element_pattern = r'<(rect|circle|polygon|ellipse|path)([^>]*?)/?>'
    elements = []
    
    for match in re.finditer(element_pattern, svg_content):
        tag = match.group(1)
        attrs = match.group(2)
        
        # Try to extract position
        if tag in ['rect', 'circle', 'ellipse']:
            x_match = re.search(r'(?:x|cx)="([^"]*)"', attrs)
            y_match = re.search(r'(?:y|cy)="([^"]*)"', attrs)
            
            if x_match and y_match:
                try:
                    x = float(x_match.group(1))
                    y = float(y_match.group(1))
                    elements.append({'match': match, 'x': x, 'y': y, 'tag': tag})
                except ValueError:
                    continue
    
    # Sort elements by position (top to bottom, left to right)
    elements.sort(key=lambda e: (e['y'], e['x']))
    
    # Check for overlaps and adjust
    MIN_VERTICAL_SPACING = 20
    MIN_HORIZONTAL_SPACING = 30
    
    for i in range(1, len(elements)):
        prev = elements[i-1]
        curr = elements[i]
        
        # Check vertical overlap
        if abs(curr['y'] - prev['y']) < MIN_VERTICAL_SPACING and abs(curr['x'] - prev['x']) < MIN_HORIZONTAL_SPACING:
            # Adjust current element position
            new_y = prev['y'] + MIN_VERTICAL_SPACING
            
            # Update in SVG content
            old_match = curr['match'].group(0)
            if 'cy=' in old_match:
                new_match = re.sub(r'cy="[^"]*"', f'cy="{new_y}"', old_match)
            else:
                new_match = re.sub(r'y="[^"]*"', f'y="{new_y}"', old_match)
            
            svg_content = svg_content.replace(old_match, new_match, 1)
    
    return svg_content

def fix_mermaid_container(content):
    """Fix Mermaid diagram containers to prevent overlaps and excessive spacing."""
    
    # Pattern for Mermaid containers
    mermaid_patterns = [
        (r'<div class="mermaid-converted"[^>]*>(.*?)</div>\s*(?=<(?:div|section|p|h[1-6]|article|footer))', 'mermaid-converted'),
        (r'<div class="mermaid"[^>]*>(.*?)</div>\s*(?=<(?:div|section|p|h[1-6]|article|footer))', 'mermaid'),
        (r'<div class="mermaid-container"[^>]*>(.*?)</div>\s*(?=<(?:div|section|p|h[1-6]|article|footer))', 'mermaid-container'),
        (r'<div class="mermaid-diagram"[^>]*>(.*?)</div>\s*(?=<(?:div|section|p|h[1-6]|article|footer))', 'mermaid-diagram'),
    ]
    
    for pattern, container_class in mermaid_patterns:
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        for match in reversed(matches):  # Process in reverse to maintain positions
            original = match.group(0)
            inner_content = match.group(1)
            
            # Process SVG content within the container
            if '<svg' in inner_content:
                # Fix decision blocks and overlaps
                inner_content = standardize_decision_blocks(inner_content)
                inner_content = fix_overlapping_elements(inner_content)
                
                # Clean up excessive whitespace within SVG
                inner_content = re.sub(r'\n\s*\n\s*\n+', '\n', inner_content)
            
            # Create properly styled container with no excessive bottom margin
            styled_container = f'''<div class="{container_class}" style="margin: 1.5rem auto 0; padding: 1rem; text-align: center; overflow: visible; max-width: 100%; min-height: auto;">
{inner_content.strip()}
</div>'''
            
            # Remove any excessive whitespace after the container
            content = content[:match.start()] + styled_container + re.sub(r'^\s*\n+', '\n', content[match.end():], count=1)
    
    return content

def fix_svg_viewbox_and_size(content):
    """Ensure SVGs have proper viewBox and sizing to prevent cutoff."""
    
    svg_pattern = r'<svg([^>]*?)>(.*?)</svg>'
    
    def fix_svg(match):
        attrs = match.group(1)
        inner = match.group(2)
        
        # Process the inner content
        inner = standardize_decision_blocks(inner)
        inner = fix_overlapping_elements(inner)
        
        # Extract or calculate dimensions
        width_match = re.search(r'width="(\d+)"', attrs)
        height_match = re.search(r'height="(\d+)"', attrs)
        viewbox_match = re.search(r'viewBox="([^"]*)"', attrs)
        
        # If no viewBox, try to calculate from content
        if not viewbox_match and (width_match and height_match):
            width = width_match.group(1)
            height = height_match.group(1)
            
            # Add some padding to the viewBox to prevent cutoff
            padding = 20
            viewbox = f"-{padding} -{padding} {int(width) + 2*padding} {int(height) + 2*padding}"
            attrs = re.sub(r'viewBox="[^"]*"', '', attrs)  # Remove old viewBox if exists
            attrs += f' viewBox="{viewbox}"'
        
        # Ensure proper sizing style
        if 'style=' not in attrs:
            attrs += ' style="max-width: 100%; height: auto; display: block; margin: 0 auto;"'
        else:
            # Update existing style
            style_match = re.search(r'style="([^"]*)"', attrs)
            if style_match:
                style = style_match.group(1)
                if 'max-width' not in style:
                    style += '; max-width: 100%'
                if 'height' not in style:
                    style += '; height: auto'
                if 'display' not in style:
                    style += '; display: block'
                if 'margin' not in style:
                    style += '; margin: 0 auto'
                attrs = re.sub(r'style="[^"]*"', f'style="{style}"', attrs)
        
        return f'<svg{attrs}>{inner}</svg>'
    
    content = re.sub(svg_pattern, fix_svg, content, flags=re.DOTALL)
    
    return content

def remove_excessive_bottom_spacing(content):
    """Specifically target and remove excessive spacing after Mermaid diagrams."""
    
    # Remove multiple newlines after Mermaid containers
    patterns = [
        # After mermaid divs
        (r'(</div><!--[^>]*mermaid[^>]*-->)\s*\n{3,}', r'\1\n'),
        (r'(<div class="[^"]*mermaid[^"]*"[^>]*>.*?</div>)\s*\n{3,}', r'\1\n'),
        
        # After SVGs
        (r'(</svg>)\s*\n{3,}', r'\1\n'),
        
        # Multiple blank lines in general
        (r'\n\s*\n\s*\n+', r'\n\n'),
        
        # Excessive spacing before next section
        (r'(</div>)\s*\n{4,}(<(?:h[1-6]|section|div|p))', r'\1\n\n\2'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)
    
    return content

def add_mermaid_specific_styles(content):
    """Add or update styles specifically for Mermaid diagrams."""
    
    mermaid_styles = '''
<style>
/* Mermaid Diagram Specific Styles */
.mermaid-converted,
.mermaid,
.mermaid-container,
.mermaid-diagram {
    margin: 1.5rem auto 0 !important;
    margin-bottom: 0 !important;
    padding: 1rem !important;
    text-align: center !important;
    overflow: visible !important;
    max-width: 100% !important;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    box-sizing: border-box;
}

/* Ensure next element doesn't have excessive top margin */
.mermaid-converted + *,
.mermaid + *,
.mermaid-container + *,
.mermaid-diagram + * {
    margin-top: 1.5rem !important;
}

/* SVG within Mermaid containers */
.mermaid-converted svg,
.mermaid svg,
.mermaid-container svg,
.mermaid-diagram svg {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
    overflow: visible !important;
}

/* Standardized decision diamonds */
polygon.decision,
.decision-node polygon,
polygon[class*="decision"] {
    fill: #fff3cd !important;
    stroke: #856404 !important;
    stroke-width: 2px !important;
}

/* Prevent text overlap */
text {
    pointer-events: none;
    z-index: 1000;
}

/* Fix for overlapping elements */
rect, circle, polygon, ellipse {
    pointer-events: all;
}

/* Remove any default margins that might cause issues */
.mermaid-converted > :last-child,
.mermaid > :last-child,
.mermaid-container > :last-child,
.mermaid-diagram > :last-child {
    margin-bottom: 0 !important;
}

/* Ensure proper spacing between consecutive diagrams */
.mermaid-converted + .mermaid-converted,
.mermaid + .mermaid,
.mermaid-container + .mermaid-container,
.mermaid-diagram + .mermaid-diagram {
    margin-top: 2rem !important;
}
</style>
'''
    
    # Remove old Mermaid styles if they exist
    content = re.sub(r'<style>\s*/\*.*?Mermaid.*?\*/.*?</style>', '', content, flags=re.DOTALL)
    
    # Add new styles before closing </head> tag
    if '</head>' in content:
        content = content.replace('</head>', mermaid_styles + '\n</head>')
    
    return content

def process_file(filepath):
    """Process a single HTML file to fix Mermaid diagrams."""
    
    try:
        print(f"\nProcessing: {os.path.basename(filepath)}")
        
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has Mermaid content
        if not has_mermaid_content(content):
            print(f"  ⚬ No Mermaid diagrams found - skipping")
            return False
        
        print(f"  ✓ Mermaid content detected")
        
        # Create backup
        backup_path = filepath + '.mermaid_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Backup created: {os.path.basename(backup_path)}")
        
        # Apply all fixes
        original_length = len(content)
        
        # Apply fixes in specific order
        content = fix_mermaid_container(content)
        content = fix_svg_viewbox_and_size(content)
        content = remove_excessive_bottom_spacing(content)
        content = add_mermaid_specific_styles(content)
        
        # Final cleanup
        content = re.sub(r'\n{4,}', '\n\n\n', content)  # No more than 3 consecutive newlines
        
        # Write the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        new_length = len(content)
        
        # Analysis
        svg_count = content.count('<svg')
        polygon_count = content.count('<polygon')
        mermaid_div_count = sum(content.count(x) for x in ['mermaid-converted', 'class="mermaid"', 'mermaid-container', 'mermaid-diagram'])
        
        print(f"  ✓ Fixed successfully")
        print(f"    • Size: {original_length:,} → {new_length:,} bytes")
        print(f"    • Mermaid containers: {mermaid_div_count}")
        print(f"    • SVG elements: {svg_count}")
        print(f"    • Diamond shapes: {polygon_count}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to process all 02module files with Mermaid diagrams."""
    
    print("=" * 70)
    print("Mermaid Diagram Fix Script for 02module Files")
    print("=" * 70)
    
    # Get base path
    base_path = get_base_path()
    module_path = os.path.join(base_path, "02module")
    
    print(f"Base path: {base_path}")
    print(f"Module path: {module_path}")
    
    if not os.path.exists(module_path):
        print(f"\n✗ Error: Module path not found: {module_path}")
        return
    
    # Get all HTML files in 02module (excluding backups)
    html_files = [
        f for f in os.listdir(module_path) 
        if f.endswith('.html') and not f.endswith('.backup') and not f.endswith('.mermaid_backup')
    ]
    
    print(f"\nFound {len(html_files)} HTML files in 02module")
    print("-" * 70)
    
    fixed_count = 0
    mermaid_files = []
    
    # Process each file
    for filename in sorted(html_files):
        filepath = os.path.join(module_path, filename)
        
        # Quick check for Mermaid content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if has_mermaid_content(content):
            mermaid_files.append(filename)
            if process_file(filepath):
                fixed_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"  Total files scanned: {len(html_files)}")
    print(f"  Files with Mermaid diagrams: {len(mermaid_files)}")
    print(f"  Files successfully fixed: {fixed_count}")
    
    if mermaid_files:
        print(f"\nFiles with Mermaid diagrams that were processed:")
        for fname in mermaid_files:
            status = "✓" if fname in [f for f in mermaid_files if process_file] else "✗"
            print(f"  {status} {fname}")
    
    print("\n" + "=" * 70)
    print("✓ Mermaid diagram fixing complete!")
    print("\nNext steps:")
    print("1. Clear browser cache (Ctrl+Shift+Delete)")
    print("2. Hard refresh the pages (Ctrl+F5)")
    print("3. Check that decision blocks are diamond-shaped")
    print("4. Verify no overlapping elements")
    print("5. Confirm no excessive bottom spacing")

if __name__ == "__main__":
    main()
