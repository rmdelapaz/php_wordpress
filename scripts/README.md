# PHP WordPress Course - File Fix Scripts

This directory contains Python scripts to fix and validate HTML files in the PHP WordPress course.

## Scripts Overview

### 1. `fix_session_names.py`
Adds descriptive session names to sidebar section titles.
- Updates `<h4 class="sidebar-section-title">Session X</h4>` to include the session name
- Example: "Session 3" becomes "Session 3: CSS Basics"

### 2. `fix_quick_links.py`
Standardizes the Quick Links section in the sidebar across all modules.
- Ensures consistent navigation links
- Adds module overview, course home, next module, and resources links

### 3. `fix_mermaid_diagrams.py`
Fixes Mermaid diagram display issues.
- Converts problematic Mermaid diagrams to SVG
- Adds proper styling for Mermaid containers
- Handles HTML escaping issues in diagrams

### 4. `validate_structure.py`
Validates HTML structure and reports issues.
- Checks for required meta tags
- Validates sidebar structure
- Ensures navigation elements are present
- Reports issues and warnings

### 5. `run_all_fixes.py`
Master script that runs all fixes in sequence.
- Creates optional backup before making changes
- Runs all fix scripts in order
- Provides summary of results

## Usage

### Run Individual Scripts

```bash
# Fix session names only
python fix_session_names.py

# Fix quick links only
python fix_quick_links.py

# Fix mermaid diagrams only
python fix_mermaid_diagrams.py

# Validate structure only
python validate_structure.py
```

### Run All Fixes

```bash
# Run all fixes with optional backup
python run_all_fixes.py
```

## Configuration

All scripts use the WSL path:
```python
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
```

To modify for your environment, update the `BASE_PATH` variable in each script.

## Customization

### Adding New Session Names

Edit `SESSION_NAMES` dictionary in `fix_session_names.py`:

```python
SESSION_NAMES = {
    "01module": {
        "Session 1": "Session 1: Introduction",
        "Session 2": "Session 2: HTML Fundamentals",
        # Add more sessions...
    },
    # Add more modules...
}
```

### Adding Mermaid Conversions

Edit `MERMAID_CONVERSIONS` dictionary in `fix_mermaid_diagrams.py`:

```python
MERMAID_CONVERSIONS = {
    "file_name_key": """<svg>...</svg>""",
    # Add more conversions...
}
```

## Safety Features

- **Backup Option**: `run_all_fixes.py` offers to create a timestamped backup
- **Validation**: `validate_structure.py` checks files without modifying them
- **Skip Logic**: Scripts skip files that are already correct
- **Error Handling**: Scripts continue processing even if individual files fail

## Output

Scripts provide detailed output:
- ✅ Fixed: File was successfully modified
- ⏭️ Skipped: File already correct or doesn't need changes
- ⚠️ Warning: Non-critical issue found
- ❌ Error: Critical issue or processing failure

## Requirements

- Python 3.6+
- Access to WSL filesystem from Windows
- Read/write permissions for course files

## Troubleshooting

### Permission Errors
Ensure you have write access to the course directory.

### Path Issues
Verify the WSL path is correct for your system:
```bash
# In Windows Explorer, navigate to:
\\wsl$\Ubuntu\home\[your-username]\projects\php_wordpress
```

### Encoding Issues
Scripts use UTF-8 encoding. If you encounter encoding errors, ensure your files are UTF-8 encoded.

## Future Enhancements

Potential improvements to add:
- [ ] Automatic link ordering based on file sequence
- [ ] Smart session detection from file content
- [ ] Automated testing after fixes
- [ ] Rollback functionality
- [ ] Detailed diff output
- [ ] Parallel processing for faster execution
- [ ] Configuration file support
- [ ] Interactive mode for selective fixes
