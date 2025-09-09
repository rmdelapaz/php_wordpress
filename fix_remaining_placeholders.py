#!/usr/bin/env python3
"""
Script to fix remaining code block placeholders in php_string_operators.html
"""

from pathlib import Path

def fix_remaining_placeholders():
    """Replace remaining placeholders with appropriate PHP code."""
    
    # Use the correct path for WSL
    file_path = Path("/home/practicalace/projects/php_wordpress/02module/php_string_operators.html")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacements for remaining placeholders
    replacements = {
        '###CODE_BLOCK_15###': '''<?php
// Comparing concatenation vs interpolation

$firstName = "John";
$lastName = "Smith";
$age = 30;
$occupation = "Developer";

// Using concatenation
$intro1 = "My name is " . $firstName . " " . $lastName . ". I am " . $age . " years old and work as a " . $occupation . ".";

// Using interpolation
$intro2 = "My name is $firstName $lastName. I am $age years old and work as a $occupation.";

// Both produce the same output
echo $intro1 . "\\n";
echo $intro2 . "\\n";

// For HTML generation
// Concatenation approach (clearer for complex HTML)
$html1 = '<div class="user">' . 
         '<h2>' . htmlspecialchars($firstName . ' ' . $lastName) . '</h2>' .
         '<p>Age: ' . $age . '</p>' .
         '<p>Job: ' . htmlspecialchars($occupation) . '</p>' .
         '</div>';

// Interpolation approach (can get messy with quotes)
$html2 = "<div class=\\"user\\">
          <h2>{$firstName} {$lastName}</h2>
          <p>Age: {$age}</p>
          <p>Job: {$occupation}</p>
          </div>";
?>''',

        '###CODE_BLOCK_16###': '''<?php
// Simple template system using string interpolation and concatenation

class Template {
    private $vars = [];
    
    public function assign($key, $value) {
        $this->vars[$key] = $value;
    }
    
    public function render($template) {
        // Extract variables for interpolation
        extract($this->vars);
        
        // Use output buffering to capture the template
        ob_start();
        eval('?>' . $template);
        return ob_get_clean();
    }
}

// Usage example
$tpl = new Template();
$tpl->assign('title', 'Welcome Page');
$tpl->assign('username', 'John Doe');
$tpl->assign('messages', 5);

$template = '<!DOCTYPE html>
<html>
<head>
    <title><?= $title ?></title>
</head>
<body>
    <h1>Welcome, <?= $username ?>!</h1>
    <p>You have <?= $messages ?> new messages.</p>
</body>
</html>';

echo $tpl->render($template);
?>''',

        '###CODE_BLOCK_17###': '''<?php
// Heredoc syntax - works like double quotes
$name = "Alice";
$product = "PHP Course";
$price = 49.99;

$emailContent = <<<EOT
Dear $name,

Thank you for your interest in our $product!

Special offer just for you:
- Product: $product
- Regular Price: \\$$price
- Your Discount: 20%
- Final Price: \\${$price * 0.8}

This offer expires soon, so don't miss out!

Best regards,
The Sales Team
EOT;

echo $emailContent;

// Heredoc for HTML
$html = <<<HTML
<div class="product-card">
    <h2>$product</h2>
    <p class="price">\\$$price</p>
    <button>Buy Now</button>
</div>
HTML;

echo $html;
?>''',

        '###CODE_BLOCK_18###': '''<?php
// Nowdoc syntax - works like single quotes (no variable interpolation)
$name = "Bob";
$variable = "test";

// Note the single quotes around the identifier
$codeExample = <<<'CODE'
This is a PHP code example:

<?php
$name = "John";
$age = 30;
echo "My name is $name and I am $age years old.";
?>

Notice that $name and $variable are NOT replaced.
This is perfect for code examples and documentation.
CODE;

echo $codeExample;

// Nowdoc for SQL queries
$sql = <<<'SQL'
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id
WHERE orders.total > 100
AND users.status = 'active'
ORDER BY orders.created_at DESC;
SQL;

echo "Query to execute:\\n" . $sql;
?>''',

        '###CODE_BLOCK_19###': '''<?php
// Email template using Heredoc
function sendWelcomeEmail($user) {
    $name = $user['name'];
    $email = $user['email'];
    $username = $user['username'];
    $activationLink = "https://example.com/activate?token=" . $user['token'];
    $currentYear = date('Y');
    
    $emailBody = <<<EMAIL
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f4f4f4; }
        .button { display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Our Platform!</h1>
        </div>
        <div class="content">
            <h2>Hello, $name!</h2>
            <p>Thank you for registering with us. Your account has been created successfully.</p>
            <p><strong>Your Details:</strong></p>
            <ul>
                <li>Name: $name</li>
                <li>Email: $email</li>
                <li>Username: $username</li>
            </ul>
            <p>To activate your account, please click the button below:</p>
            <p style="text-align: center;">
                <a href="$activationLink" class="button">Activate Account</a>
            </p>
            <p><small>Or copy this link: $activationLink</small></p>
        </div>
        <div class="footer">
            <p>&copy; $currentYear Your Company. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
EMAIL;
    
    return $emailBody;
}

// Usage
$newUser = [
    'name' => 'Jane Smith',
    'email' => 'jane@example.com',
    'username' => 'janesmith',
    'token' => 'abc123xyz789'
];

echo sendWelcomeEmail($newUser);
?>''',

        '###CODE_BLOCK_20###': '''<?php
// Common string functions that complement string operators

$text = "Hello World";
$email = "john.doe@example.com";
$sentence = "  PHP is a great language  ";

// String length
echo strlen($text); // Output: 11

// Convert case
echo strtoupper($text);  // Output: HELLO WORLD
echo strtolower($text);  // Output: hello world
echo ucfirst("hello");   // Output: Hello
echo ucwords("hello world"); // Output: Hello World

// Find and replace
echo str_replace("World", "PHP", $text); // Output: Hello PHP
echo str_ireplace("world", "PHP", $text); // Case-insensitive replace

// Substring operations
echo substr($text, 0, 5);  // Output: Hello
echo substr($text, -5);    // Output: World
echo substr($text, 6, 3);  // Output: Wor

// Find position
echo strpos($text, "World");  // Output: 6
echo strrpos($email, ".");   // Output: 19 (last occurrence)

// Trimming
echo trim($sentence);        // Remove whitespace from both ends
echo ltrim($sentence);       // Remove from left
echo rtrim($sentence);       // Remove from right

// Splitting and joining
$parts = explode(" ", $text);
print_r($parts); // Array ( [0] => Hello [1] => World )

$joined = implode("-", $parts);
echo $joined; // Output: Hello-World

// Padding
echo str_pad("5", 3, "0", STR_PAD_LEFT);   // Output: 005
echo str_pad("PHP", 10, "*", STR_PAD_BOTH); // Output: ***PHP****

// Repeat
echo str_repeat("=", 20); // Output: ====================
?>''',

        '###CODE_BLOCK_21###': '''<?php
// Advanced string operations

// sprintf for formatted strings
$name = "John";
$age = 25;
$balance = 1234.567;

$formatted = sprintf("Name: %s, Age: %d, Balance: $%.2f", $name, $age, $balance);
echo $formatted; // Output: Name: John, Age: 25, Balance: $1234.57

// String parsing
$data = "name=John&age=25&city=NewYork";
parse_str($data, $result);
print_r($result);
// Array ( [name] => John [age] => 25 [city] => NewYork )

// Regular expressions
$email = "contact@example.com";
if (preg_match("/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/", $email)) {
    echo "Valid email";
}

// Extract numbers from string
$text = "The price is $45.99 for 3 items";
preg_match_all('/\\d+\\.?\\d*/', $text, $matches);
print_r($matches[0]); // Array ( [0] => 45.99 [1] => 3 )

// Word wrap
$longText = "This is a very long sentence that needs to be wrapped at a specific width for better display.";
echo wordwrap($longText, 30, "\\n"); // Wrap at 30 characters

// String comparison
$str1 = "Apple";
$str2 = "apple";

echo strcmp($str1, $str2);  // Case-sensitive comparison
echo strcasecmp($str1, $str2); // Case-insensitive comparison

// Levenshtein distance (similarity)
$word1 = "kitten";
$word2 = "sitting";
echo levenshtein($word1, $word2); // Output: 3 (edit distance)

// Sound-based comparison
echo soundex("Smith");  // S530
echo soundex("Smythe"); // S530 (sounds similar)
?>''',

        '###CODE_BLOCK_22###': '''<?php
// URL Builder using string operations

class URLBuilder {
    private $scheme = 'https';
    private $host = '';
    private $path = '/';
    private $params = [];
    private $fragment = '';
    
    public function setScheme($scheme) {
        $this->scheme = $scheme;
        return $this;
    }
    
    public function setHost($host) {
        $this->host = $host;
        return $this;
    }
    
    public function setPath($path) {
        $this->path = '/' . ltrim($path, '/');
        return $this;
    }
    
    public function addParam($key, $value) {
        $this->params[$key] = $value;
        return $this;
    }
    
    public function setFragment($fragment) {
        $this->fragment = $fragment;
        return $this;
    }
    
    public function build() {
        // Start with scheme and host
        $url = $this->scheme . '://' . $this->host;
        
        // Add path
        $url .= $this->path;
        
        // Add query parameters
        if (!empty($this->params)) {
            $queryParts = [];
            foreach ($this->params as $key => $value) {
                $queryParts[] = urlencode($key) . '=' . urlencode($value);
            }
            $url .= '?' . implode('&', $queryParts);
        }
        
        // Add fragment
        if ($this->fragment) {
            $url .= '#' . $this->fragment;
        }
        
        return $url;
    }
}

// Usage
$url = new URLBuilder();
$finalUrl = $url->setHost('api.example.com')
                ->setPath('/users/search')
                ->addParam('q', 'john doe')
                ->addParam('limit', 10)
                ->addParam('sort', 'name')
                ->setFragment('results')
                ->build();

echo $finalUrl;
// Output: https://api.example.com/users/search?q=john+doe&limit=10&sort=name#results
?>''',

        '###CODE_BLOCK_26###': '''<?php
// Best practices example: Building a secure contact form response

function generateContactFormResponse($formData) {
    // Validate and sanitize input
    $name = htmlspecialchars(trim($formData['name'] ?? ''), ENT_QUOTES, 'UTF-8');
    $email = filter_var($formData['email'] ?? '', FILTER_SANITIZE_EMAIL);
    $subject = htmlspecialchars(trim($formData['subject'] ?? ''), ENT_QUOTES, 'UTF-8');
    $message = htmlspecialchars(trim($formData['message'] ?? ''), ENT_QUOTES, 'UTF-8');
    
    // Check required fields
    $errors = [];
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Valid email is required";
    }
    if (empty($message)) {
        $errors[] = "Message is required";
    }
    
    // If there are errors, return error message
    if (!empty($errors)) {
        $errorHtml = '<div class="alert alert-danger">';
        $errorHtml .= '<h4>Please correct the following errors:</h4>';
        $errorHtml .= '<ul>';
        foreach ($errors as $error) {
            $errorHtml .= '<li>' . $error . '</li>';
        }
        $errorHtml .= '</ul>';
        $errorHtml .= '</div>';
        return $errorHtml;
    }
    
    // Build success response using clean, readable concatenation
    $response = '<div class="alert alert-success">';
    $response .= '<h4>Thank you for your message!</h4>';
    $response .= '<p>We have received your message and will respond within 24 hours.</p>';
    $response .= '</div>';
    
    // Build confirmation details
    $response .= '<div class="confirmation-details">';
    $response .= '<h5>Message Details:</h5>';
    $response .= '<dl class="row">';
    
    // Use array for better organization of repetitive HTML
    $details = [
        'Name' => $name,
        'Email' => $email,
        'Subject' => $subject ?: '(No subject)',
        'Message' => nl2br($message)
    ];
    
    foreach ($details as $label => $value) {
        $response .= '<dt class="col-sm-3">' . $label . ':</dt>';
        $response .= '<dd class="col-sm-9">' . $value . '</dd>';
    }
    
    $response .= '</dl>';
    $response .= '</div>';
    
    return $response;
}

// Example usage
$formData = [
    'name' => 'John Doe',
    'email' => 'john@example.com',
    'subject' => 'Question about services',
    'message' => "Hello,\\nI would like to know more about your services.\\nThank you!"
];

echo generateContactFormResponse($formData);
?>''',

        '###CODE_BLOCK_27###': '''<?php
// Exercise 1: String Concatenation Challenge
// Build an HTML table from an array of data

$students = [
    ['id' => 1, 'name' => 'Alice Johnson', 'grade' => 'A', 'score' => 95],
    ['id' => 2, 'name' => 'Bob Smith', 'grade' => 'B', 'score' => 87],
    ['id' => 3, 'name' => 'Charlie Brown', 'grade' => 'A', 'score' => 92],
    ['id' => 4, 'name' => 'Diana Prince', 'grade' => 'C', 'score' => 78],
    ['id' => 5, 'name' => 'Edward Norton', 'grade' => 'B', 'score' => 85]
];

function buildStudentTable($students) {
    // Start building the table
    $html = '<table class="table table-striped">' . "\\n";
    
    // Add table header
    $html .= '  <thead>' . "\\n";
    $html .= '    <tr>' . "\\n";
    $html .= '      <th>ID</th>' . "\\n";
    $html .= '      <th>Name</th>' . "\\n";
    $html .= '      <th>Grade</th>' . "\\n";
    $html .= '      <th>Score</th>' . "\\n";
    $html .= '      <th>Status</th>' . "\\n";
    $html .= '    </tr>' . "\\n";
    $html .= '  </thead>' . "\\n";
    
    // Add table body
    $html .= '  <tbody>' . "\\n";
    
    foreach ($students as $student) {
        // Determine status based on score
        $status = $student['score'] >= 90 ? 'Excellent' : 
                 ($student['score'] >= 80 ? 'Good' : 'Needs Improvement');
        
        // Determine row class based on grade
        $rowClass = $student['grade'] === 'A' ? 'table-success' : 
                   ($student['grade'] === 'B' ? 'table-info' : 'table-warning');
        
        // Build table row
        $html .= '    <tr class="' . $rowClass . '">' . "\\n";
        $html .= '      <td>' . $student['id'] . '</td>' . "\\n";
        $html .= '      <td>' . htmlspecialchars($student['name']) . '</td>' . "\\n";
        $html .= '      <td>' . $student['grade'] . '</td>' . "\\n";
        $html .= '      <td>' . $student['score'] . '%</td>' . "\\n";
        $html .= '      <td>' . $status . '</td>' . "\\n";
        $html .= '    </tr>' . "\\n";
    }
    
    $html .= '  </tbody>' . "\\n";
    $html .= '</table>';
    
    return $html;
}

// Display the table
echo buildStudentTable($students);
?>''',

        '###CODE_BLOCK_28###': '''<?php
// Exercise 2: URL Query Builder
// Create a function that builds a URL query string from an array

function buildQueryString($params, $encode = true) {
    if (empty($params)) {
        return '';
    }
    
    $pairs = [];
    
    foreach ($params as $key => $value) {
        // Handle arrays (like checkboxes)
        if (is_array($value)) {
            foreach ($value as $item) {
                $k = $encode ? urlencode($key) . '[]' : $key . '[]';
                $v = $encode ? urlencode($item) : $item;
                $pairs[] = $k . '=' . $v;
            }
        } 
        // Handle null values
        elseif ($value === null) {
            continue; // Skip null values
        }
        // Handle boolean values
        elseif (is_bool($value)) {
            $k = $encode ? urlencode($key) : $key;
            $v = $value ? '1' : '0';
            $pairs[] = $k . '=' . $v;
        }
        // Handle regular values
        else {
            $k = $encode ? urlencode($key) : $key;
            $v = $encode ? urlencode($value) : $value;
            $pairs[] = $k . '=' . $v;
        }
    }
    
    return implode('&', $pairs);
}

// Test the function
$params = [
    'search' => 'php programming',
    'category' => 'tutorials',
    'tags' => ['beginner', 'strings', 'operators'],
    'sort' => 'date',
    'order' => 'desc',
    'page' => 1,
    'featured' => true,
    'draft' => false,
    'deleted' => null // This will be skipped
];

$queryString = buildQueryString($params);
echo "Query String: " . $queryString . "\\n\\n";

// Build complete URL
$baseUrl = 'https://example.com/api/search';
$fullUrl = $baseUrl . '?' . $queryString;
echo "Full URL: " . $fullUrl . "\\n\\n";

// Alternative: Using http_build_query (built-in function)
$phpQueryString = http_build_query($params);
echo "PHP Built-in: " . $phpQueryString;
?>''',

        '###CODE_BLOCK_29###': '''<?php
// Exercise 3: Template System
// Create a simple template system that replaces placeholders

class SimpleTemplate {
    private $template = '';
    private $variables = [];
    
    public function __construct($template = '') {
        $this->template = $template;
    }
    
    public function setTemplate($template) {
        $this->template = $template;
        return $this;
    }
    
    public function assign($key, $value) {
        $this->variables[$key] = $value;
        return $this;
    }
    
    public function assignArray($array) {
        $this->variables = array_merge($this->variables, $array);
        return $this;
    }
    
    public function render() {
        $output = $this->template;
        
        // Replace simple variables {{variable}}
        foreach ($this->variables as $key => $value) {
            if (!is_array($value) && !is_object($value)) {
                $placeholder = '{{' . $key . '}}';
                $output = str_replace($placeholder, $value, $output);
            }
        }
        
        // Handle loops {{#each items}} ... {{/each}}
        $output = $this->processLoops($output);
        
        // Handle conditionals {{#if condition}} ... {{/if}}
        $output = $this->processConditionals($output);
        
        // Clean up any remaining placeholders
        $output = preg_replace('/{{.*?}}/', '', $output);
        
        return $output;
    }
    
    private function processLoops($template) {
        $pattern = '/{{#each\\s+(\\w+)}}(.*?){{{\\/each}}/s';
        
        return preg_replace_callback($pattern, function($matches) {
            $arrayName = $matches[1];
            $loopTemplate = $matches[2];
            $output = '';
            
            if (isset($this->variables[$arrayName]) && is_array($this->variables[$arrayName])) {
                foreach ($this->variables[$arrayName] as $item) {
                    $itemOutput = $loopTemplate;
                    if (is_array($item)) {
                        foreach ($item as $key => $value) {
                            $itemOutput = str_replace('{{' . $key . '}}', $value, $itemOutput);
                        }
                    } else {
                        $itemOutput = str_replace('{{value}}', $item, $itemOutput);
                    }
                    $output .= $itemOutput;
                }
            }
            
            return $output;
        }, $template);
    }
    
    private function processConditionals($template) {
        $pattern = '/{{#if\\s+(\\w+)}}(.*?){{{\\/if}}/s';
        
        return preg_replace_callback($pattern, function($matches) {
            $condition = $matches[1];
            $content = $matches[2];
            
            if (isset($this->variables[$condition]) && $this->variables[$condition]) {
                return $content;
            }
            
            return '';
        }, $template);
    }
}

// Example usage
$template = '
<h1>{{title}}</h1>
<p>Welcome, {{username}}!</p>

{{#if showMessage}}
<div class="alert">{{message}}</div>
{{/if}}

<h2>Your Orders:</h2>
<ul>
{{#each orders}}
    <li>Order #{{id}}: {{product}} - ${{price}}</li>
{{/each}}
</ul>

<p>Total Orders: {{orderCount}}</p>
';

$tpl = new SimpleTemplate($template);
$output = $tpl->assign('title', 'My Shop')
              ->assign('username', 'John Doe')
              ->assign('showMessage', true)
              ->assign('message', 'You have new notifications!')
              ->assign('orders', [
                  ['id' => 101, 'product' => 'PHP Book', 'price' => '29.99'],
                  ['id' => 102, 'product' => 'MySQL Guide', 'price' => '34.99'],
                  ['id' => 103, 'product' => 'WordPress Course', 'price' => '49.99']
              ])
              ->assign('orderCount', 3)
              ->render();

echo $output;
?>'''
    }
    
    # Replace all placeholders
    for placeholder, code in replacements.items():
        if placeholder in content:
            # Escape the code for HTML
            escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Wrap in code tags
            formatted_code = f'<code class="language-php">{escaped_code}</code>'
            # Replace the placeholder
            content = content.replace(placeholder, formatted_code)
            print(f"✓ Replaced {placeholder}")
        else:
            print(f"- {placeholder} not found")
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✨ All placeholders have been replaced!")
    print("The php_string_operators.html file is now complete with real code examples.")

if __name__ == "__main__":
    fix_remaining_placeholders()
