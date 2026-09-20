"""
Fix EPS save di semua file Python halloween:
- Ganti facecolor="white" hardcoded dengan fig.get_facecolor()
- Pastikan semua file punya EPS support yang benar
"""
import re
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent / "code"
py_files = sorted([f for f in CODE_DIR.glob("*.py") if f.name != "vector_icon.py"])

fixed = 0
already_ok = 0
no_eps = 0

for fpath in py_files:
    text = fpath.read_text(encoding="utf-8")
    original = text

    # Cek apakah sudah punya EPS block
    if "EPS_DIR" not in text:
        print(f"[NO EPS] {fpath.name}")
        no_eps += 1
        continue

    # Fix 1: facecolor="white" hardcoded di EPS save → fig.get_facecolor()
    text = re.sub(
        r'(fig\.savefig\(eps_path, format="eps", pad_inches=0, )facecolor="white"(, dpi=DPI\))',
        r'\1facecolor=fig.get_facecolor()\2',
        text
    )

    if text != original:
        fpath.write_text(text, encoding="utf-8")
        print(f"[FIXED] {fpath.name}")
        fixed += 1
    else:
        already_ok += 1

print(f"\n=== DONE: {fixed} fixed, {already_ok} already ok, {no_eps} no EPS ===")
