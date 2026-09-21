"""
Hapus kode EPS dari semua file Python halloween.
Mengembalikan file ke kondisi hanya generate JPG + SVG.
"""
import re
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent / "code"
py_files = sorted([f for f in CODE_DIR.glob("*.py") if f.name != "vector_icon.py"])

removed = 0
skipped = 0

for fpath in py_files:
    text = fpath.read_text(encoding="utf-8")
    original = text

    if "EPS_DIR" not in text:
        skipped += 1
        continue

    # Hapus EPS_DIR definition
    text = re.sub(r'\nEPS_DIR = OUTPUT_DIR / "eps"', "", text)

    # Hapus EPS_DIR.mkdir
    text = re.sub(r'\nEPS_DIR\.mkdir\(parents=True,\s*exist_ok=True\)', "", text)

    # Hapus blok eps save (berbagai variasi)
    # Variasi 1: dengan get_facecolor
    text = re.sub(
        r'\n    eps_path = EPS_DIR / f"\{name\} \{DATE\}\.eps"\n'
        r'    orig_size = fig\.get_size_inches\(\)\n'
        r'    fig\.set_size_inches\(30, 30\)\n'
        r'    fig\.savefig\(eps_path, format="eps", pad_inches=0, facecolor=fig\.get_facecolor\(\), dpi=DPI\)\n'
        r'    fig\.set_size_inches\(orig_size\[0\], orig_size\[1\]\)',
        "", text
    )
    # Variasi 2: dengan facecolor="white"
    text = re.sub(
        r'\n    eps_path = EPS_DIR / f"\{name\} \{DATE\}\.eps"\n'
        r'    orig_size = fig\.get_size_inches\(\)\n'
        r'    fig\.set_size_inches\(30, 30\)\n'
        r'    fig\.savefig\(eps_path, format="eps", pad_inches=0, facecolor="white", dpi=DPI\)\n'
        r'    fig\.set_size_inches\(orig_size\[0\], orig_size\[1\]\)',
        "", text
    )

    # Hapus eps dari print statement jika ada
    text = re.sub(
        r'( \| \{eps_path\})',
        "", text
    )

    if text != original:
        fpath.write_text(text, encoding="utf-8")
        print(f"[REMOVED] {fpath.name}")
        removed += 1
    else:
        print(f"[WARN] No change: {fpath.name}")

print(f"\n=== DONE: {removed} removed, {skipped} skipped (no EPS) ===")
