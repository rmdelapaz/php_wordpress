// Navigation and Progress Tracking System
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize navigation
    initializeNavigation();
    initializeProgressTracker();
    initializeSearch();
    
    // Navigation initialization
    function initializeNavigation() {
        // Mobile menu toggle
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const navMenu = document.querySelector('.nav-menu');
        
        if (mobileMenuBtn && navMenu) {
            mobileMenuBtn.addEventListener('click', function() {
                navMenu.classList.toggle('active');
                this.classList.toggle('active');
                
                // Update aria-expanded
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                this.setAttribute('aria-expanded', !isExpanded);
            });
        }
        
        // Dropdown menus
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const dropdown = this.nextElementSibling;
                if (dropdown) {
                    dropdown.classList.toggle('show');
                    this.classList.toggle('active');
                }
            });
        });
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
                document.querySelectorAll('.dropdown-toggle.active').forEach(toggle => {
                    toggle.classList.remove('active');
                });
            }
        });
    }
    
    // Progress tracker
    function initializeProgressTracker() {
        // Get or create progress data
        let progress = localStorage.getItem('courseProgress');
        if (!progress) {
            progress = {};
            localStorage.setItem('courseProgress', JSON.stringify(progress));
        } else {
            progress = JSON.parse(progress);
        }
        
        // Mark current page as visited
        const currentPage = window.location.pathname;
        if (!progress[currentPage]) {
            progress[currentPage] = {
                visited: true,
                completed: false,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('courseProgress', JSON.stringify(progress));
        }
        
        // Update progress bar
        updateProgressBar(progress);
        
        // Add complete lesson button functionality
        const completeBtn = document.querySelector('.complete-lesson-btn');
        if (completeBtn) {
            // Check if already completed
            if (progress[currentPage] && progress[currentPage].completed) {
                completeBtn.textContent = '✓ Completed';
                completeBtn.classList.add('completed');
            }
            
            completeBtn.addEventListener('click', function() {
                progress[currentPage].completed = !progress[currentPage].completed;
                localStorage.setItem('courseProgress', JSON.stringify(progress));
                
                if (progress[currentPage].completed) {
                    this.textContent = '✓ Completed';
                    this.classList.add('completed');
                } else {
                    this.textContent = 'Mark as Complete';
                    this.classList.remove('completed');
                }
                
                updateProgressBar(progress);
            });
        }
    }
    
    // Update progress bar
    function updateProgressBar(progress) {
        const progressBar = document.querySelector('.progress-bar-fill');
        const progressText = document.querySelector('.progress-text');
        
        if (progressBar && progressText) {
            // Count total lessons (based on navigation links)
            const totalLessons = document.querySelectorAll('.lesson-link').length || 50; // fallback
            const completedLessons = Object.values(progress).filter(p => p.completed).length;
            
            const percentage = Math.round((completedLessons / totalLessons) * 100);
            progressBar.style.width = percentage + '%';
            progressText.textContent = `${completedLessons} of ${totalLessons} lessons completed (${percentage}%)`;
        }
    }
    
    // Search functionality
    function initializeSearch() {
        const searchInput = document.querySelector('.search-input');
        const searchResults = document.querySelector('.search-results');
        
        if (searchInput && searchResults) {
            let searchIndex = null;
            
            // Load search index
            fetch('/assets/data/search-index.json')
                .then(response => response.json())
                .then(data => {
                    searchIndex = data;
                })
                .catch(error => console.error('Error loading search index:', error));
            
            // Handle search input
            searchInput.addEventListener('input', debounce(function() {
                const query = this.value.toLowerCase().trim();
                
                if (query.length < 2) {
                    searchResults.classList.remove('show');
                    return;
                }
                
                if (!searchIndex) {
                    searchResults.innerHTML = '<div class="search-result">Loading search index...</div>';
                    searchResults.classList.add('show');
                    return;
                }
                
                // Perform search
                const results = performSearch(query, searchIndex);
                displaySearchResults(results, searchResults);
            }, 300));
            
            // Close search results when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.search-container')) {
                    searchResults.classList.remove('show');
                }
            });
        }
    }
    
    // Perform search
    function performSearch(query, index) {
        const results = [];
        const queryWords = query.split(' ').filter(word => word.length > 0);
        
        index.forEach(item => {
            let score = 0;
            const titleLower = item.title.toLowerCase();
            const contentLower = (item.content || '').toLowerCase();
            
            queryWords.forEach(word => {
                // Title matches (higher weight)
                if (titleLower.includes(word)) {
                    score += 10;
                }
                // Content matches
                if (contentLower.includes(word)) {
                    score += 1;
                }
                // Tag matches
                if (item.tags && item.tags.some(tag => tag.toLowerCase().includes(word))) {
                    score += 5;
                }
            });
            
            if (score > 0) {
                results.push({
                    ...item,
                    score: score
                });
            }
        });
        
        // Sort by score
        results.sort((a, b) => b.score - a.score);
        
        return results.slice(0, 10); // Return top 10 results
    }
    
    // Display search results
    function displaySearchResults(results, container) {
        if (results.length === 0) {
            container.innerHTML = '<div class="search-result">No results found</div>';
        } else {
            container.innerHTML = results.map(result => `
                <a href="${result.url}" class="search-result">
                    <div class="search-result-title">${highlightText(result.title)}</div>
                    <div class="search-result-module">${result.module || ''}</div>
                </a>
            `).join('');
        }
        container.classList.add('show');
    }
    
    // Highlight search terms (basic implementation)
    function highlightText(text) {
        // This is a simple implementation - can be enhanced
        return text;
    }
    
    // Debounce utility
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func.apply(this, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Previous/Next navigation
    const prevBtn = document.querySelector('.prev-lesson');
    const nextBtn = document.querySelector('.next-lesson');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            if (this.hasAttribute('disabled')) {
                e.preventDefault();
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            if (this.hasAttribute('disabled')) {
                e.preventDefault();
            }
        });
    }
});
