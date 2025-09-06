/**
 * Sidebar Toggle Functionality
 * Allows users to hide/show the sidebar with state persistence
 */

(function() {
    'use strict';

    // Check if sidebar exists
    const sidebar = document.querySelector('.sidebar, aside.sidebar');
    if (!sidebar) return;

    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.className = 'sidebar-toggle';
    toggleButton.setAttribute('aria-label', 'Toggle Sidebar');
    toggleButton.setAttribute('title', 'Toggle Sidebar (Ctrl+B)');
    toggleButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
    `;

    // Create backdrop for mobile
    const backdrop = document.createElement('div');
    backdrop.className = 'sidebar-backdrop';

    // Insert elements
    document.body.appendChild(toggleButton);
    document.body.appendChild(backdrop);

    // Load saved state from localStorage
    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true') {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        forceReflow();
    }

    // Force browser to recalculate layout
    function forceReflow() {
        // Force the browser to recalculate styles
        const mainContent = document.querySelector('.main-content, main, #main-content');
        if (mainContent) {
            // Trigger reflow
            void mainContent.offsetHeight;
            
            // Force repaint
            mainContent.style.display = 'none';
            mainContent.offsetHeight; // Trigger reflow
            mainContent.style.display = '';
            
            // Dispatch resize event for any scripts that need it
            window.dispatchEvent(new Event('resize'));
        }
    }

    // Toggle function
    function toggleSidebar() {
        const isCollapsed = sidebar.classList.contains('collapsed');
        
        if (isCollapsed) {
            // Show sidebar
            sidebar.classList.remove('collapsed');
            document.body.classList.remove('sidebar-collapsed');
            localStorage.setItem('sidebarCollapsed', 'false');
            showStateIndicator('Sidebar shown');
        } else {
            // Hide sidebar
            sidebar.classList.add('collapsed');
            document.body.classList.add('sidebar-collapsed');
            localStorage.setItem('sidebarCollapsed', 'true');
            showStateIndicator('Sidebar hidden');
        }
        
        // Force layout recalculation
        forceReflow();
        
        // Trigger any responsive tables or charts to redraw
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 350); // After animation completes
    }

    // Show temporary state indicator
    function showStateIndicator(message) {
        // Create or get indicator
        let indicator = document.querySelector('.sidebar-state-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'sidebar-state-indicator';
            sidebar.appendChild(indicator);
        }

        // Show message
        indicator.textContent = message;
        indicator.classList.add('show');
        
        // Hide after 2 seconds
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 2000);
    }

    // Event listeners
    toggleButton.addEventListener('click', toggleSidebar);
    
    // Close sidebar on backdrop click (mobile)
    backdrop.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    });

    // Keyboard shortcut (Ctrl/Cmd + B)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            toggleSidebar();
        }
    });

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (window.innerWidth > 768) {
                backdrop.classList.remove('active');
            }
            forceReflow();
        }, 250);
    });

    // Add keyboard navigation for sidebar links when visible
    const sidebarLinks = sidebar.querySelectorAll('.sidebar-link');
    let currentFocusIndex = -1;

    document.addEventListener('keydown', (e) => {
        // Only work when sidebar is visible
        if (sidebar.classList.contains('collapsed')) return;

        // Alt + S to focus sidebar
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            if (sidebarLinks.length > 0) {
                currentFocusIndex = 0;
                sidebarLinks[currentFocusIndex].focus();
            }
        }

        // Arrow navigation when sidebar link is focused
        if (document.activeElement.classList.contains('sidebar-link')) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                currentFocusIndex = (currentFocusIndex + 1) % sidebarLinks.length;
                sidebarLinks[currentFocusIndex].focus();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                currentFocusIndex = currentFocusIndex <= 0 ? sidebarLinks.length - 1 : currentFocusIndex - 1;
                sidebarLinks[currentFocusIndex].focus();
            }
        }
    });

    // Auto-hide sidebar on small screens initially
    if (window.innerWidth <= 768 && savedState === null) {
        sidebar.classList.add('collapsed');
        document.body.classList.add('sidebar-collapsed');
        forceReflow();
    }

    // Initial reflow to ensure proper layout
    setTimeout(() => {
        forceReflow();
    }, 100);

    console.log('Sidebar toggle initialized. Use Ctrl/Cmd+B to toggle.');
})();
