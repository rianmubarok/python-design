import os
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel\real-detected")

for f in BASE.glob("*.jpg"):
    old_name = f.stem
    # Strip date suffix
    name = old_name.replace("_12092026", "")
    
    # Skip if already has vector_nirmana
    if "vector_nirmana" in name:
        continue
    
    # Add vector_nirmana
    if name.startswith("parallel_"):
        new_name = name.replace("parallel_", "parallel_vector_nirmana_", 1)
    elif name.startswith("abstract_parallel_lines_"):
        new_name = name.replace("_pattern_", "_vector_nirmana_pattern_", 1)
        new_name = new_name.replace("_texture", "_vector_nirmana_texture", 1)
        new_name = new_name.replace("_design", "_vector_nirmana_design", 1)
    else:
        new_name = name + "_vector_nirmana"
    
    new_file = f.parent / (new_name + f.suffix)
    if not new_file.exists():
        f.rename(new_file)
        print(f"OK: {old_name} -> {new_name}")
    else:
        print(f"SKIP (exists): {new_name}")
