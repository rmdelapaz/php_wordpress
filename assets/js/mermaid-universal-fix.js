// Mermaid Universal Fix - Initialize Mermaid diagrams (ENHANCED VERSION)
(function() {
    'use strict';
    
    console.log('Mermaid initialization script starting...');
    
    // Check if mermaid is available
    if (typeof mermaid === 'undefined') {
        console.log('Mermaid not found, loading from CDN...');
        // Load Mermaid library dynamically if not present
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
        script.onload = function() {
            console.log('Mermaid loaded successfully');
            initializeMermaid();
        };
        script.onerror = function() {
            console.error('Failed to load Mermaid from CDN');
        };
        document.head.appendChild(script);
    } else {
        console.log('Mermaid already loaded');
        // Mermaid is already loaded
        initializeMermaid();
    }
    
    function initializeMermaid() {
        try {
            console.log('Initializing Mermaid configuration...');
            
            // Configure Mermaid with simpler settings
            mermaid.initialize({
                startOnLoad: false, // We'll manually init
                theme: 'default',
                securityLevel: 'loose', // Allow more flexibility
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis'
                },
                logLevel: 'debug' // Enable debug logging
            });
            
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', processMermaidDiagrams);
            } else {
                processMermaidDiagrams();
            }
            
        } catch (error) {
            console.error('Error initializing Mermaid:', error);
        }
    }
    
    function processMermaidDiagrams() {
        console.log('Processing Mermaid diagrams...');
        
        try {
            // Find all mermaid elements
            const mermaidElements = document.querySelectorAll('pre.mermaid, .mermaid');
            console.log(`Found ${mermaidElements.length} Mermaid diagram(s)`);
            
            if (mermaidElements.length === 0) {
                console.log('No Mermaid diagrams found on this page');
                return;
            }
            
            // Process each diagram individually
            mermaidElements.forEach((element, index) => {
                try {
                    // Get the diagram text
                    const graphDefinition = element.textContent.trim();
                    console.log(`Processing diagram ${index + 1}:`, graphDefinition.substring(0, 50) + '...');
                    
                    // Create a unique ID if not present
                    if (!element.id) {
                        element.id = `mermaid-diagram-${index}`;
                    }
                    
                    // Clear any existing content
                    element.innerHTML = graphDefinition;
                    element.removeAttribute('data-processed');
                    
                    // Try to render the diagram
                    mermaid.init(undefined, element);
                    console.log(`Diagram ${index + 1} processed successfully`);
                    
                } catch (error) {
                    console.error(`Error processing diagram ${index + 1}:`, error);
                    
                    // Try alternative rendering method
                    try {
                        console.log(`Trying alternative rendering for diagram ${index + 1}`);
                        const graphDefinition = element.textContent.trim();
                        const insertSvg = function(svgCode) {
                            element.innerHTML = svgCode;
                        };
                        mermaid.mermaidAPI.render(`mermaid-svg-${index}`, graphDefinition, insertSvg);
                    } catch (altError) {
                        console.error(`Alternative rendering also failed for diagram ${index + 1}:`, altError);
                        element.innerHTML = `<div style="color: red; padding: 10px; border: 1px solid red;">
                            Error rendering Mermaid diagram. Check console for details.
                        </div>`;
                    }
                }
            });
            
        } catch (error) {
            console.error('Error processing Mermaid diagrams:', error);
        }
    }
    
    // Expose function globally for manual triggering if needed
    window.reinitializeMermaid = function() {
        console.log('Manually reinitializing Mermaid...');
        if (typeof mermaid !== 'undefined') {
            processMermaidDiagrams();
        } else {
            console.error('Mermaid is not loaded');
        }
    };
    
    console.log('Mermaid initialization script loaded. Use window.reinitializeMermaid() to manually trigger.');
})();
