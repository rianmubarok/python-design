"""Fix escaped quotes yang masuk ke file Python dari patch sebelumnya."""
import re
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent / "code"
py_files = sorted([f for f in CODE_DIR.glob("*.py") if f.name != "vector_icon.py"])

fixed = 0
for fpath in py_files:
    text = fpath.read_text(encoding="utf-8")
    original = text

    # Fix all escaped quotes in the file
    text = text.replace(r'OUTPUT_DIR / \"eps\"', 'OUTPUT_DIR / "eps"')
    text = text.replace(r'EPS_DIR / f\"{name} {DATE}.eps\"', 'EPS_DIR / f"{name} {DATE}.eps"')
    text = text.replace(r'format=\"eps\"', 'format="eps"')
    text = text.replace(r'facecolor=\"white\"', 'facecolor="white"')
    text = text.replace(r'facecolor=\"black\"', 'facecolor="black"')
    text = text.replace(r'facecolor=fig.get_facecolor()', 'facecolor=fig.get_facecolor()')

    if text != original:
        fpath.write_text(text, encoding="utf-8")
        print(f"[FIXED] {fpath.name}")
        fixed += 1

print(f"\nDone: {fixed} files fixed")
