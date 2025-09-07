/**
 * MERMAID FIX - REMOVE LEFT PADDING
 * Directly addresses the left-side spacing issue
 */

(function() {
    'use strict';
    
    console.log('=== MERMAID CENTERING FIX ===');
    
    // Add styles to remove left padding and center
    const style = document.createElement('style');
    style.textContent = `
        .mermaid-diagram,
        .mermaid-container {
            padding: 20px;
            background: #fff;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            margin: 20px auto;
            overflow-x: auto;
            overflow-y: visible;
        }
        
        .mermaid {
            display: block;
            text-align: left;  /* Changed from center */
            margin: 0;
            padding: 0;
        }
        
        .mermaid svg {
            display: block;
            margin: 0;
            padding: 0;
            transform: translateX(0);  /* Reset any transform */
        }
        
        /* Override any g transform that adds padding */
        .mermaid svg > g {
            transform: translate(20px, 20px) !important;  /* Small consistent padding */
        }
        
        /* Ensure node backgrounds are visible */
        .mermaid rect {
            fill: #E8F4FF !important;
            stroke: #5B9BD5 !important;
        }
        
        /* Text should be visible */
        .mermaid text {
            fill: #000 !important;
        }
    `;
    document.head.appendChild(style);
    
    // Convert pre to div
    function convertPreToDiv() {
        const pres = document.querySelectorAll('pre.mermaid');
        console.log('Found ' + pres.length + ' pre.mermaid elements');
        
        pres.forEach((pre) => {
            let text = pre.textContent || '';
            const lines = text.split('\n');
            let minIndent = Infinity;
            
            lines.forEach(line => {
                if (line.trim()) {
                    const indent = line.match(/^(\s*)/)[1].length;
                    minIndent = Math.min(minIndent, indent);
                }
            });
            
            if (minIndent < Infinity) {
                text = lines.map(line => line.substring(minIndent)).join('\n').trim();
            }
            
            const div = document.createElement('div');
            div.className = 'mermaid';
            div.textContent = text;
            pre.parentNode.replaceChild(div, pre);
        });
    }
    
    // Fix SVG positioning after render
    function fixSVGPositioning() {
        const svgs = document.querySelectorAll('.mermaid svg');
        console.log('Fixing positioning for ' + svgs.length + ' SVGs');
        
        svgs.forEach((svg, index) => {
            // Get the viewBox
            const viewBox = svg.getAttribute('viewBox');
            if (viewBox) {
                const [x, y, width, height] = viewBox.split(' ').map(Number);
                console.log('SVG ' + index + ' viewBox:', x, y, width, height);
                
                // If x is large negative, adjust it
                if (x < -50) {
                    svg.setAttribute('viewBox', '0 0 ' + (width + Math.abs(x)) + ' ' + height);
                    console.log('Adjusted viewBox to remove left padding');
                }
            }
            
            // Check the main g element transform
            const g = svg.querySelector('g');
            if (g) {
                const transform = g.getAttribute('transform');
                console.log('Main g transform:', transform);
            }
        });
    }
    
    // Initialize Mermaid
    function initMermaid() {
        if (window.mermaid) {
            delete window.mermaid;
        }
        
        console.log('Loading Mermaid 9.1.7...');
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@9.1.7/dist/mermaid.min.js';
        
        script.onload = function() {
            console.log('Mermaid loaded');
            
            // Initialize
            window.mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                flowchart: {
                    htmlLabels: false,
                    useMaxWidth: true,  /* Changed to true */
                    rankSpacing: 50,
                    nodeSpacing: 30,
                    curve: 'linear',
                    padding: 15  /* Reduced padding */
                }
            });
            
            // Render
            const divs = document.querySelectorAll('.mermaid');
            divs.forEach((div, index) => {
                try {
                    const graphDef = div.textContent;
                    const id = 'mermaid-' + index;
                    div.innerHTML = '';
                    div.id = id;
                    
                    window.mermaid.mermaidAPI.render(
                        id + '-svg',
                        graphDef,
                        function(svgCode) {
                            div.innerHTML = svgCode;
                            console.log('Rendered diagram ' + index);
                        }
                    );
                } catch (e) {
                    console.error('Error:', e);
                }
            });
            
            // Fix positioning after rendering
            setTimeout(fixSVGPositioning, 500);
        };
        
        document.head.appendChild(script);
    }
    
    // Main
    function main() {
        convertPreToDiv();
        setTimeout(initMermaid, 100);
    }
    
    // Run
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', main);
    } else {
        main();
    }
    
    // Manual fix
    window.fixMermaidPosition = fixSVGPositioning;
})();
