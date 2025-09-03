// Site Configuration and Template Components
const SiteConfig = {
    siteName: 'PHP WordPress Development',
    siteDescription: 'Complete Web Development Course - From HTML to WordPress',
    siteAuthor: 'PHP WordPress Course',
    siteYear: new Date().getFullYear(),
    
    modules: [
        {
            number: 1,
            title: 'Web Development Fundamentals',
            folder: '01module',
            duration: '2 weeks',
            sessions: 10,
            description: 'Core technologies of web development: HTML, CSS, JavaScript, and PHP introduction.'
        },
        {
            number: 2,
            title: 'PHP Fundamentals',
            folder: '02module',
            duration: '2 weeks',
            sessions: 10,
            description: 'Deep dive into PHP programming, from syntax to object-oriented programming.'
        },
        {
            number: 3,
            title: 'Database Development with MySQL',
            folder: '03module',
            duration: '1 week',
            sessions: 5,
            description: 'Database design, SQL, and PHP-MySQL interaction.'
        },
        {
            number: 4,
            title: 'WordPress Fundamentals & Docker',
            folder: '04module',
            duration: '2 weeks',
            sessions: 10,
            description: 'WordPress architecture, containerization with Docker, and website building.'
        },
        {
            number: 5,
            title: 'WordPress Theme Development',
            folder: '05module',
            duration: '2 weeks',
            sessions: 10,
            description: 'Creating custom WordPress themes from scratch.'
        },
        {
            number: 6,
            title: 'WordPress Plugin Development',
            folder: '06module',
            duration: '2 weeks',
            sessions: 10,
            description: 'Developing custom WordPress plugins to extend functionality.'
        },
        {
            number: 7,
            title: 'Advanced WordPress Development',
            folder: '07module',
            duration: '2 weeks',
            sessions: 10,
            description: 'REST API, custom post types, taxonomies, and advanced topics.'
        },
        {
            number: 8,
            title: 'WordPress Deployment & Maintenance',
            folder: '08module',
            duration: '1 week',
            sessions: 5,
            description: 'Best practices for deployment, security, and maintenance.'
        },
        {
            number: 9,
            title: 'Final Project',
            folder: '09module',
            duration: '2 weeks',
            sessions: 10,
            description: 'Apply everything learned to build a complete WordPress application.'
        }
    ],
    
    navigation: [
        { title: 'Home', url: '/', type: 'link' },
        { 
            title: 'Modules', 
            url: '#', 
            type: 'dropdown',
            items: [] // Will be populated from modules
        },
        { title: 'Resources', url: '/resources.html', type: 'link' },
        { title: 'About', url: '/about.html', type: 'link' }
    ]
};

// Populate module dropdown
SiteConfig.modules.forEach(module => {
    SiteConfig.navigation[1].items.push({
        title: `Module ${module.number}: ${module.title}`,
        url: `/module${module.number}.html`
    });
});

// Template Components
class TemplateComponents {
    static createHeader(pageTitle = '', showProgress = false) {
        const currentPath = window.location.pathname;
        
        return `
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
                                <h1 class="site-title">${SiteConfig.siteName}</h1>
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
                                    ${SiteConfig.navigation.map(item => {
                                        if (item.type === 'dropdown') {
                                            return `
                                                <li class="nav-item dropdown">
                                                    <button class="nav-link dropdown-toggle" aria-haspopup="true">
                                                        ${item.title}
                                                    </button>
                                                    <div class="dropdown-menu" aria-label="${item.title} submenu">
                                                        ${item.items.map(subitem => `
                                                            <a href="${subitem.url}" class="dropdown-item">
                                                                ${subitem.title}
                                                            </a>
                                                        `).join('')}
                                                    </div>
                                                </li>
                                            `;
                                        } else {
                                            const isActive = currentPath === item.url ? 'active' : '';
                                            return `
                                                <li class="nav-item">
                                                    <a href="${item.url}" class="nav-link ${isActive}">
                                                        ${item.title}
                                                    </a>
                                                </li>
                                            `;
                                        }
                                    }).join('')}
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
                
                ${showProgress ? `
                <!-- Progress Bar -->
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
                ` : ''}
                
                <!-- Main Content Area -->
                <main id="main-content" class="main-content" role="main">
        `;
    }
    
    static createFooter() {
        return `
                </main>
                <!-- End Main Content Area -->
                
                <!-- Footer -->
                <footer class="site-footer" role="contentinfo">
                    <div class="footer-container">
                        <div class="footer-content">
                            <!-- About Section -->
                            <div class="footer-section footer-about">
                                <h3>${SiteConfig.siteName}</h3>
                                <p>${SiteConfig.siteDescription}</p>
                            </div>
                            
                            <!-- Quick Links -->
                            <div class="footer-section">
                                <h4>Quick Links</h4>
                                <ul class="footer-links">
                                    <li><a href="/">Home</a></li>
                                    <li><a href="/module1.html">Start Learning</a></li>
                                    <li><a href="/resources.html">Resources</a></li>
                                    <li><a href="/about.html">About</a></li>
                                </ul>
                            </div>
                            
                            <!-- Modules -->
                            <div class="footer-section">
                                <h4>Course Modules</h4>
                                <ul class="footer-links">
                                    ${SiteConfig.modules.slice(0, 5).map(module => `
                                        <li><a href="/module${module.number}.html">Module ${module.number}</a></li>
                                    `).join('')}
                                    <li><a href="/#modules">View All Modules →</a></li>
                                </ul>
                            </div>
                            
                            <!-- Contact/Support -->
                            <div class="footer-section">
                                <h4>Support</h4>
                                <ul class="footer-links">
                                    <li><a href="/help.html">Help Center</a></li>
                                    <li><a href="/faq.html">FAQ</a></li>
                                    <li><a href="/contact.html">Contact Us</a></li>
                                    <li><a href="/feedback.html">Feedback</a></li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- Footer Bottom -->
                        <div class="footer-bottom">
                            <div class="footer-bottom-content">
                                <p class="copyright">
                                    &copy; ${SiteConfig.siteYear} ${SiteConfig.siteName}. All rights reserved.
                                </p>
                                <nav class="footer-bottom-links" aria-label="Footer navigation">
                                    <a href="/privacy.html">Privacy Policy</a>
                                    <span class="separator">|</span>
                                    <a href="/terms.html">Terms of Service</a>
                                    <span class="separator">|</span>
                                    <a href="/sitemap.html">Sitemap</a>
                                </nav>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
            <!-- End Page Wrapper -->
            
            <!-- Back to Top Button -->
            <button id="back-to-top" class="back-to-top" aria-label="Back to top">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 19V5M12 5l-7 7M12 5l7 7"/>
                </svg>
            </button>
        `;
    }
    
    static createBreadcrumb(items) {
        if (!items || items.length === 0) return '';
        
        return `
            <nav class="breadcrumb" aria-label="Breadcrumb">
                <ol class="breadcrumb-list">
                    <li class="breadcrumb-item">
                        <a href="/">Home</a>
                        <span class="breadcrumb-separator">/</span>
                    </li>
                    ${items.map((item, index) => {
                        const isLast = index === items.length - 1;
                        if (isLast) {
                            return `
                                <li class="breadcrumb-item">
                                    <span aria-current="page">${item.title}</span>
                                </li>
                            `;
                        } else {
                            return `
                                <li class="breadcrumb-item">
                                    <a href="${item.url}">${item.title}</a>
                                    <span class="breadcrumb-separator">/</span>
                                </li>
                            `;
                        }
                    }).join('')}
                </ol>
            </nav>
        `;
    }
    
    static createLessonNavigation(prevLesson, nextLesson) {
        return `
            <div class="lesson-navigation">
                ${prevLesson ? `
                    <a href="${prevLesson.url}" class="lesson-nav-button prev">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"/>
                        </svg>
                        <span>
                            <small>Previous</small><br>
                            ${prevLesson.title}
                        </span>
                    </a>
                ` : '<div></div>'}
                
                <button class="complete-lesson-btn">
                    Mark as Complete
                </button>
                
                ${nextLesson ? `
                    <a href="${nextLesson.url}" class="lesson-nav-button next">
                        <span>
                            <small>Next</small><br>
                            ${nextLesson.title}
                        </span>
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"/>
                        </svg>
                    </a>
                ` : '<div></div>'}
            </div>
        `;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SiteConfig, TemplateComponents };
}