#!/usr/bin/env python3
"""
Script to replace placeholder content in php_string_operators.html with actual content from 02module_old
"""

import re
import os

def extract_code_blocks(content):
    """Extract all code blocks from the old content"""
    code_blocks = []
    
    # Find all <pre> tags with code content
    pre_pattern = r'<pre>(.*?)</pre>'
    matches = re.findall(pre_pattern, content, re.DOTALL)
    
    for match in matches:
        # Clean up the code block
        code = match.strip()
        code_blocks.append(code)
    
    return code_blocks

def replace_placeholders(new_content, code_blocks):
    """Replace placeholder code blocks with actual content"""
    
    # Define the actual code blocks based on the old file
    actual_code_blocks = {
        '###CODE_BLOCK_0###': '''<code class="language-php">&lt;?php
// Basic concatenation examples
$firstName = "John";
$lastName = "Doe";

// Using the concatenation operator (.)
$fullName = $firstName . " " . $lastName;
echo $fullName; // Output: John Doe

// Concatenating multiple strings
$greeting = "Hello, " . $firstName . " " . $lastName . "!";
echo $greeting; // Output: Hello, John Doe!

// Building a sentence
$age = 25;
$city = "New York";
$sentence = "My name is " . $fullName . ", I am " . $age . " years old and live in " . $city . ".";
echo $sentence;
// Output: My name is John Doe, I am 25 years old and live in New York.
?&gt;</code>''',
        
        '###CODE_BLOCK_1###': '''<code class="language-php">&lt;?php
// Understanding the difference between concatenation and addition
$num1 = "5";
$num2 = "3";

// String concatenation with the dot operator
$concatenated = $num1 . $num2;
echo "Concatenation: " . $concatenated; // Output: Concatenation: 53

// Mathematical addition with the plus operator
$added = $num1 + $num2;
echo "Addition: " . $added; // Output: Addition: 8

// Be careful with types!
$a = "10";
$b = "20";
echo $a . $b;  // Output: 1020 (string concatenation)
echo $a + $b;  // Output: 30 (mathematical addition)

// Mixing operators requires parentheses for clarity
$price = 10;
$quantity = 3;
echo "Total: $" . ($price * $quantity); // Output: Total: $30
?&gt;</code>''',
        
        '###CODE_BLOCK_2###': '''<code class="language-php">&lt;?php
// Type conversion in concatenation
$integer = 42;
$float = 3.14159;
$boolean = true;
$null = null;

// PHP automatically converts types to strings
echo "Integer: " . $integer;     // Output: Integer: 42
echo "Float: " . $float;         // Output: Float: 3.14159
echo "Boolean: " . $boolean;     // Output: Boolean: 1 (true becomes 1)
echo "Boolean: " . false;        // Output: Boolean: (false becomes empty string)
echo "Null: " . $null;           // Output: Null: (null becomes empty string)

// Objects need __toString() method
class User {
    public $name =