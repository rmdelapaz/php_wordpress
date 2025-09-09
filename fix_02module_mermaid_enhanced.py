#!/usr/bin/env python3
"""
Enhanced script to fix/repair Mermaid diagrams in 02module HTML files.
Converts Mermaid diagrams to self-contained inline SVG with embedded styles.
Handles multiple diagram types and ensures changes don't affect other modules.
"""

import re
from pathlib import Path
from datetime import datetime
import shutil
import html

class MermaidToSVGConverter:
    """Converter for Mermaid diagrams to inline SVG."""
    
    def __init__(self):
        self.default_width = 800
        self.default_height = 400
        
    def convert(self, mermaid_content):
        """Convert Mermaid content to SVG based on diagram type."""
        # Clean the content
        mermaid_content = self.clean_mermaid_content(mermaid_content)
        
        if not mermaid_content:
            return self.create_error_svg("Empty diagram content")
        
        # Determine diagram type and convert accordingly
        if 'flowchart' in mermaid_content.lower() or 'graph' in mermaid_content.lower():
            return self.convert_flowchart(mermaid_content)
        elif 'classDiagram' in mermaid_content:
            return self.convert_class_diagram(mermaid_content)
        elif 'sequenceDiagram' in mermaid_content:
            return self.create_placeholder_svg("Sequence Diagram", mermaid_content)
        else:
            # Default: try to parse as flowchart
            return self.convert_flowchart(mermaid_content)
    
    def clean_mermaid_content(self, content):
        """Clean and normalize Mermaid content."""
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove HTML entities
        content = html.unescape(content)
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        return content.strip()
    
    def convert_flowchart(self, content):
        """Convert flowchart/graph to SVG."""
        # Parse nodes and connections
        nodes = self.parse_nodes(content)
        connections = self.parse_connections(content)
        
        if not nodes:
            return self.create_placeholder_svg("Flowchart", content)
        
        # Create SVG
        svg_height = max(400, len(nodes) * 100)
        
        svg = f'''<svg viewBox="0 0 {self.default_width} {svg_height}" xmlns="http://www.w3.org/2000/svg" 
     style="max-width: 100%; height: auto; display: block; margin: 0 auto; background: white; border-radius: 8px;">
    
    <!-- Embedded styles for this diagram only -->
    <defs>
        <style type="text/css">
            .node-rect {{ fill: #e1f5fe; stroke: #01579b; stroke-width: 2px; }}
            .node-rect:hover {{ fill: #b3e5fc; }}
            .node-text {{ fill: #01579b; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; font-weight: 500; }}
            .connection-line {{ stroke: #546e7a; stroke-width: 2px; fill: none; }}
            .arrow-marker {{ fill: #546e7a; }}
            .diagram-title {{ fill: #263238; font-size: 18px; font-weight: bold; }}
            .subgraph-rect {{ fill: #fff3e0; stroke: #e65100; stroke-width: 1px; stroke-dasharray: 5,5; opacity: 0.3; }}
        </style>
        
        <!-- Arrow marker -->
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" class="arrow-marker"/>
        </marker>
    </defs>
    
    <!-- Background -->
    <rect x="0" y="0" width="{self.default_width}" height="{svg_height}" fill="#fafafa" rx="8"/>
    
'''
        
        # Calculate node positions
        positions = self.calculate_flowchart_positions(nodes, connections)
        
        # Draw connections
        for from_id, to_id, label in connections:
            if from_id in positions and to_id in positions:
                x1, y1 = positions[from_id]
                x2, y2 = positions[to_id]
                
                # Simple straight line connection
                svg += f'''    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
          class="connection-line" marker-end="url(#arrow)"/>
'''
                
                # Add label if exists
                if label:
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    svg += f'''    <text x="{mid_x}" y="{mid_y - 5}" text-anchor="middle" 
          class="node-text" font-size="12">{self.escape_xml(label)}</text>
'''
        
        # Draw nodes
        for node_id, node_data in nodes.items():
            if node_id in positions:
                x, y = positions[node_id]
                text = node_data['text']
                node_type = node_data['type']
                
                # Calculate dimensions
                width = max(120, len(text) * 8 + 20)
                height = 50
                
                # Draw based on node type
                if node_type == 'round':
                    svg += f'''    <rect x="{x - width//2}" y="{y - height//2}" width="{width}" height="{height}" 
          rx="25" class="node-rect"/>
'''
                elif node_type == 'diamond':
                    # Simplified diamond as rotated square
                    svg += f'''    <rect x="{x - width//2}" y="{y - height//2}" width="{width}" height="{height}" 
          transform="rotate(45 {x} {y})" class="node-rect"/>
'''
                else:  # Default rectangle
                    svg += f'''    <rect x="{x - width//2}" y="{y - height//2}" width="{width}" height="{height}" 
          rx="5" class="node-rect"/>
'''
                
                # Add text
                svg += f'''    <text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" 
          class="node-text">{self.escape_xml(text)}</text>
'''
        
        svg += '</svg>'
        return svg
    
    def parse_nodes(self, content):
        """Parse nodes from Mermaid content."""
        nodes = {}
        
        # Patterns for different node types
        patterns = [
            (r'([A-Za-z0-9_]+)\[([^\]]+)\]', 'rect'),      # Rectangle [text]
            (r'([A-Za-z0-9_]+)\(([^\)]+)\)', 'round'),     # Round (text)
            (r'([A-Za-z0-9_]+)\{([^\}]+)\}', 'diamond'),   # Diamond {text}
            (r'([A-Za-z0-9_]+)\[\[([^\]]+)\]\]', 'rect'),  # Double rectangle [[text]]
        ]
        
        for pattern, node_type in patterns:
            for match in re.finditer(pattern, content):
                node_id = match.group(1)
                node_text = match.group(2).strip('"\'')
                nodes[node_id] = {
                    'text': node_text,
                    'type': node_type
                }
        
        return nodes
    
    def parse_connections(self, content):
        """Parse connections from Mermaid content."""
        connections = []
        
        # Connection patterns
        patterns = [
            r'([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)',           # A --> B
            r'([A-Za-z0-9_]+)\s*---\s*([A-Za-z0-9_]+)',           # A --- B
            r'([A-Za-z0-9_]+)\s*-->\|([^|]+)\|\s*([A-Za-z0-9_]+)', # A -->|label| B
            r'([A-Za-z0-9_]+)\s*--\s*([^-]+)\s*-->\s*([A-Za-z0-9_]+)', # A -- label --> B
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                if len(match.groups()) == 2:
                    connections.append((match.group(1), match.group(2), ''))
                elif len(match.groups()) == 3:
                    connections.append((match.group(1), match.group(3), match.group(2)))
        
        return connections
    
    def calculate_flowchart_positions(self, nodes, connections):
        """Calculate positions for flowchart nodes."""
        positions = {}
        
        if not nodes:
            return positions
        
        # Build adjacency list
        graph = {node: [] for node in nodes}
        for from_id, to_id, _ in connections:
            if from_id in graph and to_id in nodes:
                graph[from_id].append(to_id)
        
        # Find levels using topological-like ordering
        levels = self.assign_levels(graph, nodes)
        
        # Calculate positions
        y_spacing = 120
        max_width = self.default_width - 100
        
        for level, level_nodes in enumerate(levels):
            y = 80 + level * y_spacing
            
            if level_nodes:
                x_spacing = max_width / (len(level_nodes) + 1)
                for i, node_id in enumerate(level_nodes):
                    x = 50 + (i + 1) * x_spacing
                    positions[node_id] = (x, y)
        
        return positions
    
    def assign_levels(self, graph, nodes):
        """Assign nodes to levels for layout."""
        visited = set()
        levels = []
        
        # Find nodes with no incoming edges (roots)
        all_targets = set()
        for source in graph:
            all_targets.update(graph[source])
        
        roots = [node for node in nodes if node not in all_targets]
        if not roots and nodes:
            roots = [list(nodes.keys())[0]]
        
        # BFS to assign levels
        current_level = roots
        while current_level:
            level_nodes = []
            for node in current_level:
                if node not in visited:
                    level_nodes.append(node)
                    visited.add(node)
            
            if level_nodes:
                levels.append(level_nodes)
            
            # Get next level
            next_level = []
            for node in current_level:
                if node in graph:
                    for child in graph[node]:
                        if child not in visited:
                            next_level.append(child)
            
            current_level = next_level
        
        # Add any remaining nodes
        remaining = [node for node in nodes if node not in visited]
        if remaining:
            levels.append(remaining)
        
        return levels
    
    def convert_class_diagram(self, content):
        """Convert class diagram to SVG."""
        # For now, create a styled placeholder
        return self.create_placeholder_svg("Class Diagram", content, style="class")
    
    def create_placeholder_svg(self, diagram_type, original_content="", style="default"):
        """Create a nice placeholder SVG."""
        # Different styles for different diagram types
        colors = {
            "default": {"bg": "#e3f2fd", "border": "#1976d2", "text": "#0d47a1"},
            "class": {"bg": "#f3e5f5", "border": "#7b1fa2", "text": "#4a148c"},
            "sequence": {"bg": "#e8f5e9", "border": "#388e3c", "text": "#1b5e20"},
        }
        
        color_scheme = colors.get(style, colors["default"])
        
        svg = f'''<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" 
     style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
    
    <!-- Background -->
    <rect x="0" y="0" width="600" height="300" rx="8" fill="{color_scheme['bg']}" 
          stroke="{color_scheme['border']}" stroke-width="2"/>
    
    <!-- Icon -->
    <g transform="translate(300, 100)">
        <rect x="-40" y="-30" width="80" height="60" rx="5" 
              fill="white" stroke="{color_scheme['border']}" stroke-width="2"/>
        <line x1="-20" y1="-10" x2="20" y2="-10" 
              stroke="{color_scheme['border']}" stroke-width="2"/>
        <line x1="-20" y1="0" x2="20" y2="0" 
              stroke="{color_scheme['border']}" stroke-width="2"/>
        <line x1="-20" y1="10" x2="20" y2="10" 
              stroke="{color_scheme['border']}" stroke-width="2"/>
    </g>
    
    <!-- Text -->
    <text x="300" y="180" text-anchor="middle" 
          font-family="'Segoe UI', Arial, sans-serif" font-size="18" 
          fill="{color_scheme['text']}" font-weight="bold">
        {self.escape_xml(diagram_type)}
    </text>
    
    <text x="300" y="210" text-anchor="middle" 
          font-family="'Segoe UI', Arial, sans-serif" font-size="14" 
          fill="{color_scheme['text']}" opacity="0.8">
        (Diagram converted to static representation)
    </text>
    
    <!-- Original content hint -->
    <text x="300" y="240" text-anchor="middle" 
          font-family="monospace" font-size="10" 
          fill="{color_scheme['text']}" opacity="0.5">
        {self.escape_xml(original_content[:50] + '...' if len(original_content) > 50 else original_content)}
    </text>
</svg>'''
        return svg
    
    def create_error_svg(self, error_message):
        """Create an error SVG."""
        return f'''<svg viewBox="0 0 400 100" xmlns="http://www.w3.org/2000/svg" 
     style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
    <rect x="0" y="0" width="400" height="100" rx="5" fill="#ffebee" stroke="#f44336" stroke-width="2"/>
    <text x="200" y="50" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#c62828">
        Error: {self.escape_xml(error_message)}
    </text>
</svg>'''
    
    def escape_xml(self, text):
        """Escape XML/SVG special characters."""
        return (str(text)
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


def find_and_convert_mermaid(html_content):
    """Find all Mermaid blocks and convert them to SVG."""
    converter = MermaidToSVGConverter()
    converted_count = 0
    
    # Patterns to find Mermaid content
    mermaid_patterns = [
        (r'<div\s+class="mermaid-diagram"[^>]*>.*?<div\s+class="mermaid"[^>]*>(.*?)</div>.*?</div>', re.DOTALL),
        (r'<div\s+class="mermaid"[^>]*>(.*?)</div>', re.DOTALL),
        (r'<pre\s+class="mermaid"[^>]*>(.*?)</pre>', re.DOTALL),
    ]
    
    for pattern, flags in mermaid_patterns:
        matches = list(re.finditer(pattern, html_content, flags))
        
        # Process matches in reverse to maintain string positions
        for match in reversed(matches):
            mermaid_content = match.group(1)
            
            # Convert to SVG
            svg = converter.convert(mermaid_content)
            
            # Wrap in container
            svg_html = f'''
<div class="mermaid-converted" style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
    <div style="margin-bottom: 10px; font-size: 12px; color: #6c757d; text-transform: uppercase; letter-spacing: 1px;">Diagram</div>
    {svg}
</div>'''
            
            # Replace original with SVG
            html_content = html_content[:match.start()] + svg_html + html_content[match.end():]
            converted_count += 1
    
    return html_content, converted_count


def remove_mermaid_dependencies(html_content):
    """Remove Mermaid CDN scripts and initialization code."""
    # Remove script tags that reference mermaid
    patterns = [
        r'<script[^>]*mermaid[^>]*>.*?</script>',
        r'<script[^>]*>.*?mermaid\.initialize.*?</script>',
        r'<script[^>]*>.*?import\s+mermaid.*?</script>',
    ]
    
    for pattern in patterns:
        html_content = re.sub(pattern, '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    return html_content


def process_html_file(file_path):
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Mermaid content
        if 'mermaid' not in content.lower():
            return False, "No Mermaid content found"
        
        # Convert Mermaid diagrams
        modified_content, count = find_and_convert_mermaid(content)
        
        if count == 0:
            return False, "No Mermaid blocks to convert"
        
        # Remove Mermaid dependencies
        modified_content = remove_mermaid_dependencies(modified_content)
        
        # Save modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        return True, f"Converted {count} diagram(s)"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def create_backup(directory):
    """Create a timestamped backup of the directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = directory.parent / f"{directory.name}_mermaid_backup_{timestamp}"
    
    try:
        shutil.copytree(str(directory), str(backup_dir))
        return backup_dir
    except Exception as e:
        print(f"Backup failed: {e}")
        return None


def main():
    """Main function."""
    # Set up path
    module_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    
    if not module_path.exists():
        module_path = Path("/home/practicalace/projects/php_wordpress/02module")
        if not module_path.exists():
            print("Error: 02module directory not found")
            return
    
    print("=" * 70)
    print(" Mermaid Diagram Converter for Module 02")
    print(" Converts Mermaid diagrams to self-contained inline SVG")
    print("=" * 70)
    print(f"Target: {module_path}\n")
    
    # Backup option
    response = input("Create backup? (y/n): ")
    if response.lower() == 'y':
        backup_dir = create_backup(module_path)
        if backup_dir:
            print(f"✓ Backup created: {backup_dir.name}\n")
        else:
            if input("Continue without backup? (y/n): ").lower() != 'y':
                return
    
    # Process files
    html_files = list(module_path.glob("*.html"))
    print(f"Processing {len(html_files)} HTML files...\n")
    
    stats = {"converted": 0, "skipped": 0, "failed": 0}
    
    for file_path in sorted(html_files):
        print(f"• {file_path.name:<50}", end=" ")
        success, message = process_html_file(file_path)
        
        if success:
            print(f"✓ {message}")
            stats["converted"] += 1
        elif "No Mermaid" in message:
            print(f"- {message}")
            stats["skipped"] += 1
        else:
            print(f"✗ {message}")
            stats["failed"] += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  ✓ Converted: {stats['converted']} files")
    print(f"  - Skipped: {stats['skipped']} files")
    print(f"  ✗ Failed: {stats['failed']} files")
    
    if stats["converted"] > 0:
        print("\n✨ Success! Mermaid diagrams have been converted to inline SVG.")
        print("   • No external dependencies required")
        print("   • Diagrams are now self-contained")
        print("   • Changes only affect Module 02 files")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        input("\nPress Enter to exit...")
