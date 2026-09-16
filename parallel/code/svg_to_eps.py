"""Convert generated SVG files to EPS (vector) for microstock submission.

For every ``svg/`` folder found, a sibling ``eps/`` folder is created and each
``*.svg`` is written as a matching ``*.eps`` (same base name). The EPS artboard
is scaled to ARTBOARD (default 4000x4000) so it matches the JPG dimensions.

Existing EPS that are newer than their SVG are skipped, so it is safe to re-run.
Use ``--force`` to convert everything regardless.

Usage (from any directory):
    python svg_to_eps.py                 # parallel/ category, skip up-to-date
    python svg_to_eps.py --force         # parallel/, regenerate all
    python svg_to_eps.py geometric       # another category by name
    python svg_to_eps.py all --force     # every category, regenerate all
"""

import sys
from pathlib import Path

import cairosvg

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_ROOT = PROJECT_ROOT / "parallel"

ARTBOARD = 4000  # final EPS artboard size in points (matches JPG px)
# cairosvg sizes output in CSS px at 96 dpi; 1 pt = 96/72 px.
OUTPUT_UNITS = round(ARTBOARD * 96 / 72)


def convert(root, force=False):
    total = 0
    svg_dirs = sorted({p.parent for p in root.rglob("*.svg")})
    if not svg_dirs:
        print(f"No SVG files found under: {root}")
        return
    for svg_dir in svg_dirs:
        eps_dir = svg_dir.parent / "eps"
        eps_dir.mkdir(parents=True, exist_ok=True)
        converted = skipped = 0
        for svg in sorted(svg_dir.glob("*.svg")):
            out = eps_dir / f"{svg.stem}.eps"
            if not force and out.exists() and out.stat().st_mtime >= svg.stat().st_mtime:
                skipped += 1
                continue
            cairosvg.svg2eps(
                bytestring=svg.read_bytes(),
                write_to=str(out),
                output_width=OUTPUT_UNITS,
                output_height=OUTPUT_UNITS,
            )
            converted += 1
        total += converted
        print(f"{svg_dir.relative_to(root)} -> {converted} EPS "
              f"({skipped} up-to-date) in {eps_dir.relative_to(root)}")
    print(f"Total converted: {total} EPS (artboard {ARTBOARD}x{ARTBOARD})")


def main():
    args = sys.argv[1:]
    force = "--force" in args
    positional = [a for a in args if not a.startswith("--")]
    target = positional[0] if positional else None

    if target is None:
        root = DEFAULT_ROOT
    elif target.lower() == "all":
        root = PROJECT_ROOT
    else:
        root = PROJECT_ROOT / target
    root = root.resolve()
    if not root.is_dir():
        print(f"Folder not found: {root}")
        sys.exit(1)
    print(f"Converting SVG -> EPS under: {root} (force={force})")
    convert(root, force=force)


if __name__ == "__main__":
    main()
