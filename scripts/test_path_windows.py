#!/usr/bin/env python3
"""
Test script to verify paths are working correctly on Windows
"""

import os
from pathlib import Path

def test_paths():
    """Test different path formats to find the correct one"""
    
    print("Testing Path Access for PHP WordPress Project")
    print("=" * 60)
    
    # List of paths to test
    test_paths = [
        r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress',
        r'\\wsl.localhost\Ubuntu\home\practicalace\projects\php_wordpress',
        Path(r'\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress'),
        Path('//wsl$/Ubuntu/home/practicalace/projects/php_wordpress'),
        Path('//wsl.localhost/Ubuntu/home/practicalace/projects/php_wordpress'),
    ]
    
    working_path = None
    
    for i, test_path in enumerate(test_paths, 1):
        print(f"\nTest {i}: {test_path}")
        try:
            path = Path(test_path)
            exists = path.exists()
            print(f"  Exists: {exists}")
            
            if exists:
                # Check for subdirectories
                module_02 = path / '02module'
                module_02_old = path / '02module_old'
                
                print(f"  02module exists: {module_02.exists()}")
                print(f"  02module_old exists: {module_02_old.exists()}")
                
                if module_02.exists() and module_02_old.exists():
                    # Count files
                    files_02 = list(module_02.glob('*.html'))
                    files_02_old = list(module_02_old.glob('*.html'))
                    
                    print(f"  Files in 02module: {len(files_02)}")
                    print(f"  Files in 02module_old: {len(files_02_old)}")
                    
                    if len(files_02) > 0 and len(files_02_old) > 0:
                        working_path = path
                        print(f"  ✅ THIS PATH WORKS!")
                        
                        # Show first few files as confirmation
                        print(f"\n  Sample files in 02module:")
                        for f in files_02[:3]:
                            print(f"    - {f.name}")
                        print(f"\n  Sample files in 02module_old:")
                        for f in files_02_old[:3]:
                            print(f"    - {f.name}")
                        break
                        
        except Exception as e:
            print(f"  Error: {e}")
    
    if working_path:
        print(f"\n" + "=" * 60)
        print(f"SUCCESS! Working path found:")
        print(f"  {working_path}")
        print(f"\nYou can use this path in the populate script.")
        return working_path
    else:
        print(f"\n" + "=" * 60)
        print("ERROR: Could not find a working path.")
        print("\nPlease try manually entering the path:")
        manual_path = input("Enter full path to php_wordpress: ").strip().strip('"').strip("'")
        
        if manual_path:
            path = Path(manual_path)
            if path.exists():
                print(f"✅ Path exists: {path}")
                return path
            else:
                print(f"❌ Path does not exist: {path}")
                return None

if __name__ == "__main__":
    test_paths()
    input("\nPress Enter to exit...")
