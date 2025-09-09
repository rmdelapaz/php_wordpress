#!/usr/bin/env python3
"""
Fix Module 03 and 04 HTML files to match the structure of Modules 01 and 02
This script works with Windows WSL paths
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import sys

class ModuleFixer:
    def __init__(self, base_path: str):
        """Initialize the module fixer with the base project path"""
        self.base_path = Path(base_path)
        self.module3_structure = {}
        self.module4_structure = {}
        
    def parse_module_overview(self, module_num: int) -> Dict:
        """Parse module overview HTML to extract session structure"""
        module_file = self.base_path / f"module{module_num}.html"
        
        if not module_file.exists():
            print(f"Warning: {module_file} not found")
            return {}
        
        with open(module_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        structure = {}
        sessions = soup.find_all('div', class_='session')
        
        for session in sessions:
            session_title = session.find('h3')
            if not session_title:
                continue
                
            session_name = session_title.text.strip()
            
            # Extract links for this session
            links = []
            for link in session.find_all('a', class_='lesson-link'):
                href = link.get('href', '')
                text = link.text.strip()
                if href and text:
                    # Extract just the filename
                    filename = href.split('/')[-1]
                    links.append({
                        'href': href,
                        'filename': filename,
                        'text': text
                    })
            
            structure[session_name] = links
        
        return structure

    def fix_css_links(self, soup: BeautifulSoup) -> bool:
        """Fix CSS links to include all necessary stylesheets"""
        head = soup.find('head')
        if not head:
            return False
        
        # Remove existing main.css link
        existing_css = head.find_all('link', {'href': re.compile(r'/assets/css/main\.css')})
        for css in existing_css:
            css.decompose()
        
        # Find where to insert CSS (after last meta tag or charset)
        insert_after = None
        for tag in head.children:
            if tag.name in ['meta', 'title']:
                insert_after = tag
        
        # Create new CSS links
        css_links = [
            {'href': '/assets/css/main.css', 'rel': 'stylesheet'},
            {'href': '/assets/css/sidebar-enhanced.css', 'rel': 'stylesheet'},
            {'href': '/assets/css/sidebar-toggle.css', 'rel': 'stylesheet'}
        ]
        
        for css in css_links:
            new_link = soup.new_tag('link', href=css['href'], rel=css['rel'])
            if insert_after:
                insert_after.insert_after(new_link)
                insert_after = new_link
        
        return True

    def fix_javascript_includes(self, soup: BeautifulSoup) -> bool:
        """Add missing JavaScript files"""
        body = soup.find('body')
        if not body:
            return False
        
        # Check if sidebar-toggle.js already exists
        existing_sidebar_js = body.find('script', {'src': '/assets/js/sidebar-toggle.js'})
        if existing_sidebar_js:
            return True
        
        # Find site-config.js
        site_config = body.find('script', {'src': '/assets/js/site-config.js'})
        
        if site_config:
            # Add sidebar-toggle.js after site-config.js
            new_script = soup.new_tag('script', src='/assets/js/sidebar-toggle.js')
            site_config.insert_after(new_script)
        else:
            # Add both navigation.js, site-config.js and sidebar-toggle.js before closing body
            scripts = [
                '/assets/js/navigation.js',
                '/assets/js/site-config.js', 
                '/assets/js/sidebar-toggle.js'
            ]
            
            # Find mermaid script or last script tag
            last_script = None
            for script in body.find_all('script'):
                if 'mermaid' not in str(script):
                    last_script = script
            
            for script_src in scripts:
                new_script = soup.new_tag('script', src=script_src)
                if last_script:
                    last_script.insert_after(new_script)
                    last_script = new_script
                else:
                    body.append(new_script)
        
        return True

    def create_sidebar_html(self, module_num: int, current_file: str, structure: Dict) -> str:
        """Create properly structured sidebar HTML"""
        module_names = {
            3: "MySQL Database",
            4: "WordPress & Docker"
        }
        
        module_name = module_names.get(module_num, f"Module {module_num}")
        
        sidebar_html = f'''<aside class="sidebar">
    <div class="sidebar-nav">
        <h3 class="sidebar-title">Module {module_num}: {module_name}</h3>'''
        
        # Add sessions
        for session_name, lessons in structure.items():
            # Extract session number if present
            session_match = re.match(r'Session (\d+):', session_name)
            if session_match:
                session_title = session_name
            else:
                session_title = session_name
            
            sidebar_html += f'''
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">{session_title}</h4>
            <ul class="sidebar-menu">'''
            
            for lesson in lessons:
                # Check if this is the current page
                is_active = lesson['filename'] == current_file
                active_class = ' class="active"' if is_active else ''
                link_class = ' class="sidebar-link active"' if is_active else ' class="sidebar-link"'
                
                sidebar_html += f'''
                <li{active_class}><a{link_class} href="{lesson['href']}">{lesson['text']}</a></li>'''
            
            sidebar_html += '''
            </ul>
        </div>'''
        
        # Add Quick Links section
        prev_module = module_num - 1
        next_module = module_num + 1
        
        sidebar_html += f'''
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Quick Links</h4>
            <ul class="sidebar-menu">
                <li><a class="sidebar-link" href="/module{module_num}.html">Module Overview</a></li>
                <li><a class="sidebar-link prev-session" href="/module{prev_module}.html">← Prev: Module {prev_module}</a></li>
                <li><a class="sidebar-link next-session" href="/module{next_module}.html">Next: Module {next_module} →</a></li>
                <li><a class="sidebar-link" href="/resources.html">Resources</a></li>
            </ul>
        </div>
    </div>
</aside>'''
        
        return sidebar_html

    def fix_sidebar(self, soup: BeautifulSoup, module_num: int, filename: str, structure: Dict) -> bool:
        """Replace existing sidebar with properly structured one"""
        # Find existing sidebar
        sidebar = soup.find('aside', class_='sidebar')
        
        if not sidebar:
            # Find where to insert sidebar (usually after breadcrumb, before article)
            article = soup.find('article', class_='lesson-content')
            if article and article.parent:
                new_sidebar_html = self.create_sidebar_html(module_num, filename, structure)
                new_sidebar = BeautifulSoup(new_sidebar_html, 'html.parser')
                article.insert_before(new_sidebar)
                return True
        else:
            # Replace existing sidebar
            new_sidebar_html = self.create_sidebar_html(module_num, filename, structure)
            new_sidebar = BeautifulSoup(new_sidebar_html, 'html.parser').find('aside')
            if new_sidebar:
                sidebar.replace_with(new_sidebar)
                return True
        
        return False

    def fix_footer_module_links(self, soup: BeautifulSoup, module_num: int) -> bool:
        """Update footer to highlight current module"""
        footer = soup.find('footer', class_='site-footer')
        if not footer:
            return False
        
        # Find all module links in footer
        module_links = footer.find_all('a', href=re.compile(r'/module\d+\.html'))
        
        for link in module_links:
            # Remove active class from all
            if 'class' in link.attrs:
                classes = link.get('class', [])
                if 'active' in classes:
                    classes.remove('active')
                    link['class'] = classes
            
            # Add active class to current module
            if f'/module{module_num}.html' in link.get('href', ''):
                if 'class' in link.attrs:
                    link['class'].append('active')
                else:
                    link['class'] = ['active']
        
        return True

    def process_html_file(self, file_path: Path, module_num: int, structure: Dict) -> bool:
        """Process a single HTML file with all fixes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get filename for sidebar active state
            filename = file_path.name
            
            # Apply all fixes
            changes_made = False
            
            # Fix CSS links
            if self.fix_css_links(soup):
                print(f"  ✓ Fixed CSS links in {filename}")
                changes_made = True
            
            # Fix JavaScript includes  
            if self.fix_javascript_includes(soup):
                print(f"  ✓ Fixed JavaScript includes in {filename}")
                changes_made = True
            
            # Fix sidebar structure
            if self.fix_sidebar(soup, module_num, filename, structure):
                print(f"  ✓ Fixed sidebar structure in {filename}")
                changes_made = True
            
            # Fix footer module links
            if self.fix_footer_module_links(soup, module_num):
                print(f"  ✓ Fixed footer links in {filename}")
                changes_made = True
            
            # Fix mermaid script if present
            mermaid_scripts = soup.find_all('script', string=re.compile(r'mermaid'))
            if mermaid_scripts:
                # Ensure mermaid universal fix is included
                has_universal_fix = soup.find('script', {'src': '/assets/js/mermaid-universal-fix.js'})
                if not has_universal_fix:
                    body = soup.find('body')
                    if body:
                        new_script = soup.new_tag('script', src='/assets/js/mermaid-universal-fix.js')
                        
                        # Add comment before script
                        comment1 = soup.new_string('<!-- Universal Mermaid Fix -->', Comment)
                        body.append(comment1)
                        body.append(new_script)
                        print(f"  ✓ Added mermaid universal fix in {filename}")
                        changes_made = True
            
            if changes_made:
                # Prettify and save
                pretty_html = soup.prettify()
                
                # Fix some BeautifulSoup prettify issues
                # Remove extra whitespace in text content
                pretty_html = re.sub(r'>\s+([^<>\s])', r'>\1', pretty_html)
                pretty_html = re.sub(r'([^<>\s])\s+<', r'\1<', pretty_html)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(pretty_html)
                
                return True
            else:
                print(f"  ℹ No changes needed for {filename}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
            return False

    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("Module 03 and 04 HTML Fixer")
        print("=" * 60)
        
        # Parse module overview files
        print("\n📖 Parsing module structure...")
        self.module3_structure = self.parse_module_overview(3)
        self.module4_structure = self.parse_module_overview(4)
        
        if not self.module3_structure:
            print("⚠️  Warning: Could not parse Module 3 structure")
        else:
            print(f"  ✓ Found {len(self.module3_structure)} sessions in Module 3")
        
        if not self.module4_structure:
            print("⚠️  Warning: Could not parse Module 4 structure")
        else:
            print(f"  ✓ Found {len(self.module4_structure)} sessions in Module 4")
        
        # Process Module 3 files
        print("\n🔧 Processing Module 03 files...")
        module3_dir = self.base_path / "03module"
        if module3_dir.exists():
            html_files = list(module3_dir.glob("*.html"))
            print(f"  Found {len(html_files)} HTML files")
            
            fixed_count = 0
            for file_path in html_files:
                if self.process_html_file(file_path, 3, self.module3_structure):
                    fixed_count += 1
            
            print(f"\n  Summary: Fixed {fixed_count}/{len(html_files)} files in Module 03")
        else:
            print(f"  ✗ Directory not found: {module3_dir}")
        
        # Process Module 4 files
        print("\n🔧 Processing Module 04 files...")
        module4_dir = self.base_path / "04module"
        if module4_dir.exists():
            html_files = list(module4_dir.glob("*.html"))
            print(f"  Found {len(html_files)} HTML files")
            
            fixed_count = 0
            for file_path in html_files:
                if self.process_html_file(file_path, 4, self.module4_structure):
                    fixed_count += 1
            
            print(f"\n  Summary: Fixed {fixed_count}/{len(html_files)} files in Module 04")
        else:
            print(f"  ✗ Directory not found: {module4_dir}")
        
        print("\n" + "=" * 60)
        print("✅ Processing complete!")
        print("\nNext steps:")
        print("1. Test the sidebar toggle functionality in a browser")
        print("2. Verify that all navigation links work correctly")
        print("3. Check that the CSS styling matches Modules 01 and 02")
        print("4. Test on different screen sizes for responsive behavior")

# Import Comment for HTML comments
from bs4 import Comment

def main():
    """Main entry point"""
    # Determine the base path
    # This script should work with WSL paths
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        # Try to auto-detect based on common WSL paths
        possible_paths = [
            r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress",
            r"\\wsl.localhost\Ubuntu\home\practicalace\projects\php_wordpress",
            "/home/practicalace/projects/php_wordpress",  # If running from within WSL
            "."  # Current directory as fallback
        ]
        
        base_path = None
        for path in possible_paths:
            if Path(path).exists():
                base_path = path
                break
        
        if not base_path:
            print("Error: Could not find project directory")
            print("Please provide the path as an argument:")
            print("  python fix_modules.py /path/to/php_wordpress")
            sys.exit(1)
    
    print(f"Using base path: {base_path}")
    
    # Create and run the fixer
    fixer = ModuleFixer(base_path)
    fixer.run()

if __name__ == "__main__":
    main()
