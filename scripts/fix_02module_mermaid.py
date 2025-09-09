#!/usr/bin/env python3
"""
Script to fix/repair Mermaid diagrams in 02module HTML files.
Converts Mermaid code blocks to inline SVG with CSS styling.
Changes are isolated to 02module files only.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil

def create_flowchart_svg(mermaid_content):
    """
    Convert Mermaid flowchart syntax to inline SVG.
    This is a simplified converter for common flowchart patterns.
    """
    # Extract nodes and connections from mermaid content
    nodes = {}
    connections = []
    
    # Common patterns in the mermaid content
    node_pattern = r'([A-Z0-9]+)\[(.*?)\]'
    connection_pattern = r'([A-Z0-9]+)\s*-->\s*([A-Z0-9]+)'
    
    # Find all nodes
    for match in re.finditer(node_pattern, mermaid_content):
        node_id = match.group(1)
        node_text = match.group(2).strip('"').strip("'")
        nodes[node_id] = node_text
    
    # Find all connections
    for match in re.finditer(connection_pattern, mermaid_content):
        from_node = match.group(1)
        to_node = match.group(2)
        connections.append((from_node, to_node))
    
    # If no nodes found, return a placeholder
    if not nodes:
        return create_placeholder_svg("Diagram content could not be parsed")
    
    # Calculate positions for nodes
    node_positions = calculate_node_positions(nodes, connections)
    
    # Generate SVG
    svg_width = 800
    svg_height = max(400, len(nodes) * 80)
    
    svg = f'''<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
    <defs>
        <style>
            .mermaid-node {{
                fill: #e3f2fd;
                stroke: #2196f3;
                stroke-width: 2;
            }}
            .mermaid-node-text {{
                fill: #333;
                font-family: Arial, sans-serif;
                font-size: 14px;
                text-anchor: middle;
                dominant-baseline: middle;
            }}
            .mermaid-arrow {{
                stroke: #666;
                stroke-width: 2;
                fill: none;
                marker-end: url(#arrowhead);
            }}
            .mermaid-title {{
                fill: #333;
                font-family: Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                text-anchor: middle;
            }}
        </style>
        <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#666"/>
        </marker>
    </defs>
'''
    
    # Draw connections first (so they appear behind nodes)
    for from_node, to_node in connections:
        if from_node in node_positions and to_node in node_positions:
            x1, y1 = node_positions[from_node]
            x2, y2 = node_positions[to_node]
            svg += f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="mermaid-arrow"/>\n'
    
    # Draw nodes
    for node_id, (x, y) in node_positions.items():
        if node_id in nodes:
            text = nodes[node_id]
            # Calculate text width (approximate)
            text_width = len(text) * 8 + 40
            text_height = 40
            
            svg += f'''    <rect x="{x - text_width//2}" y="{y - text_height//2}" width="{text_width}" height="{text_height}" rx="5" class="mermaid-node"/>
    <text x="{x}" y="{y}" class="mermaid-node-text">{escape_html(text)}</text>
'''
    
    svg += '</svg>'
    return svg

def calculate_node_positions(nodes, connections):
    """Calculate positions for nodes in a flowchart layout."""
    positions = {}
    
    # Simple layout: arrange nodes in levels
    levels = {}
    processed = set()
    
    # Find root nodes (nodes with no incoming connections)
    all_targets = {conn[1] for conn in connections}
    roots = [node for node in nodes if node not in all_targets]
    
    if not roots:
        # If no clear root, use first node
        roots = [list(nodes.keys())[0]] if nodes else []
    
    # Assign levels using BFS
    current_level = 0
    current_nodes = roots
    
    while current_nodes:
        for node in current_nodes:
            if node not in processed:
                if current_level not in levels:
                    levels[current_level] = []
                levels[current_level].append(node)
                processed.add(node)
        
        # Find next level nodes
        next_nodes = []
        for from_node, to_node in connections:
            if from_node in current_nodes and to_node not in processed:
                next_nodes.append(to_node)
        
        current_nodes = next_nodes
        current_level += 1
    
    # Add any remaining nodes
    for node in nodes:
        if node not in processed:
            if current_level not in levels:
                levels[current_level] = []
            levels[current_level].append(node)
    
    # Calculate positions based on levels
    y_spacing = 100
    x_center = 400
    
    for level, level_nodes in levels.items():
        y = 50 + level * y_spacing
        x_spacing = 600 / (len(level_nodes) + 1)
        
        for i, node in enumerate(level_nodes):
            x = 100 + (i + 1) * x_spacing
            positions[node] = (x, y)
    
    return positions

def create_placeholder_svg(message="Mermaid Diagram"):
    """Create a placeholder SVG for diagrams that can't be converted."""
    return f'''<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
    <rect x="10" y="10" width="580" height="180" rx="10" fill="#f5f5f5" stroke="#ddd" stroke-width="2"/>
    <text x="300" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#666">
        {escape_html(message)}
    </text>
    <text x="300" y="130" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#999">
        (Diagram visualization placeholder)
    </text>
</svg>'''

def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def convert_mermaid_to_svg(html_content):
    """
    Find and convert all Mermaid diagram blocks to inline SVG.
    """
    converted_count = 0
    
    # Pattern to find mermaid blocks
    patterns = [
        # Pattern 1: <div class="mermaid">content</div>
        (r'<div\s+class="mermaid"[^>]*>(.*?)</div>', re.DOTALL),
        # Pattern 2: <div class="mermaid-diagram">...<div class="mermaid">content</div>...</div>
        (r'<div\s+class="mermaid-diagram"[^>]*>.*?<div\s+class="mermaid"[^>]*>(.*?)</div>.*?</div>', re.DOTALL),
        # Pattern 3: <pre class="mermaid">content</pre>
        (r'<pre\s+class="mermaid"[^>]*>(.*?)</pre>', re.DOTALL),
    ]
    
    for pattern, flags in patterns:
        matches = list(re.finditer(pattern, html_content, flags))
        
        for match in reversed(matches):  # Process from end to maintain positions
            mermaid_content = match.group(1)
            
            # Clean the mermaid content
            mermaid_content = re.sub(r'<[^>]+>', '', mermaid_content)  # Remove HTML tags
            mermaid_content = mermaid_content.strip()
            
            if mermaid_content:
                # Determine diagram type and convert
                if 'flowchart' in mermaid_content.lower() or '-->' in mermaid_content:
                    svg = create_flowchart_svg(mermaid_content)
                else:
                    # For other diagram types, create a placeholder
                    svg = create_placeholder_svg("Mermaid Diagram")
                
                # Wrap SVG in a container div
                svg_container = f'''<div class="mermaid-svg-container" style="margin: 20px 0;">
    {svg}
</div>'''
                
                # Replace the mermaid block with SVG
                html_content = html_content[:match.start()] + svg_container + html_content[match.end():]
                converted_count += 1
    
    # Also handle any remaining mermaid script imports and initialization
    # Remove mermaid CDN imports
    html_content = re.sub(
        r'<script[^>]*mermaid[^>]*>.*?</script>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Remove mermaid initialization scripts
    html_content = re.sub(
        r'<script[^>]*>.*?mermaid\.initialize.*?</script>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    return html_content, converted_count

def add_module_specific_styles(html_content):
    """
    Add module-specific styles for the converted SVG diagrams.
    These styles are scoped to not affect other documents.
    """
    # Check if we already have the styles
    if 'mermaid-svg-module-styles' in html_content:
        return html_content
    
    # Module-specific styles
    module_styles = '''
    <!-- Module 02 Mermaid SVG Styles -->
    <style id="mermaid-svg-module-styles">
        /* Styles specific to Module 02 Mermaid diagrams */
        .lesson-body .mermaid-svg-container {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .lesson-body .mermaid-svg-container svg {
            background: white;
            border-radius: 4px;
            padding: 10px;
        }
        
        /* Ensure diagrams are responsive */
        .lesson-body .mermaid-svg-container svg {
            max-width: 100%;
            height: auto;
        }
        
        /* Style for diagram titles if any */
        .lesson-body .diagram-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
    </style>
'''
    
    # Add styles before closing </head> tag
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', module_styles + '\n</head>')
    
    return html_content

def process_file(file_path):
    """Process a single HTML file to fix Mermaid diagrams."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has mermaid content
        if 'mermaid' not in content.lower():
            return False, "No Mermaid content found"
        
        # Convert Mermaid to SVG
        modified_content, converted_count = convert_mermaid_to_svg(content)
        
        if converted_count == 0:
            return False, "No Mermaid diagrams to convert"
        
        # Add module-specific styles
        modified_content = add_module_specific_styles(modified_content)
        
        # Write the modified content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        return True, f"Converted {converted_count} Mermaid diagram(s) to SVG"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def backup_directory(dir_path):
    """Create a backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = dir_path.parent / f"{dir_path.name}_mermaid_backup_{timestamp}"
    
    print(f"Creating backup at: {backup_path.name}")
    try:
        shutil.copytree(str(dir_path), str(backup_path))
        print("✓ Backup created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating backup: {e}")
        return False

def main():
    """Main function to process all files in 02module."""
    
    # Define the path to 02module
    module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    
    # Check if directory exists
    if not module_dir.exists():
        # Try alternative path
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
        
        if not module_dir.exists():
            print("Error: 02module directory not found")
            print("Please ensure the path exists: \\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module")
            return
    
    print("=" * 60)
    print("Mermaid Diagram Fix Script for Module 02")
    print("=" * 60)
    print(f"Target directory: {module_dir}")
    print()
    
    # Create backup
    response = input("Create backup before proceeding? (recommended) (y/n): ")
    if response.lower() == 'y':
        if not backup_directory(module_dir):
            response = input("Backup failed. Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Exiting...")
                return
    
    # Get all HTML files
    html_files = list(module_dir.glob("*.html"))
    
    if not html_files:
        print("No HTML files found in 02module")
        return
    
    print(f"\nFound {len(html_files)} HTML files")
    print("Scanning for Mermaid diagrams...")
    print("=" * 60)
    
    fixed = 0
    skipped = 0
    failed = 0
    
    for file_path in sorted(html_files):
        print(f"\nProcessing: {file_path.name}")
        success, message = process_file(file_path)
        
        if success:
            print(f"  ✓ {message}")
            fixed += 1
        elif "No Mermaid" in message:
            print(f"  - {message}")
            skipped += 1
        else:
            print(f"  ✗ {message}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Fixed: {fixed} files")
    print(f"  Skipped: {skipped} files (no Mermaid content)")
    print(f"  Failed: {failed} files")
    print(f"  Total: {len(html_files)} files")
    
    if fixed > 0:
        print("\n✨ Mermaid diagrams have been converted to inline SVG!")
        print("\nThe changes:")
        print("  • Converted Mermaid code blocks to inline SVG")
        print("  • Added module-specific styles")
        print("  • Removed Mermaid CDN dependencies")
        print("  • Made diagrams self-contained and responsive")
        print("\nThese changes only affect the 02module files.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    
    input("\nPress Enter to exit...")
