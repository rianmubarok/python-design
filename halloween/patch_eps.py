"""
Patch semua file Python halloween untuk menambahkan EPS output.
Modifikasi:
1. Tambah EPS_DIR di blok direktori
2. Tambah EPS save di fungsi save()
"""
import re
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent / "code"
py_files = sorted([f for f in CODE_DIR.glob("*.py") if f.name != "vector_icon.py"])

patched = 0
skipped = 0
errors = []

for fpath in py_files:
    text = fpath.read_text(encoding="utf-8")
    original = text

    # Skip jika sudah ada EPS_DIR
    if "EPS_DIR" in text:
        print(f"[SKIP] {fpath.name}")
        skipped += 1
        continue

    # 1. Tambahkan EPS_DIR setelah SVG_DIR definition
    text = re.sub(
        r"(SVG_DIR\s*=\s*OUTPUT_DIR\s*/\s*[\"']svg[\"'])",
        r"\1\nEPS_DIR = OUTPUT_DIR / \"eps\"",
        text
    )

    # 2. Tambahkan EPS_DIR.mkdir setelah SVG_DIR.mkdir
    text = re.sub(
        r"(SVG_DIR\.mkdir\(parents=True,\s*exist_ok=True\))",
        r"\1\nEPS_DIR.mkdir(parents=True, exist_ok=True)",
        text
    )

    # 3. Patch fungsi save() - tambah eps_path
    # Cari pattern save svg dan tambahkan eps setelahnya
    # Pattern: fig.savefig(svg_path, ...)\n    plt.close(fig)
    text = re.sub(
        r"(    fig\.savefig\(svg_path[^\n]+\n)(    plt\.close\(fig\))",
        r"\1    eps_path = EPS_DIR / f\"{name} {DATE}.eps\"\n"
        r"    orig_size = fig.get_size_inches()\n"
        r"    fig.set_size_inches(30, 30)\n"
        r"    fig.savefig(eps_path, format=\"eps\", pad_inches=0, facecolor=\"white\", dpi=DPI)\n"
        r"    fig.set_size_inches(orig_size[0], orig_size[1])\n"
        r"\2",
        text
    )

    # 4. Patch print statement di save() jika ada, untuk include eps
    text = re.sub(
        r'(    print\(f"Saved: \{jpg_path\}"\))',
        r'    print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")',
        text
    )
    # Variasi lain print
    text = re.sub(
        r'(    print\(f"Tersimpan: \{jpg_path\}"\))',
        r'    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")',
        text
    )

    if text != original:
        fpath.write_text(text, encoding="utf-8")
        print(f"[PATCHED] {fpath.name}")
        patched += 1
    else:
        print(f"[WARN] No change: {fpath.name}")
        errors.append(fpath.name)

print(f"\n=== DONE: {patched} patched, {skipped} skipped, {len(errors)} warnings ===")
if errors:
    print("Files with no change (check manually):")
    for e in errors:
        print(f"  - {e}")
