// Mermaid Fix v2 - Initialize Mermaid diagrams
(function() {
    'use strict';
    
    // Check if mermaid is available
    if (typeof mermaid === 'undefined') {
        // Load Mermaid library dynamically if not present
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
        script.onload = function() {
            initializeMermaid();
        };
        document.head.appendChild(script);
    } else {
        // Mermaid is already loaded
        initializeMermaid();
    }
    
    function initializeMermaid() {
        // Configure Mermaid
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#f8f9fa',
                primaryTextColor: '#343a40',
                primaryBorderColor: '#343a40',
                lineColor: '#343a40',
                secondaryColor: '#e9ecef',
                tertiaryColor: '#fff'
            },
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
        
        // Process all mermaid containers
        const mermaidContainers = document.querySelectorAll('.mermaid');
        if (mermaidContainers.length > 0) {
            mermaid.init(undefined, mermaidContainers);
        }
    }
    
    // Also run on DOMContentLoaded to ensure all elements are ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof mermaid !== 'undefined') {
                initializeMermaid();
            }
        });
    }
})();
