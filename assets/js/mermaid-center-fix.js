// Mermaid Centering Fix
// This script ensures Mermaid diagrams are properly centered after rendering
(function() {
    'use strict';
    
    function centerMermaidDiagrams() {
        // Find all mermaid containers with the center fix class
        const centerFixContainers = document.querySelectorAll('.mermaid-center-fix');
        
        centerFixContainers.forEach(function(container) {
            // Find the SVG element that Mermaid generates
            const svg = container.querySelector('svg');
            
            if (svg) {
                // Remove any max-width inline style that Mermaid adds
                if (svg.style.maxWidth) {
                    svg.style.removeProperty('max-width');
                }
                
                // Adjust the SVG positioning to be more left-aligned
                svg.style.display = 'inline-block';
                svg.style.marginLeft = '-20px'; // Shift left
                svg.style.marginRight = 'auto';
                
                // Get the parent container of the SVG (the div Mermaid creates)
                const svgContainer = svg.parentElement;
                if (svgContainer && svgContainer.id && svgContainer.id.startsWith('mermaid')) {
                    svgContainer.style.textAlign = 'left';
                    svgContainer.style.display = 'inline-block';
                    svgContainer.style.width = 'auto';
                    svgContainer.style.paddingLeft = '0';
                }
                
                // Find the wrapper div and adjust its alignment
                const wrapperDiv = container.querySelector('.mermaid-wrapper');
                if (wrapperDiv) {
                    // Ensure the wrapper maintains the left shift
                    wrapperDiv.style.textAlign = 'center';
                    wrapperDiv.style.paddingLeft = '50px';
                }
                
                // Also check for the pre.mermaid element
                const preMermaid = container.querySelector('pre.mermaid');
                if (preMermaid) {
                    // After Mermaid processes, it might be replaced with a div
                    // Check if there's a div with id starting with 'mermaid'
                    const mermaidDiv = container.querySelector('div[id^="mermaid"]');
                    if (mermaidDiv) {
                        mermaidDiv.style.textAlign = 'left';
                        mermaidDiv.style.display = 'inline-block';
                        mermaidDiv.style.width = 'auto';
                        mermaidDiv.style.marginLeft = '-30px';
                    }
                }
            }
        });
    }
    
    // Run the centering fix after Mermaid initialization
    if (typeof mermaid !== 'undefined') {
        // Hook into Mermaid's callback system if available
        const originalInit = mermaid.init;
        mermaid.init = function() {
            const result = originalInit.apply(this, arguments);
            setTimeout(centerMermaidDiagrams, 100);
            return result;
        };
        
        // Also run after mermaid.run if it's used
        if (mermaid.run) {
            const originalRun = mermaid.run;
            mermaid.run = function() {
                const result = originalRun.apply(this, arguments);
                setTimeout(centerMermaidDiagrams, 100);
                return result;
            };
        }
    }
    
    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(centerMermaidDiagrams, 500);
        });
    } else {
        // DOM is already loaded
        setTimeout(centerMermaidDiagrams, 500);
    }
    
    // Also run on window load to catch any late rendering
    window.addEventListener('load', function() {
        setTimeout(centerMermaidDiagrams, 1000);
    });
    
    // MutationObserver to catch when Mermaid modifies the DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.tagName === 'SVG' || (node.id && node.id.startsWith('mermaid')))) {
                        setTimeout(centerMermaidDiagrams, 100);
                    }
                });
            }
        });
    });
    
    // Observe the entire document for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();
