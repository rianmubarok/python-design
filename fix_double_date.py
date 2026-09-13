import os
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel\real-detected")

for f in list(BASE.glob("*.jpg")) + list(BASE.glob("*.svg")):
    name = f.stem
    # Fix double date: _13092026_12092026 -> _12092026
    if "_13092026_12092026" in name:
        new_name = name.replace("_13092026_12092026", "_12092026")
        new_file = f.parent / (new_name + f.suffix)
        if not new_file.exists():
            f.rename(new_file)
            print(f"Fixed: {f.name} -> {new_name + f.suffix}")

print("Done!")
