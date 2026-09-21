"""
Konversi semua file SVG di halloween/output/svg ke EPS di halloween/output/eps
menggunakan cairosvg.
"""
import cairosvg
from pathlib import Path

SVG_DIR = Path(__file__).resolve().parent / "output" / "svg"
EPS_DIR = Path(__file__).resolve().parent / "output" / "eps"
EPS_DIR.mkdir(parents=True, exist_ok=True)

svg_files = sorted(SVG_DIR.glob("*.svg"))
print(f"Ditemukan {len(svg_files)} file SVG\n")

success = 0
errors = []

for svg_path in svg_files:
    eps_path = EPS_DIR / (svg_path.stem + ".eps")

    try:
        cairosvg.svg2ps(
            url=str(svg_path),
            write_to=str(eps_path),
            output_width=2160,
            output_height=2160,
        )
        print(f"[OK] {eps_path.name}")
        success += 1
    except Exception as e:
        print(f"[ERROR] {svg_path.name}: {e}")
        errors.append((svg_path.name, str(e)))

print(f"\n=== DONE: {success}/{len(svg_files)} berhasil, {len(errors)} error ===")
if errors:
    print("\nFile dengan error:")
    for name, err in errors:
        print(f"  - {name}: {err}")
