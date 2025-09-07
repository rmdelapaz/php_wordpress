/**
 * Mermaid Universal Fix - SIMPLE WORKING VERSION
 * Back to basics - just make it work
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mermaid Fix: Starting...');
    
    // Load Mermaid library
    if (typeof window.mermaid === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@9.4.3/dist/mermaid.min.js';
        script.onload = function() {
            console.log('Mermaid library loaded');
            initializeMermaid();
        };
        document.head.appendChild(script);
    } else {
        initializeMermaid();
    }
});

function initializeMermaid() {
    // Simple configuration
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: {
            htmlLabels: true,
            curve: 'linear'
        }
    });
    
    // Fix text visibility
    setInterval(function() {
        document.querySelectorAll('.mermaid text, .mermaid tspan').forEach(function(el) {
            el.style.fill = '#000000';
            el.style.stroke = 'none';
            el.setAttribute('fill', '#000000');
        });
    }, 500);
}
