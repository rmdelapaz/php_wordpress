#!/usr/bin/env python3
"""
Fix Mermaid diagrams by converting them to inline SVG or adding proper styling.
This script handles Mermaid diagram display issues in HTML files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Base path for WSL
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"

# Mermaid diagram conversions (simplified examples - can be expanded)
MERMAID_CONVERSIONS = {
    "bootstrap_grid": """<div class="grid-structure-diagram">
    <svg viewBox="0 0 800 400" width="100%" height="400">
        <!-- Main container -->
        <rect x="50" y="20" width="700" height="360" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2" rx="10" ry="10"/>
        
        <!-- Title -->
        <text x="400" y="50" text-anchor="middle" font-size="20" font-weight="bold" fill="#7952b3">Bootstrap Grid System</text>
        
        <!-- Container Box -->
        <rect x="100" y="80" width="200" height="60" fill="#9766e1" stroke="#333" stroke-width="2" rx="5" ry="5"/>
        <text x="200" y="115" text-anchor="middle" fill="white" font-size="16">Container</text>
        
        <!-- Row Box -->
        <rect x="100" y="170" width="200" height="60" fill="#9766e1" stroke="#333" stroke-width="2" rx="5" ry="5"/>
        <text x="200" y="205" text-anchor="middle" fill="white" font-size="16">Row</text>
        
        <!-- Columns Box -->
        <rect x="100" y="260" width="200" height="60" fill="#9766e1" stroke="#333" stroke-width="2" rx="5" ry="5"/>
        <text x="200" y="295" text-anchor="middle" fill="white" font-size="16">Columns</text>
        
        <!-- Arrows -->
        <path d="M 200 140 L 200 170" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
        <path d="M 200 230 L 200 260" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
        
        <!-- Breakpoints section -->
        <rect x="400" y="80" width="300" height="240" fill="#e9ecef" stroke="#6c757d" stroke-width="1" rx="5" ry="5"/>
        <text x="550" y="105" text-anchor="middle" font-size="16" font-weight="bold" fill="#495057">Breakpoints</text>
        
        <!-- Individual breakpoints -->
        <text x="420" y="135" font-size="14" fill="#495057">• xs - Extra small: &lt;576px</text>
        <text x="420" y="160" font-size="14" fill="#495057">• sm - Small: ≥576px</text>
        <text x="420" y="185" font-size="14" fill="#495057">• md - Medium: ≥768px</text>
        <text x="420" y="210" font-size="14" fill="#495057">• lg - Large: ≥992px</text>
        <text x="420" y="235" font-size="14" fill="#495057">• xl - Extra large: ≥1200px</text>
        <text x="420" y="260" font-size="14" fill="#495057">• xxl - Extra extra large: ≥1400px</text>
        
        <!-- Additional features -->
        <text x="420" y="290" font-size="14" font-weight="bold" fill="#495057">Features:</text>
        <text x="420" y="310" font-size="14" fill="#495057">• Gutters (spacing)</text>
        <text x="420" y="330" font-size="14" fill="#495057">• Alignment Options</text>
        
        <!-- Arrow marker definition -->
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
            </marker>
        </defs>
    </svg>
</div>"""
}

def find_mermaid_diagrams(content: str) -> List[Tuple[str, int, int]]:
    """
    Find all Mermaid diagram blocks in the content.
    Returns list of (diagram_content, start_pos, end_pos).
    """
    diagrams = []
    
    # Pattern to find mermaid blocks
    pattern = r'<div class="mermaid-container">.*?<pre class="mermaid">.*?</pre>.*?</div>'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        diagrams.append((match.group(0), match.start(), match.end()))
    
    # Also check for simple mermaid blocks
    pattern2 = r'<pre class="mermaid">.*?</pre>'
    matches2 = re.finditer(pattern2, content, re.DOTALL)
    
    for match in matches2:
        # Check if this isn't already part of a found diagram
        is_duplicate = False
        for _, start, end in diagrams:
            if match.start() >= start and match.end() <= end:
                is_duplicate = True
                break
        
        if not is_duplicate:
            diagrams.append((match.group(0), match.start(), match.end()))
    
    return diagrams

def get_file_key(file_path: str) -> Optional[str]:
    """
    Get a key for looking up conversion based on file name.
    """
    file_name = os.path.basename(file_path)
    name_without_ext = os.path.splitext(file_name)[0]
    
    # Check if we have a specific conversion for this file
    for key in MERMAID_CONVERSIONS:
        if key in name_without_ext:
            return key
    
    return None

def convert_mermaid_to_svg(diagram_content: str, file_key: Optional[str]) -> str:
    """
    Convert a Mermaid diagram to SVG or add proper styling.
    """
    # If we have a specific conversion for this file
    if file_key and file_key in MERMAID_CONVERSIONS:
        return MERMAID_CONVERSIONS[file_key]
    
    # Otherwise, wrap in a properly styled container
    # Extract the mermaid code
    mermaid_code_match = re.search(r'<pre class="mermaid">(.*?)</pre>', diagram_content, re.DOTALL)
    
    if mermaid_code_match:
        mermaid_code = mermaid_code_match.group(1).strip()
        
        # Create a styled container that will work with mermaid.js
        return f'''<div class="mermaid-diagram" style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <pre class="mermaid" style="text-align: center;">
{mermaid_code}
    </pre>
</div>'''
    
    return diagram_content

def fix_mermaid_diagrams(file_path: str) -> bool:
    """
    Fix Mermaid diagrams in a single HTML file.
    Returns True if file was modified, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all mermaid diagrams
        diagrams = find_mermaid_diagrams(content)
        
        if not diagrams:
            print(f"⏭️  Skipped: {os.path.basename(file_path)} - No Mermaid diagrams found")
            return False
        
        # Get file key for specific conversions
        file_key = get_file_key(file_path)
        
        # Process diagrams in reverse order to maintain positions
        modified = False
        for diagram_content, start_pos, end_pos in reversed(diagrams):
            # Convert the diagram
            new_content = convert_mermaid_to_svg(diagram_content, file_key)
            
            if new_content != diagram_content:
                # Replace in content
                content = content[:start_pos] + new_content + content[end_pos:]
                modified = True
        
        if modified:
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed: {os.path.basename(file_path)} - Converted {len(diagrams)} Mermaid diagram(s)")
            return True
        else:
            print(f"⏭️  Skipped: {os.path.basename(file_path)} - Mermaid diagrams already OK")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def add_mermaid_styles(module_path: str) -> bool:
    """
    Add CSS styles for Mermaid diagrams to the module's CSS or inline styles.
    """
    # This would add necessary CSS for Mermaid diagrams
    # For now, we're handling it inline in the conversion
    return True

def process_module(module: str) -> Dict[str, int]:
    """
    Process all HTML files in a module directory for Mermaid fixes.
    """
    module_path = os.path.join(BASE_PATH, module)
    stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
    
    if not os.path.exists(module_path):
        print(f"❌ Module directory not found: {module_path}")
        stats["errors"] = 1
        return stats
    
    print(f"\n📁 Processing module: {module}")
    print("=" * 50)
    
    # Add module-wide Mermaid styles if needed
    add_mermaid_styles(module_path)
    
    # Get all HTML files in the module directory
    html_files = [f for f in os.listdir(module_path) if f.endswith('.html')]
    
    for html_file in sorted(html_files):
        file_path = os.path.join(module_path, html_file)
        stats["processed"] += 1
        
        if fix_mermaid_diagrams(file_path):
            stats["modified"] += 1
        else:
            stats["skipped"] += 1
    
    return stats

def main():
    """
    Main function to process all modules.
    """
    print("🔧 Mermaid Diagram Fixer Script")
    print("=" * 50)
    print(f"Base path: {BASE_PATH}")
    print("=" * 50)
    
    total_stats = {"processed": 0, "modified": 0, "skipped": 0, "errors": 0}
    
    # Process modules 1-6
    modules = [f"{i:02d}module" for i in range(1, 7)]
    
    for module in modules:
        stats = process_module(module)
        
        # Update total stats
        for key in total_stats:
            total_stats[key] += stats[key]
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  Total files processed: {total_stats['processed']}")
    print(f"  Files modified: {total_stats['modified']}")
    print(f"  Files skipped: {total_stats['skipped']}")
    print(f"  Errors: {total_stats['errors']}")
    print("=" * 50)
    print("✅ Mermaid diagram fixing complete!")

if __name__ == "__main__":
    main()
