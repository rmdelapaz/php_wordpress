#!/usr/bin/env python3
"""
Simple script to test and find the correct path to your module directories.
"""

import os
import sys

print("=" * 60)
print("PATH DIAGNOSTIC TOOL")
print("=" * 60)

# Test various possible paths
test_paths = [
    r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress",
    r"\\wsl.localhost\Ubuntu\home\practicalace\projects\php_wordpress",
    r"\\wsl$\ubuntu\home\practicalace\projects\php_wordpress",  # lowercase ubuntu
    "/home/practicalace/projects/php_wordpress",
    "/mnt/c/Users/*/projects/php_wordpress",  # if mapped to Windows
    os.path.join(os.getcwd(), "01module"),  # relative to current dir
    os.getcwd(),  # current directory
]

print("\nTesting possible paths...")
print("-" * 60)

found_path = None

for path in test_paths:
    # Handle wildcards
    if '*' in path:
        print(f"\n✗ Skipping wildcard path: {path}")
        continue
        
    print(f"\nTesting: {path}")
    
    if os.path.exists(path):
        print(f"  ✓ Path exists!")
        
        # Check for 01module
        module01_path = os.path.join(path, "01module")
        if os.path.exists(module01_path):
            print(f"  ✓ Found 01module at: {module01_path}")
            
            # List files
            try:
                files = os.listdir(module01_path)
                html_files = [f for f in files if f.endswith('.html')]
                print(f"  ✓ Contains {len(html_files)} HTML files")
                if html_files:
                    print(f"  ✓ Sample files: {', '.join(html_files[:3])}")
                    found_path = path
                    break
            except Exception as e:
                print(f"  ✗ Error listing files: {e}")
        else:
            print(f"  ✗ No 01module directory found")
            
            # Try to list what's in this directory
            try:
                contents = os.listdir(path)
                dirs = [d for d in contents if os.path.isdir(os.path.join(path, d))]
                print(f"  → Directories found: {', '.join(dirs[:5])}")
            except Exception as e:
                print(f"  ✗ Cannot list directory contents: {e}")
    else:
        print(f"  ✗ Path does not exist")

print("\n" + "=" * 60)

if found_path:
    print(f"\n✅ SUCCESS! Found your project at: {found_path}")
    print(f"\nUse this path in the scripts:")
    print(f'  base_path = r"{found_path}"')
    
    # Create a fixed version
    print("\n" + "-" * 60)
    print("Creating fixed_paths.py with correct path...")
    
    with open("fixed_paths.py", "w") as f:
        f.write(f'''# Correct path for your system
BASE_PATH = r"{found_path}"
MODULE01_DIR = r"{os.path.join(found_path, '01module')}"
MODULE02_DIR = r"{os.path.join(found_path, '02module')}"
MODULE03_DIR = r"{os.path.join(found_path, '03module')}"

print(f"Using base path: {{BASE_PATH}}")
''')
    
    print("✓ Created fixed_paths.py with correct paths")
    print("\nYou can now import this in the other scripts:")
    print("  from fixed_paths import BASE_PATH")
else:
    print("\n❌ Could not find your project directory!")
    print("\nPlease check:")
    print("1. Are you running this from the right location?")
    print("2. Is WSL running?")
    print("3. Try running from within WSL: python3 test_paths.py")
    print("\nCurrent working directory:", os.getcwd())
    
    # Additional diagnostics
    print("\n" + "-" * 60)
    print("Additional diagnostics:")
    
    # Check if we're in WSL
    if os.path.exists("/proc/version"):
        with open("/proc/version", "r") as f:
            version = f.read()
            if "microsoft" in version.lower():
                print("✓ Running in WSL")
            else:
                print("✗ Not running in WSL")
    
    # Check current directory contents
    print(f"\nContents of current directory ({os.getcwd()}):")
    try:
        contents = os.listdir(".")
        for item in contents[:10]:
            print(f"  - {item}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 60)
