import os
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel\real-detected")
DATE = "12092026"

for f in list(BASE.glob("*.jpg")) + list(BASE.glob("*.svg")):
    name = f.stem
    # Skip if already has date
    if name.endswith(f"_{DATE}"):
        continue
    # Add date
    new_name = f"{name}_{DATE}{f.suffix}"
    new_file = f.parent / new_name
    if not new_file.exists():
        f.rename(new_file)
        print(f"OK: {f.name} -> {new_name}")

print("Done!")
