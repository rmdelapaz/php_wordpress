// Mermaid Text Size Fix - Targeted approach
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
        // Configure Mermaid with larger text
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#f8f9fa',
                primaryTextColor: '#000',
                primaryBorderColor: '#343a40',
                lineColor: '#343a40',
                secondaryColor: '#e9ecef',
                tertiaryColor: '#fff',
                mainBkg: '#f8f9fa',
                secondBkg: '#e9ecef',
                tertiaryBkg: '#dee2e6',
                textColor: '#000',
                nodeTextColor: '#000',
                fontSize: '20px',  // Larger base font size
                fontFamily: '"Arial", "Helvetica", sans-serif'
            },
            flowchart: {
                useMaxWidth: true,
                htmlLabels: false, // Keep false for compatibility
                curve: 'basis',
                nodeSpacing: 150,  // More space for larger text
                rankSpacing: 150,
                diagramPadding: 50,
                padding: 50
            },
            timeline: {
                diagramMarginX: 50,
                diagramMarginY: 10,
                leftMargin: 150,
                width: 150,
                height: 50,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                messageAlign: 'center',
                bottomMarginAdj: 1
            }
        });
        
        // Process all mermaid containers
        const mermaidContainers = document.querySelectorAll('.mermaid');
        if (mermaidContainers.length > 0) {
            mermaid.init(undefined, mermaidContainers);
            
            // After rendering, forcefully increase text sizes
            setTimeout(() => {
                increaseMermaidTextSize();
            }, 800);
        }
    }
    
    function increaseMermaidTextSize() {
        // Target all SVG elements within mermaid containers
        const mermaidSVGs = document.querySelectorAll('.mermaid svg, .mermaid-container svg');
        
        mermaidSVGs.forEach(svg => {
            // Increase all text elements
            const textElements = svg.querySelectorAll('text');
            textElements.forEach(text => {
                // Check if it already has our custom class
                if (!text.classList.contains('mermaid-text-enlarged')) {
                    text.classList.add('mermaid-text-enlarged');
                    
                    // Get current computed style
                    const computedStyle = window.getComputedStyle(text);
                    let currentSize = parseFloat(computedStyle.fontSize);
                    
                    // Ensure minimum size
                    if (!currentSize || currentSize < 20) {
                        currentSize = 20;
                    } else if (currentSize < 24) {
                        currentSize = currentSize * 1.5; // Increase by 50%
                    }
                    
                    // Apply new size with inline style (highest priority)
                    text.setAttribute('style', 
                        `font-size: ${currentSize}px !important; ` +
                        `font-weight: 600 !important; ` +
                        `fill: #000 !important; ` +
                        `font-family: Arial, sans-serif !important;`
                    );
                }
            });
            
            // Handle foreignObject elements (HTML labels)
            const foreignObjects = svg.querySelectorAll('foreignObject');
            foreignObjects.forEach(fo => {
                const divs = fo.querySelectorAll('div, span');
                divs.forEach(div => {
                    if (!div.classList.contains('mermaid-text-enlarged')) {
                        div.classList.add('mermaid-text-enlarged');
                        div.setAttribute('style',
                            'font-size: 20px !important; ' +
                            'font-weight: 600 !important; ' +
                            'color: #000 !important; ' +
                            'font-family: Arial, sans-serif !important;'
                        );
                    }
                });
            });
            
            // Adjust viewBox to prevent cutoff
            const viewBox = svg.getAttribute('viewBox');
            if (viewBox && !svg.hasAttribute('data-viewbox-adjusted')) {
                const [x, y, width, height] = viewBox.split(' ').map(parseFloat);
                // Add padding to prevent text cutoff
                svg.setAttribute('viewBox', `${x - 20} ${y - 20} ${width + 40} ${height + 100}`);
                svg.setAttribute('data-viewbox-adjusted', 'true');
            }
            
            // Ensure SVG has enough height
            if (!svg.style.minHeight || parseInt(svg.style.minHeight) < 400) {
                svg.style.minHeight = '400px';
            }
        });
    }
    
    // Also run on DOMContentLoaded to ensure all elements are ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof mermaid !== 'undefined') {
                setTimeout(increaseMermaidTextSize, 1000);
            }
        });
    } else {
        // DOM is already loaded
        setTimeout(increaseMermaidTextSize, 1000);
    }
    
    // Run again after a delay to catch any late-rendered diagrams
    setTimeout(increaseMermaidTextSize, 2000);
})();
