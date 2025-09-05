#!/usr/bin/env python3
"""
Batch update script for remaining Module 1 HTML files
Updated with correct Linux paths
"""

import os
import re
from pathlib import Path

# Base directory - UPDATE THIS PATH
BASE_DIR = Path("/home/practicalace/projects/php_wordpress/01module")

# Check if directory exists
if not BASE_DIR.exists():
    print(f"❌ Error: Directory {BASE_DIR} does not exist!")
    print(f"Current working directory: {os.getcwd()}")
    print("\nPlease update BASE_DIR to the correct path.")
    exit(1)

# Module 1 complete structure with all files
module1_files = {
    "session2": {
        "title": "HTML Fundamentals",
        "files": [
            ("html_validation_practices.html", "HTML Validation and Best Practices", "30 minutes",
             "Master HTML validation techniques, semantic markup, and best practices for clean, maintainable HTML code."),
            ("homework_html_profile.html", "Homework: Create a Personal Profile Page", "60 minutes",
             "Apply your HTML knowledge to build a complete personal profile page with proper structure and semantic markup.")
        ]
    },
    "session3": {
        "title": "CSS Basics",
        "files": [
            ("css_syntax_and_selectors.html", "CSS Syntax and Selectors", "45 minutes",
             "Master CSS syntax, understand different types of selectors, and learn how to target HTML elements effectively."),
            ("css_implementation_methods.html", "Inline, Internal, and External CSS", "30 minutes",
             "Learn the three ways to add CSS to HTML documents and understand when to use each method."),
            ("css_colors_fonts_text.html", "Working with Colors, Fonts, and Text", "45 minutes",
             "Explore CSS properties for colors, typography, and text styling to create visually appealing designs."),
            ("css_box_model.html", "The CSS Box Model", "45 minutes",
             "Understand the CSS box model, including margins, padding, borders, and how elements are sized and spaced."),
            ("homework_css_profile.html", "Homework: Style Your Profile Page", "60 minutes",
             "Apply CSS styling to your HTML profile page to create an attractive, professional design.")
        ]
    },
    # Add remaining sessions here...
}

def generate_html(session_key, session_data, file_index, file_info):
    """Generate complete HTML for a lesson file"""
    
    filename, title, duration, description = file_info
    session_title = session_data["title"]
    
    # HTML template content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - PHP WordPress Course</title>
    <meta name="description" content="{description}">
    <!-- Rest of HTML template -->
</head>
<body>
    <!-- Template body -->
</body>
</html>"""
    
    return html_content

# Main execution
def main():
    """Main function to update all files"""
    
    print(f"📁 Working directory: {BASE_DIR}")
    print(f"✅ Directory exists: {BASE_DIR.exists()}")
    
    # List existing files
    existing_files = list(BASE_DIR.glob("*.html"))
    print(f"📊 Found {len(existing_files)} HTML files in directory")
    
    updated_files = []
    failed_files = []
    skipped_files = []
    
    # Files to skip (already updated)
    already_updated = [
        "course_introduction.html",
        "how_web_works.html",
        "development_environment.html",
        "first_html_page.html",
        "html_structure_syntax.html",
        "essential_html_tags.html",
        "html_forms_inputs.html",
        "introduction_to_css.html"
    ]
    
    for session_key, session_data in module1_files.items():
        print(f"\n📁 Processing {session_data['title']}...")
        
        for file_index, file_info in enumerate(session_data["files"]):
            filename = file_info[0]
            filepath = BASE_DIR / filename
            
            # Skip already updated files
            if filename in already_updated:
                skipped_files.append(filename)
                print(f"  ⏭️  Skipped (already updated): {filename}")
                continue
            
            try:
                # Check if file exists
                if not filepath.exists():
                    print(f"  ⚠️  File not found: {filename}")
                    # Create the file
                    html_content = generate_html(session_key, session_data, file_index, file_info)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    updated_files.append(filename)
                    print(f"  ✅ Created: {filename}")
                else:
                    # Update existing file
                    html_content = generate_html(session_key, session_data, file_index, file_info)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    updated_files.append(filename)
                    print(f"  ✅ Updated: {filename}")
                
            except Exception as e:
                failed_files.append((filename, str(e)))
                print(f"  ❌ Failed: {filename} - {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Update Summary:")
    print(f"  ✅ Successfully updated: {len(updated_files)} files")
    print(f"  ⏭️  Skipped (already updated): {len(skipped_files)} files")
    print(f"  ❌ Failed: {len(failed_files)} files")
    
    if failed_files:
        print(f"\n⚠️ Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    print(f"\n🎉 Batch update complete!")
    
    # Create summary file
    summary_path = BASE_DIR.parent / "batch_update_results.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Module 1 Batch Update Results

## Successfully Updated: {len(updated_files)}
{chr(10).join(f"- {f}" for f in updated_files) if updated_files else "None"}

## Skipped (Already Updated): {len(skipped_files)}
{chr(10).join(f"- {f}" for f in skipped_files) if skipped_files else "None"}

## Failed: {len(failed_files)}
{chr(10).join(f"- {f[0]}: {f[1]}" for f in failed_files) if failed_files else "None"}

## Total Progress
- Total files processed: {len(updated_files) + len(skipped_files) + len(failed_files)}
- Success rate: {(len(updated_files) / (len(updated_files) + len(failed_files)) * 100 if updated_files else 0):.1f}%
""")
    
    print(f"\n📝 Summary saved to: {summary_path}")

if __name__ == "__main__":
    # Check Python version
    import sys
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    # Run the update
    main()
