#!/usr/bin/env python3
"""
Script to identify and report files with missing code blocks (###CODE_BLOCK_N### placeholders).
This will help understand the scope of the problem and what needs to be fixed.
"""

from pathlib import Path
import re

def check_for_code_placeholders(file_path):
    """Check if a file contains unresolved code block placeholders."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find all code block placeholders
        placeholders = re.findall(r'###CODE_BLOCK_\d+###', content)
        
        # Also check for <pre> tags with these placeholders
        pre_placeholders = re.findall(r'<pre>###CODE_BLOCK_\d+###</pre>', content)
        
        return len(placeholders), pre_placeholders
        
    except Exception as e:
        return 0, []

def analyze_modules():
    """Analyze both old and new module directories for code placeholder issues."""
    
    old_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module_old")
    new_module_dir = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\02module")
    
    # Check if directories exist
    if not old_module_dir.exists():
        old_module_dir = Path("/home/practicalace/projects/php_wordpress/02module_old")
        new_module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
    
    print("=" * 70)
    print(" Code Block Placeholder Analysis")
    print("=" * 70)
    
    # Analyze OLD module files
    print("\n02module_old Analysis:")
    print("-" * 70)
    
    old_files_with_placeholders = []
    old_html_files = list(old_module_dir.glob("*.html"))
    
    for file_path in sorted(old_html_files):
        count, pre_blocks = check_for_code_placeholders(file_path)
        if count > 0:
            old_files_with_placeholders.append((file_path.name, count))
            print(f"  {file_path.name:<50} {count} placeholders")
    
    # Analyze NEW module files  
    print("\n02module Analysis:")
    print("-" * 70)
    
    new_files_with_placeholders = []
    new_html_files = list(new_module_dir.glob("*.html"))
    
    for file_path in sorted(new_html_files):
        count, pre_blocks = check_for_code_placeholders(file_path)
        if count > 0:
            new_files_with_placeholders.append((file_path.name, count))
            print(f"  {file_path.name:<50} {count} placeholders")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  Old module: {len(old_files_with_placeholders)} files with placeholders")
    print(f"  New module: {len(new_files_with_placeholders)} files with placeholders")
    
    return old_files_with_placeholders, new_files_with_placeholders

def generate_placeholder_code(placeholder_num):
    """Generate appropriate code content for a placeholder."""
    # This would need to be customized based on the context
    # For now, return a generic PHP code example
    
    code_templates = {
        0: """<?php
// Basic concatenation example
$firstName = "John";
$lastName = "Doe";

// Using the concatenation operator (.)
$fullName = $firstName . " " . $lastName;
echo $fullName; // Output: John Doe

// Concatenating multiple strings
$greeting = "Hello, " . $firstName . " " . $lastName . "!";
echo $greeting; // Output: Hello, John Doe!
?>""",
        1: """<?php
// Concatenation vs Addition
$num1 = "5";
$num2 = "3";

// String concatenation
$concat = $num1 . $num2;
echo $concat; // Output: 53

// Mathematical addition
$sum = $num1 + $num2;
echo $sum; // Output: 8

// Mixing types
$text = "The sum is: " . ($num1 + $num2);
echo $text; // Output: The sum is: 8
?>""",
        2: """<?php
// Type conversion in concatenation
$number = 42;
$boolean = true;
$float = 3.14;

// PHP automatically converts to string
$result = "Number: " . $number;       // "Number: 42"
$result = "Boolean: " . $boolean;     // "Boolean: 1"
$result = "Float: " . $float;         // "Float: 3.14"

// Array warning
$array = [1, 2, 3];
// $result = "Array: " . $array;      // Warning: Array to string conversion
$result = "Array: " . implode(", ", $array); // "Array: 1, 2, 3"
?>""",
        3: """<?php
// Dynamic HTML generation
$products = [
    ['name' => 'Laptop', 'price' => 999.99],
    ['name' => 'Mouse', 'price' => 29.99],
    ['name' => 'Keyboard', 'price' => 79.99]
];

$html = '<table class="products">';
$html .= '<thead><tr><th>Product</th><th>Price</th></tr></thead>';
$html .= '<tbody>';

foreach ($products as $product) {
    $html .= '<tr>';
    $html .= '<td>' . htmlspecialchars($product['name']) . '</td>';
    $html .= '<td>$' . number_format($product['price'], 2) . '</td>';
    $html .= '</tr>';
}

$html .= '</tbody></table>';
echo $html;
?>"""
    }
    
    # Return template based on number, or default
    return code_templates.get(placeholder_num, code_templates[0])

def create_fix_script():
    """Create a script to fix the placeholder issues."""
    
    fix_script = '''#!/usr/bin/env python3
"""
Script to handle code block placeholders in HTML files.
Since the original code blocks are missing, this provides a solution.
"""

from pathlib import Path
import re

def fix_code_placeholders(file_path):
    """Replace code placeholders with actual code examples."""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if file has placeholders
    if '###CODE_BLOCK_' not in content:
        return False, "No placeholders found"
    
    # For php_string_operators.html specifically, we need string operation examples
    if 'php_string_operators' in str(file_path):
        replacements = {
            '###CODE_BLOCK_0###': """<?php
// Basic concatenation
$firstName = "John";
$lastName = "Doe";
$fullName = $firstName . " " . $lastName;
echo $fullName; // Output: John Doe

// Multiple concatenations
$greeting = "Hello, " . $firstName . " " . $lastName . "!";
echo $greeting; // Output: Hello, John Doe!
?>""",
            '###CODE_BLOCK_1###': """<?php
// Concatenation vs Addition
$a = "5";
$b = "3";

// String concatenation
echo $a . $b;  // Output: 53

// Mathematical addition  
echo $a + $b;  // Output: 8

// Mixed operations
echo "Result: " . ($a + $b); // Output: Result: 8
?>""",
            '###CODE_BLOCK_2###': """<?php
// Type conversion examples
$number = 42;
$float = 3.14159;
$boolean = true;

echo "Integer: " . $number;     // Output: Integer: 42
echo "Float: " . $float;        // Output: Float: 3.14159
echo "Boolean: " . $boolean;    // Output: Boolean: 1

// Arrays need special handling
$array = ['apple', 'banana'];
echo "Fruits: " . implode(", ", $array); // Output: Fruits: apple, banana
?>""",
            # Add more as needed...
        }
        
        # Replace all found placeholders
        for placeholder, code in replacements.items():
            content = content.replace(placeholder, code)
    
    # Generic replacements for other files
    else:
        # Replace with generic PHP examples
        for i in range(30):  # Handle up to 30 placeholders
            placeholder = f'###CODE_BLOCK_{i}###'
            if placeholder in content:
                # Generate contextual code based on file name and position
                code = f"""<?php
// Code example {i}
// This is a placeholder that needs proper content
// TODO: Add appropriate code for this section

echo "Example code block {i}";
?>"""
                content = content.replace(placeholder, code)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)
    
    return True, "Placeholders replaced"

def main():
    """Process files with placeholder issues."""
    
    module_dir = Path(r"\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\02module")
    
    if not module_dir.exists():
        module_dir = Path("/home/practicalace/projects/php_wordpress/02module")
    
    # List of files known to have placeholder issues
    files_to_fix = [
        'php_string_operators.html',
        # Add other files as identified
    ]
    
    print("Fixing code placeholders...")
    
    for filename in files_to_fix:
        file_path = module_dir / filename
        if file_path.exists():
            success, message = fix_code_placeholders(file_path)
            print(f"  {filename}: {message}")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path(r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress\fix_code_placeholders.py")
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(fix_script)
    
    print(f"\nCreated fix script: {script_path.name}")

def main():
    """Main analysis function."""
    
    # Analyze the situation
    old_issues, new_issues = analyze_modules()
    
    print("\n" + "=" * 70)
    print("ANALYSIS RESULTS:")
    print("-" * 70)
    
    print("\nThe Issue:")
    print("  The source files (02module_old) contain placeholder markers like ###CODE_BLOCK_N###")
    print("  instead of actual code examples. These placeholders were copied as-is to the new files.")
    
    print("\nPossible Causes:")
    print("  1. The original files were templates waiting for code to be inserted")
    print("  2. A build process that should have replaced placeholders didn't run")
    print("  3. The actual code blocks are stored separately and need to be merged")
    
    print("\nSolutions:")
    print("  1. Find the original code blocks if they exist separately")
    print("  2. Generate appropriate code examples for each placeholder")
    print("  3. Use a different source that has complete content")
    
    # Create fix script
    create_fix_script()
    
    print("\nNext Steps:")
    print("  1. Check if there's a separate file with the actual code blocks")
    print("  2. Run fix_code_placeholders.py to add generic code examples")
    print("  3. Manually review and update with appropriate code for each section")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
