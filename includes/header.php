<?php
/**
 * Header Template
 * Include this file at the top of every page
 */

// Include configuration if not already included
if (!defined('SITE_NAME')) {
    require_once __DIR__ . '/config.php';
}

// Get current page info
$current_page = get_current_page_info();
$nav_items = get_navigation_items();

// Page-specific variables (can be set before including header)
$page_title = $page_title ?? SITE_NAME;
$page_description = $page_description ?? SITE_DESCRIPTION;
$page_keywords = $page_keywords ?? SITE_KEYWORDS;
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <!-- SEO Meta Tags -->
    <title><?php echo htmlspecialchars($page_title); ?></title>
    <meta name="description" content="<?php echo htmlspecialchars($page_description); ?>">
    <meta name="keywords" content="<?php echo htmlspecialchars($page_keywords); ?>">
    <meta name="author" content="<?php echo SITE_AUTHOR; ?>">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="<?php echo htmlspecialchars($page_title); ?>">
    <meta property="og:description" content="<?php echo htmlspecialchars($page_description); ?>">
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?php echo SITE_URL . $current_page['path']; ?>">
    <meta property="og:image" content="<?php echo SITE_URL . IMG_PATH; ?>/og-image.jpg">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="<?php echo htmlspecialchars($page_title); ?>">
    <meta name="twitter:description" content="<?php echo htmlspecialchars($page_description); ?>">
    <meta name="twitter:image" content="<?php echo SITE_URL . IMG_PATH; ?>/twitter-card.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/favicon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="<?php echo CSS_PATH; ?>/main.css">
    
    <!-- Mermaid for diagrams (if needed) -->
    <?php if ($include_mermaid ?? false): ?>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
    <?php endif; ?>
    
    <!-- Additional head content -->
    <?php if (isset($additional_head)): ?>
        <?php echo $additional_head; ?>
    <?php endif; ?>
</head>
<body>
    <!-- Skip to main content link for accessibility -->
    <a href="#main-content" class="sr-only">Skip to main content</a>
    
    <!-- Page Wrapper -->
    <div class="page-wrapper">
        <!-- Header -->
        <header class="site-header" role="banner">
            <div class="header-container">
                <!-- Logo/Site Title -->
                <div class="site-branding">
                    <a href="/" class="site-logo">
                        <h1 class="site-title"><?php echo SITE_NAME; ?></h1>
                    </a>
                </div>
                
                <!-- Navigation -->
                <nav class="main-navigation" role="navigation" aria-label="Main navigation">
                    <!-- Mobile Menu Button -->
                    <button class="mobile-menu-btn" aria-label="Toggle navigation" aria-expanded="false">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                    
                    <!-- Navigation Menu -->
                    <div class="nav-menu">
                        <ul class="nav-list">
                            <?php foreach ($nav_items as $item): ?>
                                <?php if ($item['type'] === 'dropdown'): ?>
                                    <li class="nav-item dropdown">
                                        <button class="nav-link dropdown-toggle" aria-haspopup="true">
                                            <?php echo htmlspecialchars($item['title']); ?>
                                        </button>
                                        <div class="dropdown-menu" aria-label="<?php echo htmlspecialchars($item['title']); ?> submenu">
                                            <?php foreach ($item['items'] as $subitem): ?>
                                                <a href="<?php echo htmlspecialchars($subitem['url']); ?>" class="dropdown-item">
                                                    <?php echo htmlspecialchars($subitem['title']); ?>
                                                </a>
                                            <?php endforeach; ?>
                                        </div>
                                    </li>
                                <?php else: ?>
                                    <li class="nav-item">
                                        <a href="<?php echo htmlspecialchars($item['url']); ?>" 
                                           class="nav-link <?php echo $current_page['path'] === $item['url'] ? 'active' : ''; ?>">
                                            <?php echo htmlspecialchars($item['title']); ?>
                                        </a>
                                    </li>
                                <?php endif; ?>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                </nav>
                
                <!-- Search -->
                <div class="search-container">
                    <div class="search-input-wrapper">
                        <svg class="search-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                        </svg>
                        <input type="search" class="search-input" placeholder="Search lessons..." aria-label="Search">
                    </div>
                    <div class="search-results" aria-live="polite"></div>
                </div>
            </div>
        </header>
        
        <!-- Progress Bar (if in a module) -->
        <?php if ($current_page['module'] !== null && $show_progress ?? true): ?>
        <div class="progress-container">
            <div class="progress-header">
                <h2 class="progress-title">Course Progress</h2>
                <span class="progress-text">Loading...</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-fill">
                    <span class="progress-bar-text"></span>
                </div>
            </div>
        </div>
        <?php endif; ?>
        
        <!-- Breadcrumb Navigation -->
        <?php if (isset($breadcrumbs) && !empty($breadcrumbs)): ?>
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <ol class="breadcrumb-list">
                <li class="breadcrumb-item">
                    <a href="/">Home</a>
                    <span class="breadcrumb-separator">/</span>
                </li>
                <?php foreach ($breadcrumbs as $index => $crumb): ?>
                    <li class="breadcrumb-item">
                        <?php if ($index === count($breadcrumbs) - 1): ?>
                            <span aria-current="page"><?php echo htmlspecialchars($crumb['title']); ?></span>
                        <?php else: ?>
                            <a href="<?php echo htmlspecialchars($crumb['url']); ?>">
                                <?php echo htmlspecialchars($crumb['title']); ?>
                            </a>
                            <span class="breadcrumb-separator">/</span>
                        <?php endif; ?>
                    </li>
                <?php endforeach; ?>
            </ol>
        </nav>
        <?php endif; ?>
        
        <!-- Main Content Area -->
        <main id="main-content" class="main-content" role="main">
