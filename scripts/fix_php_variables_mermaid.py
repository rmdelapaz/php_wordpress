#!/usr/bin/env python3
"""
Fix mermaid diagrams in php_variables_data_and_operators.html
Replaces broken mermaid diagrams with working inline SVG versions.
"""

import re

def replace_mermaid_diagrams(content):
    """Replace all mermaid diagrams with SVG equivalents"""
    
    # Replacement for first diagram - PHP Building Blocks
    diagram1_svg = '''<div class="mermaid-diagram" style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
        <!-- Title -->
        <text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">PHP Building Blocks</text>
        
        <!-- Main Node -->
        <rect x="320" y="60" width="160" height="50" rx="5" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        <text x="400" y="90" text-anchor="middle" fill="white" font-size="16" font-weight="bold">PHP Building Blocks</text>
        
        <!-- Variables Branch -->
        <rect x="80" y="180" width="120" height="40" rx="5" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
        <text x="140" y="205" text-anchor="middle" fill="white" font-size="14">Variables</text>
        
        <!-- Data Types Branch -->
        <rect x="340" y="180" width="120" height="40" rx="5" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
        <text x="400" y="205" text-anchor="middle" fill="white" font-size="14">Data Types</text>
        
        <!-- Operators Branch -->
        <rect x="600" y="180" width="120" height="40" rx="5" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
        <text x="660" y="205" text-anchor="middle" fill="white" font-size="14">Operators</text>
        
        <!-- Variables sub-items -->
        <rect x="20" y="280" width="90" height="30" rx="3" fill="#E3F2FD" stroke="#2196F3" stroke-width="1"/>
        <text x="65" y="300" text-anchor="middle" font-size="12" fill="#333">Store data</text>
        
        <rect x="20" y="320" width="110" height="30" rx="3" fill="#E3F2FD" stroke="#2196F3" stroke-width="1"/>
        <text x="75" y="340" text-anchor="middle" font-size="12" fill="#333">Named containers</text>
        
        <rect x="20" y="360" width="110" height="30" rx="3" fill="#E3F2FD" stroke="#2196F3" stroke-width="1"/>
        <text x="75" y="380" text-anchor="middle" font-size="12" fill="#333">Dynamic typing</text>
        
        <!-- Data Types sub-items -->
        <rect x="280" y="280" width="100" height="30" rx="3" fill="#FFF3E0" stroke="#FF9800" stroke-width="1"/>
        <text x="330" y="300" text-anchor="middle" font-size="12" fill="#333">Scalar Types</text>
        
        <rect x="280" y="320" width="110" height="30" rx="3" fill="#FFF3E0" stroke="#FF9800" stroke-width="1"/>
        <text x="335" y="340" text-anchor="middle" font-size="12" fill="#333">Compound Types</text>
        
        <rect x="280" y="360" width="100" height="30" rx="3" fill="#FFF3E0" stroke="#FF9800" stroke-width="1"/>
        <text x="330" y="380" text-anchor="middle" font-size="12" fill="#333">Special Types</text>
        
        <!-- Operators sub-items -->
        <rect x="540" y="280" width="80" height="30" rx="3" fill="#F3E5F5" stroke="#9C27B0" stroke-width="1"/>
        <text x="580" y="300" text-anchor="middle" font-size="12" fill="#333">Arithmetic</text>
        
        <rect x="630" y="280" width="85" height="30" rx="3" fill="#F3E5F5" stroke="#9C27B0" stroke-width="1"/>
        <text x="672" y="300" text-anchor="middle" font-size="12" fill="#333">Comparison</text>
        
        <rect x="540" y="320" width="70" height="30" rx="3" fill="#F3E5F5" stroke="#9C27B0" stroke-width="1"/>
        <text x="575" y="340" text-anchor="middle" font-size="12" fill="#333">Logical</text>
        
        <rect x="620" y="320" width="85" height="30" rx="3" fill="#F3E5F5" stroke="#9C27B0" stroke-width="1"/>
        <text x="662" y="340" text-anchor="middle" font-size="12" fill="#333">Assignment</text>
        
        <rect x="570" y="360" width="110" height="30" rx="3" fill="#F3E5F5" stroke="#9C27B0" stroke-width="1"/>
        <text x="625" y="380" text-anchor="middle" font-size="12" fill="#333">String &amp; Array</text>
        
        <!-- Connection lines -->
        <line x1="400" y1="110" x2="140" y2="180" stroke="#666" stroke-width="2"/>
        <line x1="400" y1="110" x2="400" y2="180" stroke="#666" stroke-width="2"/>
        <line x1="400" y1="110" x2="660" y2="180" stroke="#666" stroke-width="2"/>
        
        <line x1="140" y1="220" x2="65" y2="280" stroke="#666" stroke-width="1"/>
        <line x1="140" y1="220" x2="75" y2="320" stroke="#666" stroke-width="1"/>
        <line x1="140" y1="220" x2="75" y2="360" stroke="#666" stroke-width="1"/>
        
        <line x1="400" y1="220" x2="330" y2="280" stroke="#666" stroke-width="1"/>
        <line x1="400" y1="220" x2="335" y2="320" stroke="#666" stroke-width="1"/>
        <line x1="400" y1="220" x2="330" y2="360" stroke="#666" stroke-width="1"/>
        
        <line x1="660" y1="220" x2="580" y2="280" stroke="#666" stroke-width="1"/>
        <line x1="660" y1="220" x2="672" y2="280" stroke="#666" stroke-width="1"/>
        <line x1="660" y1="220" x2="575" y2="320" stroke="#666" stroke-width="1"/>
        <line x1="660" y1="220" x2="662" y2="320" stroke="#666" stroke-width="1"/>
        <line x1="660" y1="220" x2="625" y2="360" stroke="#666" stroke-width="1"/>
    </svg>
</div>'''

    # Replacement for second diagram - PHP Data Types
    diagram2_svg = '''<div class="mermaid-diagram" style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
        <!-- Title -->
        <text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">PHP Data Type Categories</text>
        
        <!-- Main Class: PHPDataTypes -->
        <rect x="250" y="60" width="200" height="100" rx="5" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
        <text x="350" y="85" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">PHPDataTypes</text>
        <line x1="250" y1="95" x2="450" y2="95" stroke="#333" stroke-width="1"/>
        <text x="260" y="115" font-size="12" fill="#333">+ Scalar Types</text>
        <text x="260" y="135" font-size="12" fill="#333">+ Compound Types</text>
        <text x="260" y="155" font-size="12" fill="#333">+ Special Types</text>
        
        <!-- ScalarTypes Class -->
        <rect x="50" y="250" width="150" height="120" rx="5" fill="#E3F2FD" stroke="#2196F3" stroke-width="2"/>
        <text x="125" y="275" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">ScalarTypes</text>
        <line x1="50" y1="285" x2="200" y2="285" stroke="#2196F3" stroke-width="1"/>
        <text x="60" y="305" font-size="12" fill="#333">+ String</text>
        <text x="60" y="325" font-size="12" fill="#333">+ Integer</text>
        <text x="60" y="345" font-size="12" fill="#333">+ Float</text>
        <text x="60" y="365" font-size="12" fill="#333">+ Boolean</text>
        
        <!-- CompoundTypes Class -->
        <rect x="275" y="250" width="150" height="100" rx="5" fill="#FFF3E0" stroke="#FF9800" stroke-width="2"/>
        <text x="350" y="275" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">CompoundTypes</text>
        <line x1="275" y1="285" x2="425" y2="285" stroke="#FF9800" stroke-width="1"/>
        <text x="285" y="305" font-size="12" fill="#333">+ Array</text>
        <text x="285" y="325" font-size="12" fill="#333">+ Object</text>
        
        <!-- SpecialTypes Class -->
        <rect x="500" y="250" width="150" height="100" rx="5" fill="#F3E5F5" stroke="#9C27B0" stroke-width="2"/>
        <text x="575" y="275" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">SpecialTypes</text>
        <line x1="500" y1="285" x2="650" y2="285" stroke="#9C27B0" stroke-width="1"/>
        <text x="510" y="305" font-size="12" fill="#333">+ NULL</text>
        <text x="510" y="325" font-size="12" fill="#333">+ Resource</text>
        
        <!-- Inheritance arrows -->
        <!-- From PHPDataTypes to ScalarTypes -->
        <path d="M 300 160 L 125 250" stroke="#333" stroke-width="2" fill="none"/>
        <polygon points="125,250 130,242 135,248" fill="white" stroke="#333" stroke-width="2"/>
        
        <!-- From PHPDataTypes to CompoundTypes -->
        <path d="M 350 160 L 350 250" stroke="#333" stroke-width="2" fill="none"/>
        <polygon points="350,250 345,242 355,242" fill="white" stroke="#333" stroke-width="2"/>
        
        <!-- From PHPDataTypes to SpecialTypes -->
        <path d="M 400 160 L 575 250" stroke="#333" stroke-width="2" fill="none"/>
        <polygon points="575,250 570,242 565,248" fill="white" stroke="#333" stroke-width="2"/>
    </svg>
</div>'''

    # Replacement for third diagram - PHP Operators
    diagram3_svg = '''<div class="mermaid-diagram" style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
        <!-- Title -->
        <text x="450" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">PHP Operator Types</text>
        
        <!-- Central Node -->
        <rect x="370" y="60" width="160" height="50" rx="5" fill="#673AB7" stroke="#4527A0" stroke-width="2"/>
        <text x="450" y="90" text-anchor="middle" fill="white" font-size="16" font-weight="bold">PHP Operators</text>
        
        <!-- First row of operators -->
        <rect x="50" y="180" width="100" height="40" rx="5" fill="#03A9F4" stroke="#0277BD" stroke-width="2"/>
        <text x="100" y="205" text-anchor="middle" fill="white" font-size="13">Arithmetic</text>
        
        <rect x="170" y="180" width="100" height="40" rx="5" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        <text x="220" y="205" text-anchor="middle" fill="white" font-size="13">Assignment</text>
        
        <rect x="290" y="180" width="100" height="40" rx="5" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
        <text x="340" y="205" text-anchor="middle" fill="white" font-size="13">Comparison</text>
        
        <rect x="410" y="180" width="80" height="40" rx="5" fill="#F44336" stroke="#C62828" stroke-width="2"/>
        <text x="450" y="205" text-anchor="middle" fill="white" font-size="13">Logical</text>
        
        <rect x="510" y="180" width="80" height="40" rx="5" fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
        <text x="550" y="205" text-anchor="middle" fill="white" font-size="13">Bitwise</text>
        
        <rect x="610" y="180" width="80" height="40" rx="5" fill="#00BCD4" stroke="#00838F" stroke-width="2"/>
        <text x="650" y="205" text-anchor="middle" fill="white" font-size="13">String</text>
        
        <rect x="710" y="180" width="80" height="40" rx="5" fill="#8BC34A" stroke="#558B2F" stroke-width="2"/>
        <text x="750" y="205" text-anchor="middle" fill="white" font-size="13">Array</text>
        
        <!-- Second row of operators -->
        <rect x="150" y="280" width="80" height="40" rx="5" fill="#FFC107" stroke="#F57C00" stroke-width="2"/>
        <text x="190" y="305" text-anchor="middle" fill="white" font-size="13">Type</text>
        
        <rect x="250" y="280" width="90" height="40" rx="5" fill="#795548" stroke="#4E342E" stroke-width="2"/>
        <text x="295" y="305" text-anchor="middle" fill="white" font-size="13">Execution</text>
        
        <rect x="360" y="280" width="140" height="40" rx="5" fill="#607D8B" stroke="#37474F" stroke-width="2"/>
        <text x="430" y="305" text-anchor="middle" fill="white" font-size="12">Increment/Decrement</text>
        
        <rect x="520" y="280" width="110" height="40" rx="5" fill="#E91E63" stroke="#880E4F" stroke-width="2"/>
        <text x="575" y="305" text-anchor="middle" fill="white" font-size="13">Error Control</text>
        
        <!-- Connection lines -->
        <line x1="420" y1="110" x2="100" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="430" y1="110" x2="220" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="440" y1="110" x2="340" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="450" y1="110" x2="450" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="460" y1="110" x2="550" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="470" y1="110" x2="650" y2="180" stroke="#666" stroke-width="1.5"/>
        <line x1="480" y1="110" x2="750" y2="180" stroke="#666" stroke-width="1.5"/>
        
        <line x1="430" y1="110" x2="190" y2="280" stroke="#666" stroke-width="1.5"/>
        <line x1="440" y1="110" x2="295" y2="280" stroke="#666" stroke-width="1.5"/>
        <line x1="450" y1="110" x2="430" y2="280" stroke="#666" stroke-width="1.5"/>
        <line x1="460" y1="110" x2="575" y2="280" stroke="#666" stroke-width="1.5"/>
    </svg>
</div>'''

    # Pattern to find mermaid diagrams (accounting for variations in whitespace)
    pattern1 = r'<div class="mermaid-diagram">\s*<pre class="mermaid">\s*graph TD[^<]*?</pre>\s*</div>'
    pattern2 = r'<div class="mermaid-diagram">\s*<pre class="mermaid">\s*classDiagram[^<]*?</pre>\s*</div>'
    pattern3 = r'<div class="mermaid-diagram">\s*<pre class="mermaid">\s*graph TB[^<]*?</pre>\s*</div>'
    
    # Replace diagrams
    content = re.sub(pattern1, diagram1_svg, content, count=1)
    content = re.sub(pattern2, diagram2_svg, content, count=1)
    content = re.sub(pattern3, diagram3_svg, content, count=1)
    
    return content

def main():
    # Read the file
    input_file = r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\01module\php_variables_data_and_operators.html'
    
    print(f"Reading file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Original file size:", len(content))
    
    # Count mermaid diagrams
    mermaid_count = content.count('class="mermaid"')
    print(f"Found {mermaid_count} mermaid diagrams")
    
    # Replace mermaid diagrams
    updated_content = replace_mermaid_diagrams(content)
    
    # Check if replacements were made
    if updated_content != content:
        # Write back to the same file
        print(f"Writing updated content back to: {input_file}")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✓ File updated successfully!")
        
        # Check the changes
        new_mermaid_count = updated_content.count('class="mermaid"')
        svg_count = updated_content.count('<svg')
        print(f"Remaining mermaid elements: {new_mermaid_count}")
        print(f"SVG elements in file: {svg_count}")
    else:
        print("No changes were needed or patterns didn't match.")

if __name__ == "__main__":
    main()
