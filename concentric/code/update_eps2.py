import re
from pathlib import Path

files = list(Path('.').glob('*.py'))
for f in files:
    if f.name == 'update_eps.py' or f.name == 'update_eps2.py':
        continue
    content = f.read_text(encoding='utf-8')
    
    # Add EPS_DIR after SVG_DIR if not present
    if 'EPS_DIR' not in content:
        content = content.replace(
            'SVG_DIR = OUTPUT_DIR / "svg"\nJPG_DIR.mkdir(parents=True, exist_ok=True)\nSVG_DIR.mkdir(parents=True, exist_ok=True)',
            'SVG_DIR = OUTPUT_DIR / "svg"\nEPS_DIR = OUTPUT_DIR / "eps"\nJPG_DIR.mkdir(parents=True, exist_ok=True)\nSVG_DIR.mkdir(parents=True, exist_ok=True)\nEPS_DIR.mkdir(parents=True, exist_ok=True)'
        )
    
    # Find and replace save function - use regex to handle variations
    # Pattern: def save(fig, name): followed by jpg/svg save lines
    def replace_save(match):
        func = match.group(0)
        if 'eps_path' in func:
            return func
        # Add eps_path line before fig.savefig
        func = func.replace(
            'svg_path = SVG_DIR / f"{name} {DATE}.svg"',
            'svg_path = SVG_DIR / f"{name} {DATE}.svg"\n    eps_path = EPS_DIR / f"{name} {DATE}.eps"'
        )
        # Add eps save line after svg save
        func = func.replace(
            'fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")',
            'fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")\n    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white")'
        )
        # Update print statement
        func = func.replace(
            'print(f"Tersimpan: {jpg_path} | {svg_path}")',
            'print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")'
        )
        func = func.replace(
            'print(f"Saved: {jpg_path} | {svg_path}")',
            'print(f"Saved: {jpg_path} | {svg_path} | {eps_path}")'
        )
        return func
    
    # Use regex to find save functions
    content = re.sub(
        r'def save\(fig, name\):.*?(?=\n\ndef |\nif __name__|$)',
        replace_save,
        content,
        flags=re.DOTALL
    )
    
    f.write_text(content, encoding='utf-8')
    print(f'Updated: {f.name}')

print("Done!")