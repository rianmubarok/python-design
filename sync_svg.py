import os
import shutil
from pathlib import Path

BASE = Path(r"D:\PEMROGRAMAN\PROJECT\2026\python-design\parallel")
REAL_DIR = BASE / "real-detected"
SVG_DIR = BASE / "output" / "svg"
DATE = "12092026"

# Get all JPG names in real-detected
jpg_files = list(REAL_DIR.glob("*.jpg"))
jpg_names = [f.stem for f in jpg_files]

# Get all SVG names in output/svg
svg_files = list(SVG_DIR.glob("*.svg"))
svg_names = [f.stem for f in svg_files]

print(f"JPG in real-detected: {len(jpg_files)}")
print(f"SVG in output/svg: {len(svg_files)}")

# For each JPG, find matching SVG and copy with correct name
copied = 0
missing = 0
for jpg_file in jpg_files:
    jpg_name = jpg_file.stem
    
    # Find matching SVG (strip date from both)
    jpg_base = jpg_name.replace(f"_{DATE}", "")
    
    for svg_file in svg_files:
        svg_name = svg_file.stem
        svg_base = svg_name.replace(f"_{DATE}", "")
        
        # Check if names match (with vector_nirmana)
        if svg_base == jpg_base or svg_base.replace("_pattern_", "_vector_nirmana_pattern_").replace("_texture", "_vector_nirmana_texture") == jpg_base:
            # Copy SVG to real-detected with JPG name
            new_svg = REAL_DIR / (jpg_name + ".svg")
            if not new_svg.exists():
                shutil.copy2(svg_file, new_svg)
                copied += 1
                print(f"Copied: {svg_file.name} -> {new_svg.name}")
            break
    else:
        # No matching SVG found
        missing += 1
        print(f"Missing SVG for: {jpg_name}")

print(f"\nCopied: {copied}")
print(f"Missing SVG: {missing}")
