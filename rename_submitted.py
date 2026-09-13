import os
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel\submitted")

for f in BASE.glob("*.jpg"):
    old_name = f.stem
    name = old_name.replace("_12092026", "")
    
    if "vector_nirmana" in name:
        continue
    
    if name.startswith("parallel_"):
        new_name = name.replace("parallel_", "parallel_vector_nirmana_", 1)
    elif name.startswith("abstract_parallel_lines_"):
        new_name = name.replace("_pattern_", "_vector_nirmana_pattern_", 1)
        new_name = new_name.replace("_texture", "_vector_nirmana_texture", 1)
    else:
        new_name = name + "_vector_nirmana"
    
    new_file = f.parent / (new_name + f.suffix)
    if not new_file.exists():
        f.rename(new_file)
        print(f"OK: {old_name} -> {new_name}")

for f in BASE.glob("*.svg"):
    old_name = f.stem
    name = old_name.replace("_12092026", "")
    
    if "vector_nirmana" in name:
        continue
    
    if name.startswith("parallel_"):
        new_name = name.replace("parallel_", "parallel_vector_nirmana_", 1)
    elif name.startswith("abstract_parallel_lines_"):
        new_name = name.replace("_pattern_", "_vector_nirmana_pattern_", 1)
        new_name = new_name.replace("_texture", "_vector_nirmana_texture", 1)
    else:
        new_name = name + "_vector_nirmana"
    
    new_file = f.parent / (new_name + f.suffix)
    if not new_file.exists():
        f.rename(new_file)
        print(f"OK: {old_name} -> {new_name}")
