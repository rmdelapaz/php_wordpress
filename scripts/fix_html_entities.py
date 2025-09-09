#!/usr/bin/env python3
"""
Fix HTML entities in homework_interactive.html
"""

import re

def fix_html_entities(content):
    """Replace HTML entities with actual characters"""
    
    # Replace common HTML entities
    replacements = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' ',
        '&times;': '×',
        '=&gt;': '=>',
        '&amp;&amp;': '&&',
        '&lt;=': '<=',
        '&gt;=': '>=',
    }
    
    for entity, replacement in replacements.items():
        content = content.replace(entity, replacement)
    
    return content

def main():
    # Read the file
    file_path = '\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\01module\\homework_interactive.html'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix HTML entities
        fixed_content = fix_html_entities(content)
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Successfully fixed HTML entities in {file_path}")
        
        # Count how many replacements were made
        entity_count = 0
        for entity in ['&lt;', '&gt;', '&amp;', '=&gt;', '&amp;&amp;']:
            count = content.count(entity)
            if count > 0:
                print(f"  Replaced {count} instances of '{entity}'")
                entity_count += count
        
        print(f"Total entities replaced: {entity_count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
