<?php
/**
 * Footer Template
 * Include this file at the bottom of every page
 */

// Include configuration if not already included
if (!defined('SITE_NAME')) {
    require_once __DIR__ . '/config.php';
}
?>
        </main>
        <!-- End Main Content Area -->
        
        <!-- Footer -->
        <footer class="site-footer" role="contentinfo">
            <div class="footer-container">
                <div class="footer-content">
                    <!-- About Section -->
                    <div class="footer-section footer-about">
                        <h3><?php echo SITE_NAME; ?></h3>
                        <p><?php echo SITE_DESCRIPTION; ?></p>
                        
                        <!-- Social Links -->
                        <?php if (!empty($social_links)): ?>
                        <div class="social-links">
                            <?php foreach ($social_links as $platform => $url): ?>
                                <?php if ($url && $url !== '#'): ?>
                                <a href="<?php echo htmlspecialchars($url); ?>" 
                                   class="social-link social-<?php echo $platform; ?>" 
                                   aria-label="Follow us on <?php echo ucfirst($platform); ?>"
                                   target="_blank" 
                                   rel="noopener noreferrer">
                                    <svg class="social-icon" width="20" height="20" fill="currentColor">
                                        <!-- Icons would go here -->
                                    </svg>
                                </a>
                                <?php endif; ?>
                            <?php endforeach; ?>
                        </div>
                        <?php endif; ?>
                    </div>
                    
                    <!-- Quick Links -->
                    <div class="footer-section">
                        <h4>Quick Links</h4>
                        <ul class="footer-links">
                            <li><a href="/">Home</a></li>
                            <li><a href="/module1.html">Start Learning</a></li>
                            <li><a href="/resources.php">Resources</a></li>
                            <li><a href="/about.php">About</a></li>
                        </ul>
                    </div>
                    
                    <!-- Modules -->
                    <div class="footer-section">
                        <h4>Course Modules</h4>
                        <ul class="footer-links">
                            <?php 
                            global $modules;
                            foreach (array_slice($modules, 0, 5, true) as $num => $module): 
                            ?>
                            <li>
                                <a href="/module<?php echo $num; ?>.html">
                                    Module <?php echo $num; ?>
                                </a>
                            </li>
                            <?php endforeach; ?>
                            <li><a href="/#modules">View All Modules →</a></li>
                        </ul>
                    </div>
                    
                    <!-- Contact/Support -->
                    <div class="footer-section">
                        <h4>Support</h4>
                        <ul class="footer-links">
                            <li><a href="/help.php">Help Center</a></li>
                            <li><a href="/faq.php">FAQ</a></li>
                            <li><a href="/contact.php">Contact Us</a></li>
                            <li><a href="/feedback.php">Feedback</a></li>
                        </ul>
                    </div>
                </div>
                
                <!-- Footer Bottom -->
                <div class="footer-bottom">
                    <div class="footer-bottom-content">
                        <p class="copyright">
                            &copy; <?php echo SITE_YEAR; ?> <?php echo SITE_NAME; ?>. All rights reserved.
                        </p>
                        <nav class="footer-bottom-links" aria-label="Footer navigation">
                            <a href="/privacy.php">Privacy Policy</a>
                            <span class="separator">|</span>
                            <a href="/terms.php">Terms of Service</a>
                            <span class="separator">|</span>
                            <a href="/sitemap.php">Sitemap</a>
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
    
    <!-- JavaScript -->
    <script src="<?php echo JS_PATH; ?>/navigation.js"></script>
    
    <!-- Additional scripts -->
    <?php if (isset($additional_scripts)): ?>
        <?php echo $additional_scripts; ?>
    <?php endif; ?>
    
    <!-- Inline Script for Quick Features -->
    <script>
        // Back to Top Button
        (function() {
            const backToTopBtn = document.getElementById('back-to-top');
            if (backToTopBtn) {
                // Show/hide button based on scroll position
                window.addEventListener('scroll', function() {
                    if (window.pageYOffset > 300) {
                        backToTopBtn.classList.add('show');
                    } else {
                        backToTopBtn.classList.remove('show');
                    }
                });
                
                // Scroll to top when clicked
                backToTopBtn.addEventListener('click', function() {
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                });
            }
        })();
        
        // Copy code blocks functionality
        document.querySelectorAll('pre').forEach(function(pre) {
            // Create copy button
            const button = document.createElement('button');
            button.className = 'code-copy-btn';
            button.textContent = 'Copy';
            button.setAttribute('aria-label', 'Copy code');
            
            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.className = 'code-block';
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(pre);
            
            // Create header
            const header = document.createElement('div');
            header.className = 'code-header';
            
            // Add language label if available
            const lang = pre.querySelector('code')?.className.match(/language-(\w+)/);
            if (lang) {
                const langLabel = document.createElement('span');
                langLabel.className = 'code-language';
                langLabel.textContent = lang[1].toUpperCase();
                header.appendChild(langLabel);
            }
            
            header.appendChild(button);
            wrapper.insertBefore(header, pre);
            
            // Copy functionality
            button.addEventListener('click', function() {
                const code = pre.textContent;
                navigator.clipboard.writeText(code).then(function() {
                    button.textContent = 'Copied!';
                    button.classList.add('copied');
                    setTimeout(function() {
                        button.textContent = 'Copy';
                        button.classList.remove('copied');
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy:', err);
                });
            });
        });
    </script>
</body>
</html>