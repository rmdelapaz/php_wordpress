/**
 * Mermaid Diagram Initialization - SIMPLE & SAFE VERSION
 * Focuses on reliability over features
 */

(function() {
    'use strict';
    
    // Function to add critical styles
    function addMermaidStyles() {
        const style = document.createElement('style');
        style.innerHTML = `
            .mermaid-diagram {
                margin: 2rem auto;
                padding: 2rem;
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                overflow: visible !important;
                min-height: 400px;
            }
            
            pre.mermaid {
                background: transparent !important;
                border: none !important;
                overflow: visible !important;
                min-height: 350px !important;
                display: block !important;
            }
            
            .mermaid text,
            .mermaid tspan {
                fill: #000000 !important;
                stroke: none !important;
                font-size: 14px !important;
            }
            
            .mermaid .node rect {
                fill: #E8F4FF !important;
                stroke: #5B9BD5 !important;
            }
            
            .mermaid path {
                stroke: #333333 !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Function to initialize Mermaid
    function initMermaid() {
        // Check for mermaid elements
        const mermaidElements = document.querySelectorAll('.mermaid, pre.mermaid');
        if (mermaidElements.length === 0) return;
        
        // Load Mermaid library
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
        script.onload = function() {
            // Initialize when script loads
            window.mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                themeVariables: {
                    primaryColor: '#E8F4FF',
                    primaryTextColor: '#000000',
                    primaryBorderColor: '#5B9BD5'
                },
                flowchart: {
                    htmlLabels: true,
                    curve: 'linear'
                },
                securityLevel: 'loose'
            });
            
            // Run mermaid
            window.mermaid.init();
        };
        script.onerror = function() {
            console.error('Failed to load Mermaid library');
        };
        document.head.appendChild(script);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            addMermaidStyles();
            initMermaid();
        });
    } else {
        addMermaidStyles();
        initMermaid();
    }
})();
