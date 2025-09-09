#!/usr/bin/env python3
"""
Fix Module 03 and 04 sidebar navigation to show only current session links
Creates backups and works with Windows WSL paths
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys

class SessionSidebarFixer:
    def __init__(self, base_path: str):
        """Initialize with the project base path"""
        self.base_path = Path(base_path)
        self.module3_sessions = {}
        self.module4_sessions = {}
        
    def create_backups(self) -> bool:
        """Create timestamped backups of 03module and 04module folders"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Backup Module 03
            source_03 = self.base_path / "03module"
            if source_03.exists():
                backup_03 = self.base_path / f"03module_backup_{timestamp}"
                print(f"Creating backup: {backup_03}")
                shutil.copytree(source_03, backup_03)
                print(f"  ✓ Module 03 backed up to {backup_03.name}")
            else:
                print(f"  ⚠ Module 03 folder not found at {source_03}")
                
            # Backup Module 04
            source_04 = self.base_path / "04module"
            if source_04.exists():
                backup_04 = self.base_path / f"04module_backup_{timestamp}"
                print(f"Creating backup: {backup_04}")
                shutil.copytree(source_04, backup_04)
                print(f"  ✓ Module 04 backed up to {backup_04.name}")
            else:
                print(f"  ⚠ Module 04 folder not found at {source_04}")
                
            return True
            
        except Exception as e:
            print(f"  ✗ Error creating backups: {e}")
            return False
    
    def parse_module_sessions(self, module_num: int) -> Dict[str, Dict]:
        """Parse module HTML to extract session structure with file mappings"""
        module_file = self.base_path / f"module{module_num}.html"
        
        if not module_file.exists():
            print(f"  ⚠ {module_file} not found")
            return {}
        
        with open(module_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sessions = {}
        current_session = None
        
        # Find all session divs and their contents
        session_pattern = r'<div class="session">(.*?)</div>\s*(?=<div class="session">|</section>)'
        session_matches = re.findall(session_pattern, content, re.DOTALL)
        
        for session_content in session_matches:
            # Extract session title
            title_match = re.search(r'<h3>(.*?)</h3>', session_content)
            if title_match:
                session_title = title_match.group(1).strip()
                
                # Extract all lesson links in this session
                link_pattern = r'<a[^>]*href="(/0[34]module/[^"]+)"[^>]*class="lesson-link"[^>]*>(.*?)</a>'
                links = re.findall(link_pattern, session_content)
                
                session_files = []
                for href, text in links:
                    filename = href.split('/')[-1]
                    session_files.append({
                        'href': href,
                        'filename': filename,
                        'text': text.strip()
                    })
                
                if session_files:
                    sessions[session_title] = {
                        'title': session_title,
                        'files': session_files
                    }
        
        return sessions
    
    def find_file_session(self, filename: str, sessions: Dict) -> Optional[Tuple[str, Dict]]:
        """Find which session a file belongs to"""
        for session_title, session_data in sessions.items():
            for file_info in session_data['files']:
                if file_info['filename'] == filename:
                    return (session_title, session_data)
        return None
    
    def get_session_navigation(self, sessions: Dict, current_session_title: str) -> Dict:
        """Get previous and next session information"""
        session_list = list(sessions.keys())
        
        if current_session_title not in session_list:
            return {'prev': None, 'next': None}
        
        current_index = session_list.index(current_session_title)
        
        nav = {
            'prev': None,
            'next': None
        }
        
        # Get previous session
        if current_index > 0:
            prev_title = session_list[current_index - 1]
            prev_files = sessions[prev_title]['files']
            if prev_files:
                # Get first file of previous session
                nav['prev'] = {
                    'title': prev_title,
                    'href': prev_files[0]['href']
                }
        
        # Get next session
        if current_index < len(session_list) - 1:
            next_title = session_list[current_index + 1]
            next_files = sessions[next_title]['files']
            if next_files:
                # Get first file of next session
                nav['next'] = {
                    'title': next_title,
                    'href': next_files[0]['href']
                }
        
        return nav
    
    def create_session_sidebar(self, module_num: int, filename: str, session_data: Dict, 
                               session_nav: Dict) -> str:
        """Create sidebar HTML showing only current session links"""
        module_names = {
            3: "MySQL Database",
            4: "WordPress & Docker"
        }
        
        module_name = module_names.get(module_num, f"Module {module_num}")
        session_title = session_data['title']
        
        # Start sidebar HTML
        sidebar_html = f'''<aside class="sidebar">
    <div class="sidebar-nav">
        <h3 class="sidebar-title">Module {module_num}: {module_name}</h3>
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">{session_title}</h4>
            <ul class="sidebar-menu">'''
        
        # Add current session links
        for file_info in session_data['files']:
            is_active = file_info['filename'] == filename
            active_li = ' class="active"' if is_active else ''
            active_link = ' class="sidebar-link active"' if is_active else ' class="sidebar-link"'
            
            sidebar_html += f'''
                <li{active_li}><a{active_link} href="{file_info['href']}">{file_info['text']}</a></li>'''
        
        sidebar_html += '''
            </ul>
        </div>'''
        
        # Add Quick Links section
        prev_module = module_num - 1 if module_num > 1 else 1
        next_module = module_num + 1 if module_num < 9 else 9
        
        sidebar_html += f'''
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Quick Links</h4>
            <ul class="sidebar-menu">
                <li><a class="sidebar-link" href="/module{module_num}.html">Module Overview</a></li>'''
        
        # Add session navigation if available
        if session_nav['prev']:
            prev_title = session_nav['prev']['title']
            # Shorten the title for display
            prev_display = prev_title.replace(f'Session {prev_title.split(":")[0].split()[-1]}:', '').strip()
            if len(prev_display) > 20:
                prev_display = f"Session {prev_title.split(':')[0].split()[-1]}"
            sidebar_html += f'''
                <li><a class="sidebar-link prev-session" href="{session_nav['prev']['href']}">← Prev: {prev_display}</a></li>'''
        
        if session_nav['next']:
            next_title = session_nav['next']['title']
            # Shorten the title for display
            next_display = next_title.replace(f'Session {next_title.split(":")[0].split()[-1]}:', '').strip()
            if len(next_display) > 20:
                next_display = f"Session {next_title.split(':')[0].split()[-1]}"
            sidebar_html += f'''
                <li><a class="sidebar-link next-session" href="{session_nav['next']['href']}">Next: {next_display} →</a></li>'''
        
        # Add module navigation
        sidebar_html += f'''
                <li><a class="sidebar-link" href="/">← Course Home</a></li>
                <li><a class="sidebar-link" href="/module{next_module}.html">Next Module →</a></li>
                <li><a class="sidebar-link" href="/resources.html">Resources</a></li>
            </ul>
        </div>
    </div>
</aside>'''
        
        return sidebar_html
    
    def process_html_file(self, file_path: Path, module_num: int, sessions: Dict) -> bool:
        """Process a single HTML file to update its sidebar"""
        filename = file_path.name
        
        # Find which session this file belongs to
        session_info = self.find_file_session(filename, sessions)
        
        if not session_info:
            print(f"  ⚠ {filename} not found in any session, skipping")
            return False
        
        session_title, session_data = session_info
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get session navigation
            session_nav = self.get_session_navigation(sessions, session_title)
            
            # Create new sidebar HTML
            new_sidebar = self.create_session_sidebar(module_num, filename, session_data, session_nav)
            
            # Replace existing sidebar
            # Pattern to match the entire aside.sidebar element
            sidebar_pattern = r'<aside\s+class="sidebar">.*?</aside>'
            
            # Check if sidebar exists
            if re.search(sidebar_pattern, content, re.DOTALL):
                # Replace existing sidebar
                new_content = re.sub(sidebar_pattern, new_sidebar, content, flags=re.DOTALL)
            else:
                # Try to insert sidebar before article.lesson-content
                article_pattern = r'(<article\s+class="lesson-content">)'
                new_content = re.sub(article_pattern, new_sidebar + '\n                    \\1', content)
            
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✓ Updated {filename} ({session_title})")
                return True
            else:
                print(f"  ℹ No changes needed for {filename}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {e}")
            return False
    
    def run(self):
        """Main execution method"""
        print("=" * 70)
        print("Module 03 and 04 Sidebar Session Fixer")
        print("=" * 70)
        
        # Step 1: Create backups
        print("\n📦 Creating backups...")
        if not self.create_backups():
            print("Failed to create backups. Aborting.")
            return
        
        # Step 2: Parse module structures
        print("\n📖 Parsing module structures...")
        self.module3_sessions = self.parse_module_sessions(3)
        self.module4_sessions = self.parse_module_sessions(4)
        
        if self.module3_sessions:
            print(f"  ✓ Found {len(self.module3_sessions)} sessions in Module 3:")
            for session_title in self.module3_sessions:
                file_count = len(self.module3_sessions[session_title]['files'])
                print(f"    • {session_title}: {file_count} files")
        else:
            print("  ⚠ No sessions found in Module 3")
        
        if self.module4_sessions:
            print(f"  ✓ Found {len(self.module4_sessions)} sessions in Module 4:")
            for session_title in self.module4_sessions:
                file_count = len(self.module4_sessions[session_title]['files'])
                print(f"    • {session_title}: {file_count} files")
        else:
            print("  ⚠ No sessions found in Module 4")
        
        # Step 3: Process Module 03 files
        if self.module3_sessions:
            print("\n🔧 Processing Module 03 files...")
            module3_dir = self.base_path / "03module"
            if module3_dir.exists():
                html_files = list(module3_dir.glob("*.html"))
                print(f"  Found {len(html_files)} HTML files to process")
                
                updated_count = 0
                for file_path in html_files:
                    if self.process_html_file(file_path, 3, self.module3_sessions):
                        updated_count += 1
                
                print(f"\n  Summary: Updated {updated_count}/{len(html_files)} files in Module 03")
        
        # Step 4: Process Module 04 files
        if self.module4_sessions:
            print("\n🔧 Processing Module 04 files...")
            module4_dir = self.base_path / "04module"
            if module4_dir.exists():
                html_files = list(module4_dir.glob("*.html"))
                print(f"  Found {len(html_files)} HTML files to process")
                
                updated_count = 0
                for file_path in html_files:
                    if self.process_html_file(file_path, 4, self.module4_sessions):
                        updated_count += 1
                
                print(f"\n  Summary: Updated {updated_count}/{len(html_files)} files in Module 04")
        
        print("\n" + "=" * 70)
        print("✅ Processing complete!")
        print("\nWhat was done:")
        print("1. Created timestamped backups of both modules")
        print("2. Updated sidebars to show only current session links")
        print("3. Added session navigation in Quick Links")
        print("4. Maintained active page highlighting")
        print("\nNext steps:")
        print("1. Test the navigation in a browser")
        print("2. Verify session groupings are correct")
        print("3. Check that Quick Links navigation works")
        print("4. If issues occur, restore from the backup folders")

def main():
    """Main entry point"""
    # Determine base path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        # Try to auto-detect common WSL paths
        possible_paths = [
            r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress",
            r"\\wsl.localhost\Ubuntu\home\practicalace\projects\php_wordpress",
            "/home/practicalace/projects/php_wordpress",
            "."  # Current directory
        ]
        
        base_path = None
        for path in possible_paths:
            test_path = Path(path)
            if test_path.exists() and (test_path / "03module").exists():
                base_path = path
                break
        
        if not base_path:
            print("Error: Could not find project directory")
            print("Usage: python fix_sidebar_sessions.py /path/to/php_wordpress")
            sys.exit(1)
    
    print(f"Using base path: {base_path}")
    
    # Run the fixer
    fixer = SessionSidebarFixer(base_path)
    fixer.run()

if __name__ == "__main__":
    main()
