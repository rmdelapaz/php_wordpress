#!/usr/bin/env python3
"""
Advanced script to fix 01module HTML files by:
1. Checking if they have proper content (not just template placeholders)
2. Populating them with content from 01module_old if needed
3. Ensuring proper mermaid diagram support
4. Creating backups before modifying files
5. Providing detailed reporting and validation
"""

import os
import shutil
from datetime import datetime
import re
from pathlib import Path
import json
import hashlib

# Paths
BASE_DIR = Path(__file__).parent
MODULE_DIR = BASE_DIR / "01module"
OLD_MODULE_DIR = BASE_DIR / "01module_old"
BACKUP_DIR = BASE_DIR / "01module_backups"

# Create backup directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CURRENT_BACKUP_DIR = BACKUP_DIR / timestamp

# Report file
REPORT_FILE = BASE_DIR / f"fix_01module_report_{timestamp}.txt"

class ContentFixer:
    def __init__(self):
        self.report = []
        self.stats = {
            'total': 0,
            'processed': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'mermaid_fixed': 0
        }
        
    def log(self, message, level="INFO"):
        """Log message to console and report."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.report.append(log_entry)
    
    def create_backup(self, file_path):
        """Create a backup of the file before modification."""
        if not CURRENT_BACKUP_DIR.exists():
            CURRENT_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        backup_path = CURRENT_BACKUP_DIR / file_path.name
        shutil.copy2(file_path, backup_path)
        self.log(f"  ✓ Backup created: {backup_path.name}", "INFO")
        return backup_path
    
    def get_file_hash(self, content):
        """Get hash of file content for comparison."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def read_file(self, file_path):
        """Read and return file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.log(f"  ✗ Error reading {file_path}: {e}", "ERROR")
            return None
    
    def write_file(self, file_path, content):
        """Write content to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            self.log(f"  ✗ Error writing {file_path}: {e}", "ERROR")
            return False
    
    def analyze_content_quality(self, content):
        """Analyze the quality and completeness of content."""
        analysis = {
            'has_placeholders': False,
            'content_length': len(content),
            'code_blocks': 0,
            'headings': 0,
            'paragraphs': 0,
            'lists': 0,
            'images': 0,
            'links': 0,
            'mermaid_diagrams': 0,
            'quality_score': 0
        }
        
        # Count various elements
        analysis['code_blocks'] = len(re.findall(r'<pre><code[^>]*>', content))
        analysis['headings'] = len(re.findall(r'<h[2-6][^>]*>', content))
        analysis['paragraphs'] = len(re.findall(r'<p[^>]*>[^<]{50,}</p>', content))
        analysis['lists'] = len(re.findall(r'<[ou]l[^>]*>', content))
        analysis['images'] = len(re.findall(r'<img[^>]*>', content)) + len(re.findall(r'<svg[^>]*>', content))
        analysis['links'] = len(re.findall(r'<a[^>]*href=', content))
        analysis['mermaid_diagrams'] = len(re.findall(r'class="mermaid"', content))
        
        # Check for placeholder content
        placeholder_patterns = [
            r'This section contains the main lesson content',
            r'Practice makes perfect!',
            r'Follow industry standards',
            r'Write clean, maintainable code',
            r'// Example code\s*// Specific to lesson topic',
        ]
        
        placeholder_count = sum(1 for pattern in placeholder_patterns 
                               if re.search(pattern, content, re.IGNORECASE))
        
        analysis['has_placeholders'] = placeholder_count >= 2
        
        # Calculate quality score (0-100)
        score = 0
        if analysis['content_length'] > 5000: score += 20
        elif analysis['content_length'] > 2000: score += 10
        
        if analysis['code_blocks'] >= 2: score += 15
        if analysis['headings'] >= 3: score += 15
        if analysis['paragraphs'] >= 5: score += 20
        if analysis['lists'] >= 1: score += 10
        if analysis['images'] >= 1: score += 10
        if analysis['links'] >= 3: score += 10
        
        if analysis['has_placeholders']: score -= 30
        
        analysis['quality_score'] = max(0, min(100, score))
        
        return analysis
    
    def has_placeholder_content(self, content):
        """Enhanced check if the file only has placeholder/template content."""
        if not content:
            return True
        
        analysis = self.analyze_content_quality(content)
        
        # If quality score is low and has placeholders, it needs updating
        if analysis['quality_score'] < 40 and analysis['has_placeholders']:
            return True
        
        # Check specific content length in lesson-body
        main_content_match = re.search(
            r'<div class="lesson-body">(.*?)</div>\s*(?=<div class="lesson-navigation"|<!-- Lesson Navigation -->)', 
            content, re.DOTALL
        )
        
        if main_content_match:
            main_content = main_content_match.group(1)
            # Remove HTML tags for length check
            text_only = re.sub(r'<[^>]+>', '', main_content)
            text_only = re.sub(r'\s+', ' ', text_only).strip()
            
            # If main content is too short, it's likely a template
            if len(text_only) < 800:
                return True
        
        return False
    
    def extract_old_content(self, old_content):
        """Extract the main content from old module file."""
        # Try multiple extraction patterns
        patterns = [
            (r'<main[^>]*>(.*?)</main>', 'main'),
            (r'<section[^>]*class="[^"]*introduction[^"]*"[^>]*>(.*?)</section>\s*</main>', 'introduction'),
            (r'</header>\s*(.*?)\s*<footer', 'body'),
            (r'<article[^>]*>(.*?)</article>', 'article')
        ]
        
        for pattern, name in patterns:
            match = re.search(pattern, old_content, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if len(content) > 500:  # Ensure we got substantial content
                    self.log(f"    📝 Extracted content using {name} pattern", "DEBUG")
                    return content
        
        return None
    
    def ensure_mermaid_support(self, content):
        """Ensure proper mermaid diagram support in the HTML."""
        changes_made = False
        
        # Check if mermaid is already properly configured
        has_proper_mermaid = 'mermaid.initialize' in content and 'securityLevel' in content
        
        if not has_proper_mermaid:
            changes_made = True
            # Add or update mermaid initialization in head
            mermaid_script = """    <!-- Mermaid for diagrams -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            },
            securityLevel: 'loose'
        });
    </script>"""
            
            # Add before </head> if not present
            if 'import mermaid' not in content:
                content = content.replace('</head>', f'{mermaid_script}\n</head>')
            else:
                # Replace existing mermaid initialization
                content = re.sub(
                    r'<script type="module">.*?import mermaid.*?</script>',
                    mermaid_script,
                    content,
                    flags=re.DOTALL
                )
        
        # Update mermaid divs to pre tags for better rendering
        if '<div class="mermaid">' in content:
            changes_made = True
            content = re.sub(r'<div class="mermaid">', '<pre class="mermaid">', content)
            content = re.sub(r'</div>(\s*)<!--\s*end mermaid\s*-->', '</pre>', content)
            content = re.sub(r'</div>(\s*</div>\s*<!--\s*mermaid)', '</pre>\\1', content)
        
        # Ensure fallback script is present
        if 'mermaid.init()' not in content:
            changes_made = True
            fallback_script = """    <!-- Mermaid fallback -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.0.2/dist/mermaid.min.js"></script>
    <script>
        // Initialize mermaid if not already initialized
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default',
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true
                },
                securityLevel: 'loose'
            });
            // Manually render any mermaid diagrams
            mermaid.init();
        }
    </script>"""
            
            # Add before </body>
            content = content.replace('</body>', f'{fallback_script}\n</body>')
        
        if changes_made:
            self.stats['mermaid_fixed'] += 1
        
        return content
    
    def merge_content(self, current_content, old_content):
        """Merge old content into current template while preserving new structure."""
        # Extract main content from old file
        old_main_content = self.extract_old_content(old_content)
        
        if not old_main_content:
            self.log("    ⚠ Could not extract content from old file", "WARNING")
            return current_content
        
        # Find the lesson-body div in current content
        lesson_body_pattern = r'(<div class="lesson-body">)(.*?)(</div>\s*(?=<div class="lesson-navigation"|<!-- Lesson Navigation -->))'
        
        match = re.search(lesson_body_pattern, current_content, re.DOTALL)
        if match:
            # Replace the placeholder content with old content
            new_content = (
                current_content[:match.start(2)] + 
                '\n' + old_main_content + '\n                        ' + 
                current_content[match.end(2):]
            )
            return new_content
        else:
            self.log("    ⚠ Could not find lesson-body div in current file", "WARNING")
            return current_content
    
    def process_file(self, file_path):
        """Process a single HTML file."""
        self.log(f"\n📄 Processing: {file_path.name}", "INFO")
        
        # Check if corresponding old file exists
        old_file_path = OLD_MODULE_DIR / file_path.name
        if not old_file_path.exists():
            self.log(f"  ⚠ No corresponding file in 01module_old, skipping", "WARNING")
            self.stats['skipped'] += 1
            return False
        
        # Read current file
        current_content = read_file(file_path)
        if not current_content:
            self.stats['errors'] += 1
            return False
        
        # Analyze current content
        current_analysis = self.analyze_content_quality(current_content)
        self.log(f"  📊 Current quality score: {current_analysis['quality_score']}/100", "INFO")
        
        # Check if it has placeholder content
        needs_update = self.has_placeholder_content(current_content)
        
        if needs_update:
            self.log(f"  🔍 Detected placeholder content, needs updating", "INFO")
            
            # Read old file content
            old_content = self.read_file(old_file_path)
            if not old_content:
                self.stats['errors'] += 1
                return False
            
            # Create backup before modifying
            backup_path = self.create_backup(file_path)
            
            # Merge content
            self.log(f"  🔄 Merging content from old file", "INFO")
            merged_content = self.merge_content(current_content, old_content)
            
            # Ensure mermaid support
            self.log(f"  🎨 Ensuring mermaid diagram support", "INFO")
            final_content = self.ensure_mermaid_support(merged_content)
            
            # Analyze new content
            new_analysis = self.analyze_content_quality(final_content)
            self.log(f"  📊 New quality score: {new_analysis['quality_score']}/100", "INFO")
            
            # Write updated content
            if self.write_file(file_path, final_content):
                self.log(f"  ✅ Successfully updated {file_path.name}", "SUCCESS")
                self.stats['updated'] += 1
                self.stats['processed'] += 1
                return True
            else:
                self.log(f"  ❌ Failed to update {file_path.name}", "ERROR")
                # Restore from backup
                shutil.copy2(backup_path, file_path)
                self.log(f"  ↩ Restored from backup", "INFO")
                self.stats['errors'] += 1
                return False
        else:
            self.log(f"  ✓ File already has proper content", "INFO")
            
            # Still check and update mermaid support if needed
            updated_content = self.ensure_mermaid_support(current_content)
            if updated_content != current_content:
                self.log(f"  🎨 Updating mermaid diagram support", "INFO")
                self.create_backup(file_path)
                self.write_file(file_path, updated_content)
                self.log(f"  ✅ Updated mermaid support", "SUCCESS")
            
            self.stats['processed'] += 1
            return True
    
    def save_report(self):
        """Save the detailed report to a file."""
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write("01MODULE CONTENT FIX REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("STATISTICS:\n")
            f.write("-" * 40 + "\n")
            for key, value in self.stats.items():
                f.write(f"{key.capitalize()}: {value}\n")
            f.write("\n")
            
            f.write("DETAILED LOG:\n")
            f.write("-" * 40 + "\n")
            for entry in self.report:
                f.write(entry + "\n")
        
        self.log(f"\n📝 Report saved to: {REPORT_FILE}", "INFO")
    
    def run(self):
        """Main function to process all HTML files."""
        self.log("=" * 60, "INFO")
        self.log("🚀 Starting Advanced 01module Content Fix Script", "INFO")
        self.log("=" * 60, "INFO")
        
        # Check directories exist
        if not MODULE_DIR.exists():
            self.log(f"❌ Error: {MODULE_DIR} does not exist!", "ERROR")
            return
        
        if not OLD_MODULE_DIR.exists():
            self.log(f"❌ Error: {OLD_MODULE_DIR} does not exist!", "ERROR")
            return
        
        self.log(f"📁 Module directory: {MODULE_DIR}", "INFO")
        self.log(f"📁 Old module directory: {OLD_MODULE_DIR}", "INFO")
        self.log(f"📁 Backup directory: {CURRENT_BACKUP_DIR}", "INFO")
        
        # Get all HTML files in 01module
        html_files = sorted(MODULE_DIR.glob("*.html"))
        
        if not html_files:
            self.log("❌ No HTML files found in 01module directory!", "ERROR")
            return
        
        self.stats['total'] = len(html_files)
        self.log(f"\n📊 Found {len(html_files)} HTML files to process", "INFO")
        self.log("-" * 60, "INFO")
        
        # Process each file
        for file_path in html_files:
            try:
                self.process_file(file_path)
            except Exception as e:
                self.log(f"  ❌ Error processing {file_path.name}: {e}", "ERROR")
                self.stats['errors'] += 1
        
        # Summary
        self.log("\n" + "=" * 60, "INFO")
        self.log("📈 Summary:", "INFO")
        self.log(f"  Total files: {self.stats['total']}", "INFO")
        self.log(f"  ✅ Processed successfully: {self.stats['processed']}", "INFO")
        self.log(f"  🔄 Updated with content: {self.stats['updated']}", "INFO")
        self.log(f"  🎨 Mermaid support fixed: {self.stats['mermaid_fixed']}", "INFO")
        self.log(f"  ⚠ Skipped: {self.stats['skipped']}", "INFO")
        self.log(f"  ❌ Errors: {self.stats['errors']}", "INFO")
        
        if CURRENT_BACKUP_DIR.exists() and any(CURRENT_BACKUP_DIR.iterdir()):
            self.log(f"\n💾 Backups saved in: {CURRENT_BACKUP_DIR}", "INFO")
        
        # Save report
        self.save_report()
        
        self.log("\n✨ Script completed!", "SUCCESS")

def main():
    """Entry point for the script."""
    fixer = ContentFixer()
    fixer.run()

if __name__ == "__main__":
    main()
