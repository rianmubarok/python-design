import re
from pathlib import Path

files = list(Path('.').glob('*.py'))
for f in files:
    if f.name == 'update_eps.py':
        continue
    content = f.read_text(encoding='utf-8')
    
    # Add EPS_DIR after SVG_DIR
    if 'EPS_DIR' not in content:
        content = content.replace(
            'SVG_DIR = OUTPUT_DIR / "svg"\nJPG_DIR.mkdir(parents=True, exist_ok=True)\nSVG_DIR.mkdir(parents=True, exist_ok=True)',
            'SVG_DIR = OUTPUT_DIR / "svg"\nEPS_DIR = OUTPUT_DIR / "eps"\nJPG_DIR.mkdir(parents=True, exist_ok=True)\nSVG_DIR.mkdir(parents=True, exist_ok=True)\nEPS_DIR.mkdir(parents=True, exist_ok=True)'
        )
    
    # Update save function to include EPS
    if 'eps_path' not in content:
        old_save = '''def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")'''
        
        new_save = '''def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    eps_path = EPS_DIR / f"{name} {DATE}.eps"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    fig.savefig(eps_path, format="eps", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path} | {eps_path}")'''
        
        content = content.replace(old_save, new_save)
    
    f.write_text(content, encoding='utf-8')
    print(f'Updated: {f.name}')

print("Done!")