"""
Konversi ulang semua SVG di halloween/submitted/svg ke EPS di halloween/submitted/eps
dengan output_width=4000 agar memenuhi syarat 4MP+ di platform submission.
"""
import cairosvg
from pathlib import Path

BASE = Path(__file__).resolve().parent / "submitted"
SVG_DIR = BASE / "svg"
EPS_DIR = BASE / "eps"
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
            output_width=4000,
            output_height=4000,
        )
        # Cek bounding box hasil
        with open(eps_path, "rb") as f:
            header = f.read(500).decode("latin-1")
        bb = [l for l in header.split("\n") if "BoundingBox" in l and "%%%" not in l]
        print(f"[OK] {eps_path.name[:70]}  {bb[0] if bb else ''}")
        success += 1
    except Exception as e:
        print(f"[ERROR] {svg_path.name}: {e}")
        errors.append((svg_path.name, str(e)))

print(f"\n=== DONE: {success}/{len(svg_files)} berhasil, {len(errors)} error ===")
if errors:
    for name, err in errors:
        print(f"  - {name}: {err}")
