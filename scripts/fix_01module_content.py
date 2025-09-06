#!/usr/bin/env python3
"""
Script to fix 01module HTML files by:
1. Checking if they have proper content (not just template placeholders)
2. Populating them with content from 01module_old if needed
3. Ensuring proper mermaid diagram support
4. Creating backups before modifying files
"""

import os
import shutil
from datetime import datetime
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
MODULE_DIR = BASE_DIR / "01module"
OLD_MODULE_DIR = BASE_DIR / "01module_old"
BACKUP_DIR = BASE_DIR / "01module_backups"

# Create backup directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CURRENT_BACKUP_DIR = BACKUP_DIR / timestamp

def create_backup(file_path):
    """Create a backup of the file before modification."""
    if not CURRENT_BACKUP_DIR.exists():
        CURRENT_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    backup_path = CURRENT_BACKUP_DIR / file_path.name
    shutil.copy2(file_path, backup_path)
    print(f"  ✓ Backup created: {backup_path.name}")
    return backup_path

def read_file(file_path):
    """Read and return file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return None

def write_file(file_path, content):
    """Write content to file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  ✗ Error writing {file_path}: {e}")
        return False

def has_placeholder_content(content):
    """Check if the file only has placeholder/template content."""
    if not content:
        return True
    
    # Indicators of placeholder content
    placeholder_patterns = [
        r'This section contains the main lesson content with examples and explanations',
        r'Practice makes perfect! Complete this exercise',
        r'Follow industry standards',
        r'Write clean, maintainable code',
        r'Test thoroughly',
        r'Document your work',
        r'// Example code\s*// Specific to lesson topic',
        r'<p>This section contains the main lesson content'
    ]
    
    # Check for actual lesson content indicators
    has_real_content_indicators = [
        r'<pre><code>[^<]{100,}',  # Code blocks with substantial content
        r'<h2>[^<]+</h2>\s*<p>[^<]{200,}',  # Sections with substantial paragraphs
        r'class="(definition|characteristics|code_example|feature)"',  # Specific content classes
    ]
    
    # Count placeholder matches
    placeholder_count = sum(1 for pattern in placeholder_patterns if re.search(pattern, content, re.IGNORECASE))
    
    # Count real content matches
    real_content_count = sum(1 for pattern in has_real_content_indicators if re.search(pattern, content, re.DOTALL))
    
    # If mostly placeholders and little real content, it's a template
    if placeholder_count >= 3 and real_content_count < 2:
        return True
    
    # Check if the main content area is too short (less than 1000 chars of actual content)
    main_content_match = re.search(r'<div class="lesson-body">(.*?)</div>\s*(?=<div class="lesson-navigation"|<!-- Lesson Navigation -->)', content, re.DOTALL)
    if main_content_match:
        main_content = main_content_match.group(1)
        # Remove HTML tags for length check
        text_only = re.sub(r'<[^>]+>', '', main_content)
        text_only = re.sub(r'\s+', ' ', text_only).strip()
        if len(text_only) < 1000:
            return True
    
    return False

def extract_old_content(old_content):
    """Extract the main content from old module file."""
    # Try to extract content between <main> tags
    main_match = re.search(r'<main[^>]*>(.*?)</main>', old_content, re.DOTALL)
    if main_match:
        return main_match.group(1).strip()
    
    # Fallback: try to get content after header and before footer
    body_match = re.search(r'</header>\s*(.*?)\s*<footer', old_content, re.DOTALL)
    if body_match:
        return body_match.group(1).strip()
    
    return None

def ensure_mermaid_support(content):
    """Ensure proper mermaid diagram support in the HTML."""
    # Check if mermaid is already properly configured
    has_proper_mermaid = 'mermaid.initialize' in content and 'securityLevel' in content
    
    if not has_proper_mermaid:
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
    content = re.sub(r'<div class="mermaid">', '<pre class="mermaid">', content)
    content = re.sub(r'</div>(\s*)<!--\s*end mermaid\s*-->', '</pre>', content)
    
    # Ensure fallback script is present
    if 'mermaid.init()' not in content:
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
    
    return content

def merge_content(current_content, old_content):
    """Merge old content into current template while preserving new structure."""
    # Extract main content from old file
    old_main_content = extract_old_content(old_content)
    
    if not old_main_content:
        print("    ⚠ Could not extract content from old file")
        return current_content
    
    # Find the lesson-body div in current content
    lesson_body_pattern = r'(<div class="lesson-body">)(.*?)(</div>\s*(?=<div class="lesson-navigation"|<!-- Lesson Navigation -->))'
    
    match = re.search(lesson_body_pattern, current_content, re.DOTALL)
    if match:
        # Replace the placeholder content with old content
        # Keep the div wrapper but replace its contents
        new_content = current_content[:match.start(2)] + '\n' + old_main_content + '\n                        ' + current_content[match.end(2):]
        return new_content
    else:
        print("    ⚠ Could not find lesson-body div in current file")
        return current_content

def process_file(file_path):
    """Process a single HTML file."""
    print(f"\n📄 Processing: {file_path.name}")
    
    # Check if corresponding old file exists
    old_file_path = OLD_MODULE_DIR / file_path.name
    if not old_file_path.exists():
        print(f"  ⚠ No corresponding file in 01module_old, skipping")
        return False
    
    # Read current file
    current_content = read_file(file_path)
    if not current_content:
        return False
    
    # Check if it has placeholder content
    if has_placeholder_content(current_content):
        print(f"  🔍 Detected placeholder content, needs updating")
        
        # Read old file content
        old_content = read_file(old_file_path)
        if not old_content:
            return False
        
        # Create backup before modifying
        backup_path = create_backup(file_path)
        
        # Merge content
        print(f"  🔄 Merging content from old file")
        merged_content = merge_content(current_content, old_content)
        
        # Ensure mermaid support
        print(f"  🎨 Ensuring mermaid diagram support")
        final_content = ensure_mermaid_support(merged_content)
        
        # Write updated content
        if write_file(file_path, final_content):
            print(f"  ✅ Successfully updated {file_path.name}")
            return True
        else:
            print(f"  ❌ Failed to update {file_path.name}")
            # Restore from backup
            shutil.copy2(backup_path, file_path)
            print(f"  ↩ Restored from backup")
            return False
    else:
        print(f"  ✓ File already has proper content")
        
        # Still check and update mermaid support if needed
        updated_content = ensure_mermaid_support(current_content)
        if updated_content != current_content:
            print(f"  🎨 Updating mermaid diagram support")
            create_backup(file_path)
            write_file(file_path, updated_content)
            print(f"  ✅ Updated mermaid support")
        
        return True

def main():
    """Main function to process all HTML files."""
    print("=" * 60)
    print("🚀 Starting 01module Content Fix Script")
    print("=" * 60)
    
    # Check directories exist
    if not MODULE_DIR.exists():
        print(f"❌ Error: {MODULE_DIR} does not exist!")
        return
    
    if not OLD_MODULE_DIR.exists():
        print(f"❌ Error: {OLD_MODULE_DIR} does not exist!")
        return
    
    print(f"📁 Module directory: {MODULE_DIR}")
    print(f"📁 Old module directory: {OLD_MODULE_DIR}")
    print(f"📁 Backup directory: {CURRENT_BACKUP_DIR}")
    
    # Get all HTML files in 01module
    html_files = sorted(MODULE_DIR.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in 01module directory!")
        return
    
    print(f"\n📊 Found {len(html_files)} HTML files to process")
    print("-" * 60)
    
    # Statistics
    processed = 0
    updated = 0
    skipped = 0
    errors = 0
    
    # Process each file
    for file_path in html_files:
        try:
            result = process_file(file_path)
            if result:
                processed += 1
                if has_placeholder_content(read_file(file_path)):
                    updated += 1
            else:
                errors += 1
        except Exception as e:
            print(f"  ❌ Error processing {file_path.name}: {e}")
            errors += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 Summary:")
    print(f"  Total files: {len(html_files)}")
    print(f"  ✅ Processed successfully: {processed}")
    print(f"  🔄 Updated with content: {updated}")
    print(f"  ⚠ Skipped: {skipped}")
    print(f"  ❌ Errors: {errors}")
    
    if CURRENT_BACKUP_DIR.exists() and any(CURRENT_BACKUP_DIR.iterdir()):
        print(f"\n💾 Backups saved in: {CURRENT_BACKUP_DIR}")
    
    print("\n✨ Script completed!")

if __name__ == "__main__":
    main()
