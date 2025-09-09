#!/usr/bin/env python3
"""
Script to fix CSS class names and formatting in php_string_operators.html
"""

from pathlib import Path
import re

def fix_formatting():
    """Fix CSS class names and formatting consistency."""
    
    file_path = Path("/home/practicalace/projects/php_wordpress/02module/php_string_operators.html")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix class names - convert underscores to hyphens
    replacements = [
        # Section classes
        ('class="operators_overview"', 'class="operators-overview"'),
        ('class="operators_table"', 'class="operators-table"'),
        ('class="concatenation_operator"', 'class="concatenation-operator"'),
        ('class="concatenation_assignment"', 'class="concatenation-assignment"'),
        ('class="type_conversion"', 'class="type-conversion"'),
        ('class="real_world"', 'class="real-world"'),
        ('class="best_practices"', 'class="best-practices"'),
        ('class="string_interpolation"', 'class="string-interpolation"'),
        ('class="heredoc_nowdoc"', 'class="heredoc-nowdoc"'),
        ('class="advanced_string_manipulation"', 'class="advanced-string-manipulation"'),
        ('class="practice_exercises"', 'class="practice-exercises"'),
        ('class="next_session"', 'class="next-session"'),
        ('class="additional_resources"', 'class="additional-resources"'),
        ('class="code_example"', 'class="code-example"'),
        
        # Fix any remaining underscore classes
        ('class="svg_container"', 'class="svg-container"'),
        ('class="mermaid_diagram"', 'class="mermaid-diagram"'),
        
        # Fix entity issues in code blocks
        ('&amp;lt;', '&lt;'),
        ('&amp;gt;', '&gt;'),
        ('&amp;amp;', '&amp;'),
        
        # Fix arrow functions in code that might be encoded wrong
        ('-&gt;', '->'),
        ('=&gt;', '=>'),
    ]
    
    # Apply all replacements
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  Replaced: {old[:30]}...")
    
    # Fix section heading consistency - ensure all section headings use hyphens not underscores
    content = re.sub(r'<section class="([^"]+)_([^"]+)"', r'<section class="\1-\2"', content)
    content = re.sub(r'<div class="([^"]+)_([^"]+)"', r'<div class="\1-\2"', content)
    
    # Additional fix for any remaining underscores in class names
    # This regex will catch any class="something_something" pattern
    content = re.sub(r'class="([^"]*?)_([^"]*?)"', r'class="\1-\2"', content)
    
    # Keep doing this until no more underscores in class names
    while re.search(r'class="[^"]*_[^"]*"', content):
        content = re.sub(r'class="([^"]*?)_([^"]*?)"', r'class="\1-\2"', content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✓ Fixed all CSS class names (underscores to hyphens)")
    print("✓ Fixed HTML entity encoding issues")
    print("✓ Fixed arrow operators in PHP code")
    print("✓ Ensured formatting consistency")
    print("\nThe php_string_operators.html file is now properly formatted!")

if __name__ == "__main__":
    print("Fixing CSS and formatting in php_string_operators.html...")
    print("=" * 50)
    fix_formatting()
