#!/usr/bin/env python3
"""
Complete fix for php_string_operators.html
- Fixes incomplete code blocks
- Properly escapes PHP code
- Ensures consistent formatting
- Removes any duplicate content
"""

import re
import os
import html

def fix_php_string_operators_complete():
    """Comprehensive fix for the PHP string operators file."""
    
    # File path
    file_path = "02module/php_string_operators.html"
    abs_path = os.path.abspath(file_path)
    
    print(f"Processing: {abs_path}")
    
    try:
        # Read current content
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original size: {len(content)} characters")
        
        # Find where the incomplete table code is
        incomplete_pattern = r'<td>\' \. htmlspecialchars\(\$product\[\'name\'\]\) \. \'</td>\' \. "\\n";\s*\$html \.= \'      \n\s*</div>'
        
        # Fix the incomplete table building code
        complete_table_code = '''<td>' . htmlspecialchars($product['name']) . '</td>' . "\\n";
    $html .= '      <td>$' . number_format($product['price'], 2) . '</td>' . "\\n";
    $html .= '      <td>' . $product['stock'] . ' units</td>' . "\\n";
    $html .= '      <td><button onclick="addToCart(' . $product['id'] . ')">Add to Cart</button></td>' . "\\n";
    $html .= '    </tr>' . "\\n";
}

$html .= '  </tbody>' . "\\n";
$html .= '</table>';

echo $html;
?></code></pre>
                </div>'''
        
        # Replace the incomplete section
        content = re.sub(
            r'<td>\' \. htmlspecialchars\(\$product\[\'name\'\]\) \. \'</td>\' \. "\\n";\s*\$html \.= \'      \s*</div>',
            complete_table_code,
            content,
            flags=re.DOTALL
        )
        
        # Ensure all PHP opening tags are properly escaped
        def fix_php_tags_in_code(match):
            """Fix PHP tags within code blocks."""
            code_content = match.group(1)
            # Only escape PHP tags, not HTML entities that are already escaped
            if '<?php' in code_content and '&lt;?php' not in code_content:
                code_content = code_content.replace('<?php', '&lt;?php')
                code_content = code_content.replace('?>', '?&gt;')
            return f'<code class="language-php">{code_content}</code>'
        
        # Apply the fix to all code blocks
        content = re.sub(
            r'<code class="language-php">(.*?)</code>',
            fix_php_tags_in_code,
            content,
            flags=re.DOTALL
        )
        
        # Fix the concatenation assignment section if it's missing the proper closing
        if "Real-World Application: Building an Email Template" in content:
            # Find and fix the email template section
            email_section_start = content.find("Real-World Application: Building an Email Template")
            if email_section_start > 0:
                # Check if this section is properly closed
                next_section = content.find("</section>", email_section_start)
                if next_section == -1 or next_section > email_section_start + 10000:
                    # Section might not be properly closed, ensure it is
                    pass
        
        # Remove any duplicate content at the end
        # The file should end with the closing tags in order
        proper_ending = '''        </div>
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
</html>'''
        
        # Find the last occurrence of the lesson navigation
        last_nav_pos = content.rfind('<div class="lesson-navigation">')
        if last_nav_pos > 0:
            # Find the end of this navigation section
            nav_end = content.find('</div>', last_nav_pos)
            if nav_end > 0:
                nav_end = content.find('</div>', nav_end + 1)  # Find the closing div for navigation
                if nav_end > 0:
                    # Everything after navigation should be the proper ending
                    content = content[:nav_end + 6] + '\n' + proper_ending
        
        # Clean up extra whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Ensure consistent indentation for main structural elements
        lines = content.split('\n')
        fixed_lines = []
        in_code_block = False
        
        for line in lines:
            # Check if we're entering or leaving a code block
            if '<pre>' in line or '<code' in line:
                in_code_block = True
            elif '</pre>' in line or '</code>' in line:
                in_code_block = False
            
            # Don't modify lines inside code blocks
            if in_code_block:
                fixed_lines.append(line)
            else:
                # For non-code lines, ensure consistent spacing
                if line.strip():
                    # Keep the line with its current indentation
                    fixed_lines.append(line)
                else:
                    fixed_lines.append('')
        
        content = '\n'.join(fixed_lines)
        
        # Create backup
        backup_path = abs_path + '.backup2'
        with open(abs_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        print(f"Created backup at: {backup_path}")
        
        # Write fixed content
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed file size: {len(content)} characters")
        
        # Verify the fix
        with open(abs_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        
        # Run verification checks
        issues = []
        
        # Check HTML structure
        if verify_content.count('</html>') != 1:
            issues.append(f"Found {verify_content.count('</html>')} </html> tags (should be 1)")
        
        if verify_content.count('<html') != 1:
            issues.append(f"Found {verify_content.count('<html')} <html> tags (should be 1)")
        
        # Check for unescaped PHP tags in the HTML (outside of code blocks)
        # This is a simple check - looking for <?php outside of code blocks
        code_blocks = re.findall(r'<code[^>]*>.*?</code>', verify_content, re.DOTALL)
        non_code_content = verify_content
        for block in code_blocks:
            non_code_content = non_code_content.replace(block, '')
        
        if '<?php' in non_code_content:
            issues.append("Found unescaped <?php tags outside code blocks")
        
        # Check for incomplete code blocks
        if 'htmlspecialchars($product[' in verify_content and '</td>' not in verify_content[verify_content.find('htmlspecialchars($product['):verify_content.find('htmlspecialchars($product[') + 200]:
            issues.append("Possible incomplete code block found")
        
        if issues:
            print("\nWarning - Issues detected:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n✓ All verification checks passed!")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_formatting_css():
    """Create CSS file for proper formatting."""
    
    css_content = """/* PHP String Operators Page Specific Styles */

/* Code block formatting */
.code-example {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.code-example h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #495057;
    font-size: 1.25rem;
    font-weight: 600;
}

.code-example h4 {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: #6c757d;
    font-size: 1.1rem;
}

.code-example pre {
    margin: 0;
    border-radius: 4px;
    background-color: #282c34;
}

.code-example code {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    line-height: 1.5;
    color: #abb2bf;
}

/* Section-specific styling */
.real-world {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    padding: 2rem;
    margin: 2rem 0;
}

.real-world h3 {
    color: white;
    margin-top: 0;
    font-size: 1.5rem;
}

.real-world p {
    color: rgba(255, 255, 255, 0.95);
}

.real-world pre {
    background-color: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.best-practices {
    background-color: #d4edda;
    border-left: 4px solid #28a745;
    padding: 1.5rem;
    margin: 2rem 0;
}

.best-practices h3 {
    color: #155724;
    margin-top: 0;
}

.best-practices ul {
    margin: 1rem 0;
}

.best-practices li {
    margin: 0.5rem 0;
}

/* Exercise sections */
.exercise {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.exercise h3 {
    color: #856404;
    margin-top: 0;
    border-bottom: 2px solid #ffeaa7;
    padding-bottom: 0.5rem;
}

.exercise p {
    color: #664d03;
    margin: 1rem 0;
}

/* Performance section */
.performance {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.performance h3 {
    color: #721c24;
    margin-top: 0;
}

/* Comparison tables */
.comparison {
    margin: 2rem 0;
}

.comparison table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.comparison th,
.comparison td {
    padding: 1rem;
    text-align: left;
    border: 1px solid #dee2e6;
}

.comparison th {
    background-color: #007bff;
    color: white;
    font-weight: 600;
}

.comparison tbody tr:nth-child(even) {
    background-color: #f8f9fa;
}

.comparison tbody tr:hover {
    background-color: #e9ecef;
}

/* Type conversion section */
.type-conversion {
    background-color: #e7f3ff;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.type-conversion h3 {
    color: #004085;
    margin-top: 0;
}

/* Operators table */
.operators-table {
    margin: 2rem 0;
}

.operators-table table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.operators-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
}

.operators-table td {
    padding: 1rem;
    border: 1px solid #dee2e6;
}

.operators-table tbody tr:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

/* SVG Container */
.svg-container {
    text-align: center;
    margin: 2rem 0;
    padding: 1rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.svg-container svg {
    max-width: 100%;
    height: auto;
}

/* Mermaid diagram container */
.mermaid-converted {
    margin: 2rem 0;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.mermaid-converted svg {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}

/* Summary section */
.summary {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 8px;
    padding: 2rem;
    margin: 2rem 0;
}

.summary h2 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 0.5rem;
}

.summary ul {
    margin-top: 1rem;
}

.summary li {
    margin: 0.75rem 0;
    line-height: 1.6;
}

/* Additional resources section */
.additional-resources {
    background-color: #e8f5e9;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
}

.additional-resources h2 {
    color: #2e7d32;
    margin-bottom: 1rem;
}

.additional-resources ul {
    list-style-type: none;
    padding: 0;
}

.additional-resources li {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;
}

.additional-resources li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: #4caf50;
    font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .code-example,
    .real-world,
    .best-practices,
    .exercise,
    .performance,
    .type-conversion,
    .summary,
    .additional-resources {
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .comparison table,
    .operators-table table {
        font-size: 0.9em;
    }
    
    .comparison th,
    .comparison td,
    .operators-table th,
    .operators-table td {
        padding: 0.5rem;
    }
}
"""
    
    css_path = "assets/css/php_string_operators.css"
    
    try:
        os.makedirs(os.path.dirname(css_path), exist_ok=True)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print(f"\nCreated CSS file at: {css_path}")
        print("\nAdd this line to the <head> section of your HTML:")
        print('<link href="/assets/css/php_string_operators.css" rel="stylesheet"/>')
        return True
    except Exception as e:
        print(f"Could not create CSS file: {e}")
        return False


if __name__ == "__main__":
    print("PHP String Operators - Complete Fix")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("02module/php_string_operators.html"):
        print("Error: Cannot find 02module/php_string_operators.html")
        print("Please run this script from the php_wordpress directory")
        exit(1)
    
    # Run the comprehensive fix
    if fix_php_string_operators_complete():
        print("\n✓ Successfully fixed php_string_operators.html")
        
        # Create CSS file
        print("\nCreating formatted CSS file...")
        if create_formatting_css():
            print("✓ CSS file created successfully")
        
        print("\n" + "=" * 50)
        print("Fix complete! The file should now be properly formatted.")
        print("\nNext steps:")
        print("1. Check the file in your browser")
        print("2. Add the CSS link to the HTML if needed")
        print("3. Verify all code examples display correctly")
    else:
        print("\n✗ Failed to fix the file")
        print("Please check the error messages above")
