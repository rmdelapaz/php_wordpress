<?php
/**
 * Site Configuration
 * Central configuration file for the PHP WordPress course website
 */

// Site Information
define('SITE_NAME', 'PHP WordPress Development');
define('SITE_DESCRIPTION', 'Complete Web Development Course - From HTML to WordPress');
define('SITE_AUTHOR', 'PHP WordPress Course');
define('SITE_KEYWORDS', 'PHP, WordPress, Web Development, Programming, HTML, CSS, JavaScript');
define('SITE_URL', 'http://localhost/php_wordpress');
define('SITE_YEAR', date('Y'));

// Asset paths
define('ASSETS_PATH', '/assets');
define('CSS_PATH', ASSETS_PATH . '/css');
define('JS_PATH', ASSETS_PATH . '/js');
define('IMG_PATH', ASSETS_PATH . '/images');

// Module Information
$modules = [
    1 => [
        'title' => 'Web Development Fundamentals',
        'folder' => '01module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'Core technologies of web development: HTML, CSS, JavaScript, and PHP introduction.'
    ],
    2 => [
        'title' => 'PHP Fundamentals',
        'folder' => '02module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'Deep dive into PHP programming, from syntax to object-oriented programming.'
    ],
    3 => [
        'title' => 'Database Development with MySQL',
        'folder' => '03module',
        'duration' => '1 week',
        'sessions' => 5,
        'description' => 'Database design, SQL, and PHP-MySQL interaction.'
    ],
    4 => [
        'title' => 'WordPress Fundamentals & Docker',
        'folder' => '04module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'WordPress architecture, containerization with Docker, and website building.'
    ],
    5 => [
        'title' => 'WordPress Theme Development',
        'folder' => '05module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'Creating custom WordPress themes from scratch.'
    ],
    6 => [
        'title' => 'WordPress Plugin Development',
        'folder' => '06module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'Developing custom WordPress plugins to extend functionality.'
    ],
    7 => [
        'title' => 'Advanced WordPress Development',
        'folder' => '07module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'REST API, custom post types, taxonomies, and advanced topics.'
    ],
    8 => [
        'title' => 'WordPress Deployment, Docker & Maintenance',
        'folder' => '08module',
        'duration' => '1 week',
        'sessions' => 5,
        'description' => 'Best practices for deployment, security, and maintenance.'
    ],
    9 => [
        'title' => 'Final Project',
        'folder' => '09module',
        'duration' => '2 weeks',
        'sessions' => 10,
        'description' => 'Apply everything learned to build a complete WordPress application.'
    ]
];

// Social Media Links (Optional)
$social_links = [
    'twitter' => '#',
    'github' => 'https://github.com',
    'linkedin' => '#',
    'youtube' => '#'
];

// Navigation Structure
function get_navigation_items() {
    global $modules;
    $nav_items = [
        ['title' => 'Home', 'url' => '/', 'type' => 'link'],
        ['title' => 'Modules', 'url' => '#', 'type' => 'dropdown', 'items' => []],
        ['title' => 'Resources', 'url' => '/resources.php', 'type' => 'link'],
        ['title' => 'About', 'url' => '/about.php', 'type' => 'link']
    ];
    
    // Build module dropdown
    foreach ($modules as $num => $module) {
        $nav_items[1]['items'][] = [
            'title' => "Module $num: " . $module['title'],
            'url' => "/module$num.html"
        ];
    }
    
    return $nav_items;
}

// Helper function to get current page info
function get_current_page_info() {
    $current_file = basename($_SERVER['PHP_SELF']);
    $current_path = $_SERVER['REQUEST_URI'];
    
    return [
        'file' => $current_file,
        'path' => $current_path,
        'is_home' => ($current_file == 'index.php' || $current_file == 'index.html'),
        'module' => extract_module_number($current_path)
    ];
}

// Extract module number from path
function extract_module_number($path) {
    if (preg_match('/module(\d+)/', $path, $matches)) {
        return (int)$matches[1];
    }
    if (preg_match('/(\d{2})module/', $path, $matches)) {
        return (int)$matches[1];
    }
    return null;
}

// Get lesson navigation (prev/next)
function get_lesson_navigation($current_file, $module_folder) {
    // This would need to be implemented based on your actual file structure
    // For now, returning empty array
    return [
        'prev' => null,
        'next' => null
    ];
}
?>