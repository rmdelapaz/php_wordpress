# Navigation Fix Scripts for PHP WordPress Course

## Overview
These Python scripts are designed to analyze and fix navigation inconsistencies in the Module 1 HTML files to match the consistent structure used in Modules 2 and 3.

## Scripts Included

### 1. `analyze_navigation.py`
Analyzes the current navigation structure across all modules to identify inconsistencies.

**Features:**
- Compares navigation structures across Modules 1, 2, and 3
- Identifies missing or incorrect navigation elements
- Reports files without proper sidebar structure
- Shows which files have active navigation states
- Provides a recommended navigation structure

### 2. `fix_01module_navigation.py`
Automatically fixes the navigation in all Module 1 HTML files.

**Features:**
- Updates all Module 1 HTML files with consistent navigation
- Sets the correct active state for each page
- Preserves the existing content while fixing navigation
- Provides before/after analysis
- Creates proper sidebar structure with:
  - Module title
  - Lessons section with numbered links
  - Module Resources section
  - Active state management

## Installation

1. Install Python 3.7 or higher if not already installed
2. Install required dependencies:
```bash
pip install -r requirements_nav_fix.txt
```

## Usage

### Step 1: Analyze Current State
First, run the analysis script to see the current state of navigation:

```bash
python analyze_navigation.py
```

This will show you:
- Current navigation structure in each module
- Inconsistencies and issues
- Files missing proper navigation
- Recommended structure

### Step 2: Fix Module 1 Navigation
After reviewing the analysis, run the fix script:

```bash
python fix_01module_navigation.py
```

The script will:
1. Show current navigation state
2. Ask for confirmation before making changes
3. Update all Module 1 HTML files
4. Verify the changes were applied correctly

## Navigation Structure

The fixed navigation will have this structure for Module 1:

```html
<aside class="sidebar">
    <div class="sidebar-nav">
        <h3 class="sidebar-title">Module 1: Web Fundamentals</h3>
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Lessons</h4>
            <ul class="sidebar-menu">
                <li><a href="/01module/course_introduction.html" class="sidebar-link">1.1 Course Introduction</a></li>
                <li><a href="/01module/first_html_page.html" class="sidebar-link">1.2 Your First HTML Page</a></li>
                <li><a href="/01module/introduction_to_css.html" class="sidebar-link">1.3 Introduction to CSS</a></li>
                <li><a href="/01module/js_intro.html" class="sidebar-link">1.4 JavaScript Introduction</a></li>
                <li><a href="/01module/php_and_wordpress.html" class="sidebar-link">1.5 PHP and WordPress Overview</a></li>
                <li><a href="/01module/php_header_footer.html" class="sidebar-link">1.6 PHP Headers and Footers</a></li>
                <li><a href="/01module/project_static_site.html" class="sidebar-link">1.7 Project: Static Website</a></li>
            </ul>
        </div>
        <div class="sidebar-section">
            <h4 class="sidebar-section-title">Module Resources</h4>
            <ul class="sidebar-menu">
                <li><a href="/module1.html" class="sidebar-link">Module Overview</a></li>
                <li><a href="/resources.html" class="sidebar-link">Additional Resources</a></li>
            </ul>
        </div>
    </div>
</aside>
```

The script automatically adds the `active` class to the current page's link.

## What Gets Fixed

1. **Missing sidebar-nav structure** - Adds proper div with class="sidebar-nav"
2. **Missing section headers** - Adds h3 for module title and h4 for section titles
3. **Inconsistent links** - Updates all navigation links to be consistent
4. **Missing active states** - Sets the active class on the current page
5. **Improper nesting** - Fixes HTML structure to match modules 2 and 3
6. **Missing sidebar-menu class** - Adds ul with proper class

## Safety Features

- **Backup recommended**: Always backup your files before running the fix script
- **Confirmation required**: Script asks for confirmation before making changes
- **Non-destructive**: Only modifies navigation, preserves all other content
- **Verification**: Shows before/after analysis to confirm changes

## Troubleshooting

If you encounter issues:

1. **Module not found**: Check that the path in the script matches your WSL setup
2. **Permission denied**: Run with appropriate permissions or as administrator
3. **BeautifulSoup not installed**: Run `pip install beautifulsoup4`
4. **Encoding issues**: Script uses UTF-8 encoding by default

## Manual Verification

After running the fix script, manually verify:
1. Open each HTML file in a browser
2. Check that navigation appears correctly
3. Verify the current page is highlighted (active state)
4. Test all navigation links work properly

## Support

If you need to customize the navigation structure, edit the `create_01module_navigation()` function in `fix_01module_navigation.py`.
