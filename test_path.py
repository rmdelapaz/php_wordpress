import os
from pathlib import Path

# Test path access
test_path = "\\\\wsl$\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\01module"
path_obj = Path(test_path)

print(f"Testing path: {test_path}")
print(f"Path exists: {path_obj.exists()}")

if path_obj.exists():
    print(f"Is directory: {path_obj.is_dir()}")
    files = list(path_obj.iterdir())[:5]
    print(f"First 5 files: {[f.name for f in files]}")
else:
    # Try alternative approach
    print("\nTrying alternative path...")
    alt_path = Path("\\\\wsl.localhost\\Ubuntu\\home\\practicalace\\projects\\php_wordpress\\01module")
    print(f"Alternative path exists: {alt_path.exists()}")
