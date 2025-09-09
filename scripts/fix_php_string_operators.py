#!/usr/bin/env python3
"""
Script to fix issues in php_string_operators.html file
- Removes duplicate content
- Fixes HTML entities
- Ensures consistent formatting
- Maintains proper structure
"""

import re
import os
from pathlib import Path

def fix_php_string_operators():
    """Main function to fix all issues in the file."""
    
    # Use relative path since we're running from the project directory
    file_path = "02module/php_string_operators.html"
    
    # Get absolute path
    abs_path = os.path.abspath(file_path)
    
    print(f"Processing file: {abs_path}")
    
    try:
        # Read the file content
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original file size: {len(content)} characters")
        
        # Step 1: Remove duplicate sections
        # The file has duplicate content starting from certain sections
        # Find the first occurrence of the closing tags pattern and truncate there
        
        # Look for the proper ending pattern
        proper_ending = """</div>
</article>
</div>
</div>
</main>
<!-- Footer -->"""
        
        # Find the first complete occurrence of the proper ending
        end_index = content.find(proper_ending)
        if end_index != -1:
            # Find the actual end of the HTML document
            footer_end = content.find('</html>', end_index)
            if footer_end != -1:
                content = content[:footer_end + 7]  # +7 for '</html>'
                print(f"Removed duplicate content. New size: {len(content)} characters")
        
        # Step 2: Fix HTML entities in code blocks
        def fix_code_entities(match):
            """Fix HTML entities within code blocks."""
            code = match.group(1)
            # Replace HTML entities with actual characters
            code = code.replace('&lt;', '<')
            code = code.replace('&gt;', '>')
            code = code.replace('&amp;', '&')
            code = code.replace('&quot;', '"')
            return f'<code class="language-php">{code}</code>'
        
        # Fix entities in PHP code blocks
        content = re.sub(r'<code class="language-php">(.*?)</code>', 
                         fix_code_entities, content, flags=re.DOTALL)
        
        # Step 3: Fix broken HTML structures
        # Fix any broken table cell tags
        content = re.sub(r'<td>\n\s*</div>', '</td>\n    </tr>\n  </tbody>\n</table>\n</div>', content)
        
        # Step 4: Ensure consistent indentation for HTML structure
        lines = content.split('\n')
        fixed_lines = []
        indent_level = 0
        in_pre_block = False
        
        for line in lines:
            stripped = line.strip()
            
            # Handle pre blocks specially
            if '<pre' in line:
                in_pre_block = True
                fixed_lines.append(line)
                continue
            elif '</pre>' in line:
                in_pre_block = False
                fixed_lines.append(line)
                continue
            
            # Don't modify content inside pre blocks
            if in_pre_block:
                fixed_lines.append(line)
                continue
            
            # Skip empty lines
            if not stripped:
                fixed_lines.append('')
                continue
            
            # Decrease indent for closing tags
            if stripped.startswith('</') and not stripped.startswith('</br'):
                indent_level = max(0, indent_level - 1)
            
            # Add properly indented line
            fixed_lines.append('    ' * indent_level + stripped)
            
            # Increase indent for opening tags (but not self-closing)
            if (stripped.startswith('<') and 
                not stripped.startswith('</') and 
                not stripped.startswith('<!') and
                not stripped.endswith('/>') and
                not any(tag in stripped for tag in ['<br>', '<hr>', '<img', '<input', '<meta', '<link'])):
                
                # Check if it's a single-line tag
                if not (stripped.endswith('>') and '</' in stripped):
                    indent_level += 1
        
        content = '\n'.join(fixed_lines)
        
        # Step 5: Fix specific CSS class issues
        # Ensure consistent class names
        content = re.sub(r'class="code-example"', 'class="code-example"', content)
        content = re.sub(r'class="real-world"', 'class="real-world"', content)
        content = re.sub(r'class="best-practices"', 'class="best-practices"', content)
        
        # Step 6: Ensure mermaid diagrams are properly converted
        # Already converted to SVG, so just ensure they're properly formatted
        content = re.sub(r'<div class="mermaid-converted"', '<div class="mermaid-converted"', content)
        
        # Step 7: Remove any duplicate exercise sections
        # Count exercise sections
        exercise_pattern = r'<h3>Exercise \d+:'
        exercises = re.findall(exercise_pattern, content)
        if len(exercises) > 6:  # Should only have 3 exercises, but they might appear twice
            # Find the second occurrence of the practice-exercises section
            practice_sections = list(re.finditer(r'<section class="practice-exercises">', content))
            if len(practice_sections) > 1:
                # Remove everything from the second practice section onwards
                content = content[:practice_sections[1].start()]
                
                # Re-add the proper ending
                content += """
        </div>
    </article>
</div>
</div>
</main>
<!-- Footer -->
<footer class="site-footer" role="contentinfo">
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-section footer-about">
                <h3>PHP WordPress Development</h3>
                <p>Complete Web Development Course</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul class="footer-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/module2.html">Module 2</a></li>
                    <li><a href="/resources.html">Resources</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>Support</h4>
                <ul class="footer-links">
                    <li><a href="/help.html">Help Center</a></li>
                    <li><a href="/faq.html">FAQ</a></li>
                    <li><a href="/contact.html">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="footer-bottom-content">
                <p class="copyright">© 2025 PHP WordPress Development Course</p>
                <nav class="footer-bottom-links">
                    <a href="/privacy.html">Privacy</a>
                    <span class="separator">|</span>
                    <a href="/terms.html">Terms</a>
                </nav>
            </div>
        </div>
    </div>
</footer>
</div>
<!-- Back to Top -->
<button aria-label="Back to top" class="back-to-top" id="back-to-top">
    <svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="24">
        <path d="M12 19V5M12 5l-7 7M12 5l7 7"></path>
    </svg>
</button>
<!-- JavaScript -->
<script src="/assets/js/navigation.js"></script>
<script src="/assets/js/site-config.js"></script>
<script src="/assets/js/sidebar-toggle.js"></script>
</body>
</html>"""
        
        # Step 8: Create backup of original file
        backup_path = abs_path + '.backup'
        if not os.path.exists(backup_path):
            with open(abs_path, 'r', encoding='utf-8') as original:
                backup_content = original.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            print(f"Created backup at: {backup_path}")
        
        # Step 9: Write the fixed content
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"File successfully fixed!")
        print(f"Final file size: {len(content)} characters")
        
        # Step 10: Verify the fix
        with open(abs_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        
        # Check for common issues
        issues = []
        if verify_content.count('</html>') > 1:
            issues.append("Multiple </html> tags found")
        if verify_content.count('<html') > 1:
            issues.append("Multiple <html> tags found")
        if '&lt;?php' in verify_content:
            issues.append("HTML entities still present in code")
        if verify_content.count('Exercise 1:') > 1:
            issues.append("Duplicate exercises found")
        
        if issues:
            print("\nWarning: Some issues may still exist:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\nAll checks passed! File appears to be properly fixed.")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_css_fix():
    """Create additional CSS fixes if needed."""
    css_fixes = """
/* Additional CSS fixes for php_string_operators.html */

.code-example {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.code-example h3 {
    margin-top: 0;
    color: #495057;
    font-size: 1.25rem;
}

.code-example pre {
    margin-bottom: 0;
    background-color: #ffffff;
    border: 1px solid #e9ecef;
}

.real-world {
    background-color: #e7f3ff;
    border-left: 4px solid #007bff;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.real-world h3 {
    color: #004085;
    margin-top: 0;
}

.best-practices {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.best-practices h3 {
    color: #155724;
    margin-top: 0;
}

.exercise {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.exercise h3 {
    color: #856404;
    margin-top: 0;
}

.performance {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.performance h3 {
    color: #721c24;
    margin-top: 0;
}

.comparison table {
    width: 100%;
    margin: 1rem 0;
    border-collapse: collapse;
}

.comparison th,
.comparison td {
    padding: 0.75rem;
    text-align: left;
    border: 1px solid #dee2e6;
}

.comparison th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.comparison tbody tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* Mermaid diagram styling */
.mermaid-converted {
    margin: 20px 0;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.mermaid-converted svg {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
}

/* Code syntax highlighting improvements */
code.language-php {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    line-height: 1.5;
}

pre code {
    display: block;
    padding: 1rem;
    overflow-x: auto;
}

/* Section spacing */
section {
    margin: 2rem 0;
}

section h2 {
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #343a40;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 0.5rem;
}

section h3 {
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    color: #495057;
}

/* List styling */
section ul,
section ol {
    margin: 1rem 0;
    padding-left: 2rem;
}

section li {
    margin: 0.5rem 0;
    line-height: 1.6;
}

/* Table styling */
.operators-table table {
    width: 100%;
    margin: 1.5rem 0;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.operators-table th,
.operators-table td {
    padding: 1rem;
    text-align: left;
    border: 1px solid #dee2e6;
}

.operators-table th {
    background-color: #007bff;
    color: white;
    font-weight: 600;
}

.operators-table tbody tr:hover {
    background-color: #f8f9fa;
}

/* SVG container styling */
.svg-container {
    margin: 1.5rem 0;
    text-align: center;
}

.svg-container svg {
    max-width: 100%;
    height: auto;
}
"""
    
    css_path = "assets/css/php_string_operators_fixes.css"
    
    try:
        os.makedirs(os.path.dirname(css_path), exist_ok=True)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_fixes)
        print(f"\nCreated additional CSS fixes at: {css_path}")
        print("Add this to your HTML head section:")
        print('<link href="/assets/css/php_string_operators_fixes.css" rel="stylesheet"/>')
        return True
    except Exception as e:
        print(f"Could not create CSS file: {e}")
        return False

if __name__ == "__main__":
    print("PHP String Operators HTML Fixer")
    print("=" * 50)
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Fix the main HTML file
    if fix_php_string_operators():
        print("\n✓ Successfully fixed php_string_operators.html")
        
        # Optionally create CSS fixes
        print("\nWould you like to create additional CSS fixes? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response == 'y':
                create_css_fix()
        except:
            print("Skipping CSS creation")
    else:
        print("\n✗ Failed to fix the file. Please check the error messages above.")
    
    print("\nProcess complete!")
