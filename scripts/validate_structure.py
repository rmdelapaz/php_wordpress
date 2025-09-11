#!/usr/bin/env python3
"""
Validate the structure and consistency of all module HTML files.
This script checks for common issues and reports any problems found.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# Base path for WSL
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"

class HTMLValidator:
    """Validator for HTML course files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.module = os.path.basename(os.path.dirname(file_path))
        self.issues = []
        self.warnings = []
        self.content = ""
        
    def load_file(self) -> bool:
        """Load the HTML file content."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.issues.append(f"Failed to load file: {str(e)}")
            return False
    
    def check_session_title(self) -> None:
        """Check if session title includes the session name."""
        pattern = r'<h4 class="sidebar-section-title">(Session \d+)([^<]*)</h4>'
        match = re.search(pattern, self.content)
        
        if match:
            session_num = match.group(1)
            session_desc = match.group(2).strip()
            
            if not session_desc or session_desc == "":
                self.issues.append(f"Session title missing description: '{session_num}'")
            elif not session_desc.startswith(":"):
                self.warnings.append(f"Session title format may be incorrect: '{session_num}{session_desc}'")
        else:
            # Check if it's a file that should have a session
            if "homework" not in self.file_name.lower() and "project" not in self.file_name.lower():
                self.warnings.append("No session title found in sidebar")
    
    def check_quick_links(self) -> None:
        """Check if Quick Links section exists and has required links."""
        pattern = r'<h4 class="sidebar-section-title">Quick Links</h4>'
        
        if pattern not in self.content:
            self.issues.append("Quick Links section not found")
            return
        
        # Check for required links
        required_links = [
            ("Module Overview", r'href="/module\d+\.html"'),
            ("Course Home", r'href="/"'),
            ("Resources", r'href="/resources\.html"')
        ]
        
        for link_text, link_pattern in required_links:
            if link_text not in self.content:
                self.warnings.append(f"Quick Links missing: '{link_text}'")
    
    def check_navigation_buttons(self) -> None:
        """Check if navigation buttons exist at the bottom."""
        if '<div class="lesson-navigation">' not in self.content:
            self.issues.append("Navigation buttons section not found")
            return
        
        # Check for complete button
        if 'class="complete-lesson-btn"' not in self.content:
            self.warnings.append("Complete lesson button not found")
        
        # Check for prev/next buttons (except for first/last lessons)
        if "introduction" not in self.file_name.lower() and "lesson-nav-button prev" not in self.content:
            self.warnings.append("Previous button not found")
        
        if "project" not in self.file_name.lower() and "lesson-nav-button next" not in self.content:
            self.warnings.append("Next button not found")
    
    def check_mermaid_diagrams(self) -> None:
        """Check for potential Mermaid diagram issues."""
        mermaid_pattern = r'<pre class="mermaid">'
        
        if mermaid_pattern in self.content:
            # Check if mermaid script is included
            if 'mermaid-universal-fix.js' not in self.content and 'mermaid.min.js' not in self.content:
                self.issues.append("Mermaid diagrams found but no Mermaid script included")
            
            # Check for problematic syntax
            if 'graph TD' in self.content or 'graph LR' in self.content:
                if '<' in self.content and '>' in self.content:
                    # Check for unescaped HTML in mermaid
                    mermaid_blocks = re.findall(r'<pre class="mermaid">(.*?)</pre>', self.content, re.DOTALL)
                    for block in mermaid_blocks:
                        if '<' in block and not '&lt;' in block:
                            self.warnings.append("Mermaid diagram may contain unescaped HTML characters")
    
    def check_breadcrumb(self) -> None:
        """Check if breadcrumb navigation exists and is correct."""
        if '<nav aria-label="Breadcrumb"' not in self.content:
            self.issues.append("Breadcrumb navigation not found")
            return
        
        # Check breadcrumb structure
        breadcrumb_pattern = r'<ol class="breadcrumb-list">(.*?)</ol>'
        match = re.search(breadcrumb_pattern, self.content, re.DOTALL)
        
        if match:
            breadcrumb_content = match.group(1)
            
            # Should have Home link
            if 'href="/"' not in breadcrumb_content:
                self.warnings.append("Breadcrumb missing Home link")
            
            # Should have module link
            module_num = self.module.replace("module", "")
            if f'href="/module{module_num}.html"' not in breadcrumb_content:
                self.warnings.append("Breadcrumb missing module link")
    
    def check_meta_tags(self) -> None:
        """Check if essential meta tags are present."""
        required_meta = [
            ('<title>', "Page title"),
            ('name="description"', "Meta description"),
            ('name="keywords"', "Meta keywords"),
            ('charset="utf-8"', "UTF-8 charset declaration")
        ]
        
        for tag, description in required_meta:
            if tag not in self.content:
                self.issues.append(f"Missing: {description}")
    
    def check_css_includes(self) -> None:
        """Check if required CSS files are included."""
        required_css = [
            'main.css',
            'sidebar-enhanced.css',
            'sidebar-toggle.css'
        ]
        
        for css_file in required_css:
            if css_file not in self.content:
                self.warnings.append(f"CSS file not included: {css_file}")
    
    def check_js_includes(self) -> None:
        """Check if required JavaScript files are included."""
        required_js = [
            'sidebar-toggle.js'
        ]
        
        for js_file in required_js:
            if js_file not in self.content:
                self.warnings.append(f"JavaScript file not included: {js_file}")
    
    def validate(self) -> Dict[str, any]:
        """Run all validation checks."""
        if not self.load_file():
            return {
                "file": self.file_name,
                "module": self.module,
                "issues": self.issues,
                "warnings": self.warnings,
                "valid": False
            }
        
        # Run all checks
        self.check_meta_tags()
        self.check_session_title()
        self.check_quick_links()
        self.check_navigation_buttons()
        self.check_breadcrumb()
        self.check_mermaid_diagrams()
        self.check_css_includes()
        self.check_js_includes()
        
        return {
            "file": self.file_name,
            "module": self.module,
            "issues": self.issues,
            "warnings": self.warnings,
            "valid": len(self.issues) == 0
        }

def validate_module(module: str) -> List[Dict]:
    """Validate all HTML files in a module."""
    module_path = os.path.join(BASE_PATH, module)
    results = []
    
    if not os.path.exists(module_path):
        print(f"❌ Module directory not found: {module_path}")
        return results
    
    # Get all HTML files
    html_files = [f for f in os.listdir(module_path) if f.endswith('.html')]
    
    for html_file in sorted(html_files):
        file_path = os.path.join(module_path, html_file)
        validator = HTMLValidator(file_path)
        result = validator.validate()
        results.append(result)
    
    return results

def print_validation_report(results: List[Dict]) -> None:
    """Print a formatted validation report."""
    total_files = len(results)
    valid_files = sum(1 for r in results if r["valid"])
    total_issues = sum(len(r["issues"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)
    
    print("\n" + "=" * 60)
    print("📋 VALIDATION REPORT")
    print("=" * 60)
    print(f"Total files checked: {total_files}")
    print(f"Valid files: {valid_files}/{total_files}")
    print(f"Total issues: {total_issues}")
    print(f"Total warnings: {total_warnings}")
    print("=" * 60)
    
    # Group results by module
    by_module = defaultdict(list)
    for result in results:
        by_module[result["module"]].append(result)
    
    # Print details for each module
    for module in sorted(by_module.keys()):
        module_results = by_module[module]
        module_issues = sum(len(r["issues"]) for r in module_results)
        module_warnings = sum(len(r["warnings"]) for r in module_results)
        
        if module_issues > 0 or module_warnings > 0:
            print(f"\n📁 {module}")
            print("-" * 40)
            
            for result in module_results:
                if result["issues"] or result["warnings"]:
                    print(f"\n  📄 {result['file']}")
                    
                    if result["issues"]:
                        print("    ❌ Issues:")
                        for issue in result["issues"]:
                            print(f"       - {issue}")
                    
                    if result["warnings"]:
                        print("    ⚠️  Warnings:")
                        for warning in result["warnings"]:
                            print(f"       - {warning}")

def main():
    """Main validation function."""
    print("🔍 HTML Structure Validator")
    print("=" * 60)
    print(f"Base path: {BASE_PATH}")
    print("=" * 60)
    
    all_results = []
    
    # Process modules 1-6
    modules = [f"{i:02d}module" for i in range(1, 7)]
    
    for module in modules:
        print(f"\nValidating {module}...")
        results = validate_module(module)
        all_results.extend(results)
    
    # Print validation report
    print_validation_report(all_results)
    
    # Determine exit status
    total_issues = sum(len(r["issues"]) for r in all_results)
    
    if total_issues == 0:
        print("\n✅ All files passed validation!")
        return 0
    else:
        print(f"\n❌ Validation found {total_issues} issue(s) that need attention.")
        return 1

if __name__ == "__main__":
    exit(main())
