/**
 * Mermaid Universal Fix v2 - Complete Solution
 * Handles all diagram types with proper text rendering
 */

(function() {
    'use strict';
    
    // Clear any previous initialization attempts
    if (window.mermaid) {
        delete window.mermaid;
        delete window.mermaidAPI;
    }
    
    // Mark as v2 to override old versions
    window.mermaidFixVersion = 2;
    
    console.log('Mermaid Universal Fix v2: Starting...');
    
    // Remove any old mermaid scripts
    const oldScripts = document.querySelectorAll('script[src*="mermaid"]');
    oldScripts.forEach(script => {
        if (script.src.includes('cdn')) {
            script.remove();
            console.log('Removed old mermaid script:', script.src);
        }
    });
    
    // Add comprehensive styles (with !important to override)
    const styleId = 'mermaid-fix-styles-v2';
    let existingStyle = document.getElementById(styleId);
    if (existingStyle) {
        existingStyle.remove();
    }
    
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
        .mermaid-container {
            padding: 20px !important;
            background: #fff !important;
            border: 2px solid #e5e7eb !important;
            border-radius: 8px !important;
            margin: 20px auto !important;
            overflow: visible !important;
            display: flex !important;
            justify-content: center !important;
            min-height: 400px !important;
        }
        
        .mermaid {
            display: inline-block !important;
            text-align: center !important;
            margin: 0 auto !important;
            width: 100% !important;
        }
        
        .mermaid svg {
            display: block !important;
            margin: 0 auto !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 350px !important;
        }
        
        /* Force all text to be visible */
        .mermaid text,
        .mermaid tspan {
            fill: #000 !important;
            stroke: none !important;
            font-size: 14px !important;
            font-family: Arial, sans-serif !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Node styling */
        .mermaid .node rect,
        .mermaid .node circle,
        .mermaid .node polygon,
        .mermaid rect.actor {
            fill: #e8f4ff !important;
            stroke: #5b9bd5 !important;
            stroke-width: 2px !important;
        }
        
        /* Style nodes based on fill directives */
        .mermaid rect[fill="#f8f9fa"] { fill: #f8f9fa !important; }
        .mermaid rect[fill="#e9ecef"] { fill: #e9ecef !important; }
        .mermaid rect[fill="#dee2e6"] { fill: #dee2e6 !important; }
    `;
    document.head.appendChild(style);
    
    // Clean and prepare Mermaid code with enhanced handling
    function cleanMermaidCode(text) {
        // Decode HTML entities first
        const temp = document.createElement('div');
        temp.innerHTML = text;
        text = temp.textContent || temp.innerText || '';
        
        // Remove excessive indentation
        const lines = text.split('\n');
        let minIndent = Infinity;
        
        lines.forEach(line => {
            if (line.trim()) {
                const match = line.match(/^(\s*)/);
                if (match) {
                    minIndent = Math.min(minIndent, match[1].length);
                }
            }
        });
        
        if (minIndent < Infinity && minIndent > 0) {
            text = lines.map(line => line.substring(minIndent)).join('\n');
        }
        
        // Fix various label patterns
        // 1. Handle compound labels with commas
        text = text.replace(/\["([^"]+),\s*([^"]+),\s*([^"]+)"\]/g, '["$1 | $2 | $3"]');
        text = text.replace(/\["([^"]+),\s*([^"]+)"\]/g, '["$1 | $2"]');
        
        // 2. HTML tags - ensure they're properly escaped
        text = text.replace(/\["<(!?)([^>]+)>"\]/g, '["&lt;$1$2&gt;"]');
        text = text.replace(/\["<\/([^>]+)>"\]/g, '["&lt;/$1&gt;"]');
        
        // 3. Forward slashes in folder names
        text = text.replace(/\[([^"\[\]]*\/[^"\[\]]*)\]/g, function(match, content) {
            if (!content.includes('"')) {
                return '["' + content + '"]';
            }
            return match;
        });
        
        // 4. Fix any remaining problematic patterns
        text = text.replace(/\[","\]/g, '["..."]');
        
        console.log('Cleaned diagram code sample:', text.substring(0, 300));
        
        return text.trim();
    }
    
    // Convert pre to div with better handling
    function convertPreToDiv() {
        const pres = document.querySelectorAll('pre.mermaid');
        console.log('Found ' + pres.length + ' pre.mermaid elements to convert');
        
        pres.forEach((pre, index) => {
            // Get raw content
            let text = pre.innerHTML;
            
            // Clean it
            text = cleanMermaidCode(text);
            
            // Create new div
            const div = document.createElement('div');
            div.className = 'mermaid';
            div.setAttribute('data-original-index', index.toString());
            div.textContent = text;
            
            // Replace pre with div
            if (pre.parentNode) {
                pre.parentNode.replaceChild(div, pre);
            }
            
            console.log('Converted diagram ' + index);
        });
    }
    
    // Initialize and render with Mermaid 9.4.3
    function initAndRender() {
        console.log('Loading Mermaid 9.4.3...');
        
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@9.4.3/dist/mermaid.min.js';
        
        script.onload = function() {
            console.log('Mermaid 9.4.3 loaded successfully');
            
            // Configure Mermaid
            window.mermaid.initialize({
                startOnLoad: false,
                theme: 'default',
                flowchart: {
                    htmlLabels: false,  // Force SVG text
                    useMaxWidth: true,
                    rankSpacing: 60,
                    nodeSpacing: 40,
                    curve: 'linear',
                    padding: 15
                },
                themeVariables: {
                    fontSize: '14px'
                },
                securityLevel: 'loose'
            });
            
            // Render all diagrams
            const divs = document.querySelectorAll('div.mermaid');
            console.log('Rendering ' + divs.length + ' diagrams...');
            
            divs.forEach((div, index) => {
                const graphDef = div.textContent;
                const uniqueId = 'mermaid-v2-' + Date.now() + '-' + index;
                
                try {
                    // Clear the div
                    div.innerHTML = '';
                    div.id = uniqueId;
                    
                    // Render with Mermaid
                    window.mermaid.mermaidAPI.render(
                        uniqueId + '-svg',
                        graphDef,
                        function(svgCode) {
                            div.innerHTML = svgCode;
                            console.log('Rendered diagram ' + index);
                            
                            // Post-process the SVG
                            setTimeout(() => {
                                const svg = div.querySelector('svg');
                                if (svg) {
                                    // Fix text visibility
                                    const texts = svg.querySelectorAll('text, tspan');
                                    texts.forEach(t => {
                                        t.style.fill = '#000';
                                        t.style.stroke = 'none';
                                    });
                                    
                                    // Fix viewBox centering
                                    const viewBox = svg.getAttribute('viewBox');
                                    if (viewBox) {
                                        const parts = viewBox.split(' ').map(Number);
                                        if (parts[0] < -80) {
                                            // Adjust for better centering
                                            svg.setAttribute('viewBox', `0 ${parts[1]} ${parts[2]} ${parts[3]}`);
                                            console.log('Centered diagram ' + index);
                                        }
                                    }
                                }
                            }, 100);
                        }
                    );
                } catch (error) {
                    console.error('Error rendering diagram ' + index + ':', error);
                    div.innerHTML = `<p style="color: red;">Error rendering diagram: ${error.message}</p>`;
                }
            });
        };
        
        script.onerror = function() {
            console.error('Failed to load Mermaid library');
        };
        
        document.head.appendChild(script);
    }
    
    // Main execution function
    function executeFixV2() {
        console.log('Executing Mermaid Fix v2...');
        
        // Step 1: Convert pre to div
        convertPreToDiv();
        
        // Step 2: Wait a bit then initialize and render
        setTimeout(initAndRender, 200);
    }
    
    // Wait for DOM and execute
    if (document.readyState === 'complete') {
        executeFixV2();
    } else {
        window.addEventListener('load', executeFixV2);
    }
    
    // Provide manual trigger
    window.rerunMermaidFix = executeFixV2;
})();
