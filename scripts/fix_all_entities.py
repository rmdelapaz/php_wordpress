#!/usr/bin/env python3
"""
Fix all HTML entities in homework_interactive.html
"""

def fix_html_entities(file_path):
    """Fix HTML entities in the file"""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original entities for reporting
    original_count = content.count('&lt;') + content.count('&gt;') + content.count('&amp;')
    
    # Replace HTML entities with actual characters
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&amp;', '&')
    content = content.replace('&quot;', '"')
    content = content.replace('&#39;', "'")
    content = content.replace('&nbsp;', ' ')
    content = content.replace('&times;', '×')
    content = content.replace('=&gt;', '=>')
    content = content.replace('&amp;&amp;', '&&')
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Count final entities for verification
    final_count = content.count('&lt;') + content.count('&gt;') + content.count('&amp;')
    
    print(f"Fixed HTML entities in {file_path}")
    print(f"  Original entity count: {original_count}")
    print(f"  Final entity count: {final_count}")
    print(f"  Entities replaced: {original_count - final_count}")
    
    return original_count - final_count

# Run the fix
if __name__ == '__main__':
    file_path = '\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\01module\\homework_interactive.html'
    entities_fixed = fix_html_entities(file_path)
    
    if entities_fixed > 0:
        print(f"\nSuccessfully fixed {entities_fixed} HTML entities!")
    else:
        print("\nNo HTML entities found to fix.")
