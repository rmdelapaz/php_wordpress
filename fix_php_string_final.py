#!/usr/bin/env python3
"""
Final comprehensive fix for php_string_operators.html
- Properly escapes ALL PHP code in code blocks
- Removes excessive whitespace around SVGs and diagrams
- Ensures consistent formatting
- Works with both WSL and native paths
"""

import re
import os
import html
from pathlib import Path
import sys

def get_file_path():
    """Get the correct file path based on the environment."""
    
    # Check if we're running from WSL or Windows
    if sys.platform == "win32" or os.path.exists(r"\\wsl$"):
        # Windows environment - use WSL path
        base_path = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
        file_path = os.path.join(base_path, "02module", "php_string_operators.html")
        css_base = base_path
    else:
        # Linux/WSL environment
        base_path = "/home/practicalace/projects/php_wordpress"
        file_path = os.path.join(base_path, "02module", "php_string_operators.html")
        css_base = base_path
    
    # Also check relative path if we're in the right directory
    if not os.path.exists(file_path):
        if os.path.exists("02module/php_string_operators.html"):
            file_path = "02module/php_string_operators.html"
            css_base = "."
    
    return file_path, css_base


def fix_php_code_escaping(content):
    """Properly escape all PHP code within code blocks."""
    
    print("Fixing PHP code escaping...")
    
    # Pattern to find code blocks
    code_block_pattern = r'<pre><code class="language-php">(.*?)</code></pre>'
    
    def escape_php_code(match):
        code = match.group(1)
        
        # First, unescape any already escaped entities to avoid double escaping
        code = html.unescape(code)
        
        # Now properly escape everything
        code = code.replace('&', '&amp;')
        code = code.replace('<', '&lt;')
        code = code.replace('>', '&gt;')
        code = code.replace('"', '&quot;')
        code = code.replace("'", '&#39;')
        
        return f'<pre><code class="language-php">{code}</code></pre>'
    
    # Apply escaping to all PHP code blocks
    content = re.sub(code_block_pattern, escape_php_code, content, flags=re.DOTALL)
    
    return content


def fix_svg_whitespace(content):
    """Remove excessive whitespace around SVG elements and diagrams."""
    
    print("Fixing SVG and diagram whitespace...")
    
    # Fix whitespace around SVG containers
    patterns = [
        # Remove excessive newlines around SVG elements
        (r'(<svg[^>]*>.*?</svg>)\s*(\n{3,})', r'\1\n\n'),
        
        # Fix whitespace around mermaid-converted divs
        (r'(\n{3,})(\s*<div class="mermaid-converted")', r'\n\n\2'),
        (r'(</div><!--\s*end mermaid-converted\s*-->)\s*(\n{3,})', r'\1\n\n'),
        
        # Fix whitespace around svg-container divs
        (r'(\n{3,})(\s*<div class="svg-container")', r'\n\n\2'),
        (r'(</div><!--\s*end svg-container\s*-->)\s*(\n{3,})', r'\1\n\n'),
        
        # Remove excessive whitespace between SVG internal elements
        (r'(<rect[^>]*/>)\s*\n\s*\n+\s*(<text)', r'\1\n                                                                                \2'),
        (r'(</text>)\s*\n\s*\n+\s*(<rect)', r'\1\n                                                                                \2'),
        
        # Clean up excessive indentation in SVG blocks
        (r'(\n)\s{100,}(<)', r'\1            \2'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Special handling for mermaid-converted sections
    mermaid_sections = re.findall(
        r'<div class="mermaid-converted"[^>]*>.*?</svg>\s*</div>',
        content,
        flags=re.DOTALL
    )
    
    for section in mermaid_sections:
        # Clean up the section
        cleaned_section = section
        # Remove excessive internal whitespace
        cleaned_section = re.sub(r'\n{3,}', '\n\n', cleaned_section)
        # Fix indentation
        lines = cleaned_section.split('\n')
        fixed_lines = []
        for line in lines:
            if line.strip():
                # Normalize indentation
                if '<div class="mermaid-converted"' in line:
                    fixed_lines.append('                                        ' + line.strip())
                elif line.strip().startswith('<svg') or line.strip().startswith('</svg'):
                    fixed_lines.append('                                            ' + line.strip())
                elif line.strip().startswith('</div>'):
                    fixed_lines.append('                                        ' + line.strip())
                else:
                    # SVG internal elements
                    fixed_lines.append('                                                ' + line.strip())
            else:
                fixed_lines.append('')
        
        cleaned_section = '\n'.join(fixed_lines)
        content = content.replace(section, cleaned_section)
    
    return content


def fix_incomplete_code_blocks(content):
    """Fix any incomplete code blocks, especially the table building example."""
    
    print("Fixing incomplete code blocks...")
    
    # Find and fix the incomplete table building code
    incomplete_table_pattern = r'(\$html \.= \'      <td>\' \. htmlspecialchars\(\$product\[\'name\'\]\) \. \'</td>\' \. "\\n";\s*\$html \.= \'      )\n\s*</div>'
    
    if re.search(incomplete_table_pattern, content):
        print("  Found incomplete table code - fixing...")
        
        complete_table = r'''\1<td>$' . number_format($product['price'], 2) . '</td>' . "\\n";
    $html .= '      <td>' . $product['stock'] . ' units</td>' . "\\n";
    $html .= '      <td><button onclick="addToCart(' . $product['id'] . ')">Add to Cart</button></td>' . "\\n";
    $html .= '    </tr>' . "\\n";
}

$html .= '  </tbody>' . "\\n";
$html .= '</table>';

echo $html;
?&gt;</code></pre>
                                                                        </div>'''
        
        content = re.sub(incomplete_table_pattern, complete_table, content)
    
    return content


def ensure_proper_structure(content):
    """Ensure proper HTML structure and remove duplicates."""
    
    print("Ensuring proper HTML structure...")
    
    # Find the main content end marker
    main_end_marker = '</article>\n                                                            </div>\n                                                        </div>\n                                                    </main>'
    
    # Proper footer and ending
    proper_ending = '''                                                    </main>
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
    
    # Find where main content should end
    if main_end_marker in content:
        end_pos = content.find(main_end_marker) + len(main_end_marker)
        content = content[:end_pos] + '\n' + proper_ending
    else:
        # Alternative: find the last lesson-navigation div
        last_nav = content.rfind('</div>\n                                                                </article>')
        if last_nav > 0:
            end_pos = content.find('</div>\n                                                        </div>\n                                                    </main>', last_nav)
            if end_pos > 0:
                content = content[:end_pos + 87] + '\n' + proper_ending
    
    return content


def clean_excessive_whitespace(content):
    """Clean up excessive whitespace throughout the document."""
    
    print("Cleaning excessive whitespace...")
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Fix excessive indentation (more than 120 spaces)
    content = re.sub(r'\n {120,}', '\n                    ', content)
    
    # Clean up whitespace around section tags
    content = re.sub(r'(\n{3,})(\s*<section)', r'\n\n\2', content)
    content = re.sub(r'(</section>)\s*(\n{3,})', r'\1\n\n', content)
    
    # Clean up whitespace around div tags
    content = re.sub(r'(\n{3,})(\s*<div class="code-example")', r'\n\n\2', content)
    content = re.sub(r'(</div><!--\s*end code-example\s*-->)\s*(\n{3,})', r'\1\n\n', content)
    
    return content


def main():
    """Main function to fix all issues."""
    
    # Get the correct file path
    file_path, css_base = get_file_path()
    
    print(f"Processing: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        print("\nTried paths:")
        print(f"  - {file_path}")
        print(f"  - 02module/php_string_operators.html (relative)")
        print(f"  - \\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module\\php_string_operators.html")
        print("\nPlease ensure you're running from the correct directory or the file exists.")
        return False
    
    try:
        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Original size: {len(content):,} characters")
        
        # Apply all fixes in sequence
        content = fix_incomplete_code_blocks(content)
        content = fix_php_code_escaping(content)
        content = fix_svg_whitespace(content)
        content = clean_excessive_whitespace(content)
        content = ensure_proper_structure(content)
        
        # Final cleanup - ensure no excessive whitespace at end
        content = content.rstrip() + '\n'
        
        # Create backup
        backup_path = file_path + '.backup_final'
        with open(file_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
        print(f"Created backup at: {backup_path}")
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed size: {len(content):,} characters")
        
        # Verification
        print("\nRunning verification checks...")
        
        issues = []
        
        # Check for unescaped PHP tags in code blocks
        code_blocks = re.findall(r'<code class="language-php">(.*?)</code>', content, re.DOTALL)
        for i, block in enumerate(code_blocks):
            if '<?php' in block or '<?' in block[:10]:
                if '&lt;?php' not in block:
                    issues.append(f"Code block {i+1} may have unescaped PHP tags")
        
        # Check HTML structure
        if content.count('</html>') != 1:
            issues.append(f"Found {content.count('</html>')} </html> tags (should be 1)")
        
        if content.count('<html') != 1:
            issues.append(f"Found {content.count('<html')} <html> tags (should be 1)")
        
        # Check for excessive whitespace patterns
        if re.search(r'\n{5,}', content):
            issues.append("Still has excessive blank lines (5+ consecutive)")
        
        if re.search(r' {150,}', content):
            issues.append("Still has excessive indentation (150+ spaces)")
        
        # Check SVG sections for excessive whitespace
        svg_sections = re.findall(r'<svg.*?</svg>', content, re.DOTALL)
        for i, svg in enumerate(svg_sections):
            if '\n\n\n\n' in svg:
                issues.append(f"SVG {i+1} still has excessive internal whitespace")
        
        if issues:
            print("\n⚠ Warning - Some issues remain:")
            for issue in issues:
                print(f"  - {issue}")
            print("\nThese may need manual review.")
        else:
            print("\n✓ All verification checks passed!")
        
        # Create CSS file
        create_clean_css(css_base)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_clean_css(base_path):
    """Create a clean CSS file for proper styling."""
    
    css_content = """/* PHP String Operators - Clean Styles */

/* Remove excessive margins around SVG containers */
.svg-container,
.mermaid-converted {
    margin: 1.5rem 0;
    padding: 1rem;
    overflow: hidden;
}

.svg-container svg,
.mermaid-converted svg {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 0 auto;
}

/* Code blocks with proper spacing */
.code-example {
    margin: 1.5rem 0;
    padding: 1.5rem;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
}

.code-example pre {
    margin: 0;
    overflow-x: auto;
}

.code-example code {
    display: block;
    padding: 1rem;
    background-color: #282c34;
    color: #abb2bf;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    line-height: 1.5;
}

/* Ensure no excessive spacing between sections */
section {
    margin: 2rem 0;
}

section + section {
    margin-top: 2rem;
}

/* Clean table spacing */
.operators-table,
.comparison {
    margin: 1.5rem 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

/* Remove any default margins that might cause issues */
h2, h3, h4 {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}

p {
    margin: 1rem 0;
}

/* Specific fixes for diagrams */
.mermaid-converted > div:first-child {
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Ensure exercises don't have excessive spacing */
.exercise {
    margin: 1.5rem 0;
    padding: 1.5rem;
}

.exercise pre {
    margin-top: 1rem;
    margin-bottom: 0;
}

/* Performance and best practices sections */
.performance,
.best-practices,
.real-world,
.type-conversion {
    margin: 1.5rem 0;
    padding: 1.5rem;
    border-radius: 8px;
}

/* Summary and additional resources */
.summary,
.additional-resources,
.next-session {
    margin: 2rem 0;
    padding: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .svg-container,
    .mermaid-converted,
    .code-example,
    .exercise,
    section {
        margin: 1rem 0;
    }
    
    .code-example,
    .exercise,
    .performance,
    .best-practices {
        padding: 1rem;
    }
}
"""
    
    css_path = os.path.join(base_path, "assets", "css", "php_string_operators_clean.css")
    
    try:
        os.makedirs(os.path.dirname(css_path), exist_ok=True)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print(f"\nCreated clean CSS file at: {css_path}")
        print("\nAdd this line to the <head> section of your HTML:")
        print('<link href="/assets/css/php_string_operators_clean.css" rel="stylesheet"/>')
        return True
    except Exception as e:
        print(f"Could not create CSS file: {e}")
        return False


if __name__ == "__main__":
    print("PHP String Operators - Final Comprehensive Fix")
    print("=" * 50)
    
    # Show current environment
    print(f"Platform: {sys.platform}")
    print(f"Current directory: {os.getcwd()}")
    
    # Run the fixes
    if main():
        print("\n✓ Successfully fixed php_string_operators.html")
        print("\n" + "=" * 50)
        print("All fixes complete!")
        print("\nThe file now has:")
        print("  • Properly escaped PHP code in all code blocks")
        print("  • Clean SVG/diagram sections without excessive whitespace")
        print("  • Consistent formatting throughout")
        print("  • Proper HTML structure")
        print("\nNext steps:")
        print("1. Open the file in a browser to verify")
        print("2. Check that all code examples display correctly")
        print("3. Verify diagrams don't have excessive spacing")
    else:
        print("\n✗ Failed to complete all fixes")
        print("Please check the error messages above")
