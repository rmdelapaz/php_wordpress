#!/usr/bin/env python3
"""
Master script to run all fixing scripts in sequence.
This script orchestrates all the fixes for the PHP WordPress course files.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict

# Base path for WSL
BASE_PATH = r"\\wsl$\Ubuntu\home\practicalace\projects\php_wordpress"
SCRIPTS_PATH = os.path.join(BASE_PATH, "scripts")

# List of fix scripts to run in order
FIX_SCRIPTS = [
    "fix_session_names.py",
    "fix_quick_links.py", 
    "fix_mermaid_diagrams.py",
    "validate_structure.py"  # Validation script (we'll create this next)
]

def run_script(script_name: str) -> bool:
    """
    Run a single fix script and return success status.
    """
    script_path = os.path.join(SCRIPTS_PATH, script_name)
    
    if not os.path.exists(script_path):
        print(f"⚠️  Script not found: {script_name}")
        return False
    
    print(f"\n{'='*60}")
    print(f"🚀 Running: {script_name}")
    print(f"{'='*60}")
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=SCRIPTS_PATH
        )
        
        # Print output
        print(result.stdout)
        
        if result.stderr:
            print(f"⚠️  Warnings/Errors:\n{result.stderr}")
        
        if result.returncode != 0:
            print(f"❌ Script failed with return code: {result.returncode}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error running script: {str(e)}")
        return False

def create_backup():
    """
    Create a backup of all module directories before making changes.
    """
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(BASE_PATH, f"backup_{timestamp}")
    
    print(f"📦 Creating backup in: {backup_dir}")
    
    try:
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup each module
        for i in range(1, 7):
            module = f"{i:02d}module"
            src = os.path.join(BASE_PATH, module)
            dst = os.path.join(backup_dir, module)
            
            if os.path.exists(src):
                print(f"  Backing up {module}...")
                shutil.copytree(src, dst)
        
        print(f"✅ Backup created successfully!")
        return backup_dir
        
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")
        return None

def main():
    """
    Main orchestration function.
    """
    print("🎯 PHP WordPress Course File Fixer")
    print("=" * 60)
    print(f"Base path: {BASE_PATH}")
    print(f"Scripts path: {SCRIPTS_PATH}")
    print("=" * 60)
    
    # Ask user if they want to create a backup
    response = input("\n💾 Create backup before proceeding? (y/n): ").strip().lower()
    
    if response == 'y':
        backup_dir = create_backup()
        if not backup_dir:
            print("⚠️  Backup failed. Continue anyway? (y/n): ", end="")
            if input().strip().lower() != 'y':
                print("❌ Aborted.")
                return
    
    print("\n" + "=" * 60)
    print("🔧 Starting fixes...")
    print("=" * 60)
    
    # Run each fix script
    success_count = 0
    failed_scripts = []
    
    for script in FIX_SCRIPTS:
        if run_script(script):
            success_count += 1
        else:
            failed_scripts.append(script)
    
    # Print final summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"✅ Successful scripts: {success_count}/{len(FIX_SCRIPTS)}")
    
    if failed_scripts:
        print(f"❌ Failed scripts:")
        for script in failed_scripts:
            print(f"   - {script}")
    else:
        print("🎉 All scripts completed successfully!")
    
    print("=" * 60)
    print("✨ Fix process complete!")

if __name__ == "__main__":
    main()
