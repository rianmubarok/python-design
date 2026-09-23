import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from pathlib import Path as FilePath
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 123
DATE = datetime.now().strftime("%d%m%Y")
SCRIPT_DIR = FilePath(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"; SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True); SVG_DIR.mkdir(parents=True, exist_ok=True)
np.random.seed(SEED)

def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE/DPI, SIZE/DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax

def save(fig, name):
    fig.savefig(JPG_DIR/f"{name} {DATE}.jpg", dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(SVG_DIR/f"{name} {DATE}.svg", format="svg", pad_inches=0, facecolor="white")
    plt.close(fig); print(f"Saved: {name}")

def draw_maple(ax, cx, cy, size, angle, filled):
    """Daun Maple tajam & proporsional."""
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    pts = [
        (0.0, -0.9), (0.04, -0.3), (0.25, -0.45), (0.35, -0.3), (0.22, -0.1),
        (0.75, -0.15), (0.85, 0.1), (0.55, 0.2), (0.75, 0.45), (0.55, 0.45), (0.4, 0.3),
        (0.45, 0.75), (0.25, 0.65), (0.0, 1.0),
        (-0.25, 0.65), (-0.45, 0.75), (-0.4, 0.3), (-0.55, 0.45), (-0.75, 0.45),
        (-0.55, 0.2), (-0.85, 0.1), (-0.75, -0.15), (-0.22, -0.1), (-0.35, -0.3),
        (-0.25, -0.45), (-0.04, -0.3), (0.0, -0.9)
    ]
    codes = [Path.MOVETO] + [Path.LINETO]*(len(pts)-2) + [Path.CLOSEPOLY]
    
    fc = "black" if filled else "white"
    ec = "black"
    lw = 1.0 if not filled else 0.5
    
    path = Path(pts, codes)
    patch = patches.PathPatch(path, facecolor=fc, edgecolor=ec, lw=lw, transform=trans, zorder=3)
    ax.add_patch(patch)

def draw_ginkgo(ax, cx, cy, size, angle, filled):
    """Daun Ginkgo kipas alami dengan belahan kecil dan tangkai melengkung."""
    rad = np.deg2rad(angle)
    trans = transforms.Affine2D().scale(size).rotate(rad).translate(cx, cy) + ax.transData
    
    # Kurva kipas ginkgo dengan lekukan di tengah atas
    t1 = np.linspace(-np.pi*0.4, -0.05, 15)
    t2 = np.linspace(0.05, np.pi*0.4, 15)
    
    x_fan1 = 0.85 * np.sin(t1)
    y_fan1 = 0.85 * np.cos(t1)
    
    x_fan2 = 0.85 * np.sin(t2)
    y_fan2 = 0.85 * np.cos(t2)
    
    # Gabungkan titik kipas + notch tengah + pangkal tangkai
    xg = np.concatenate([[0.0, -0.02], x_fan1, [0.0], x_fan2, [0.02, 0.0]])
    yg = np.concatenate([[-0.8, -0.1], y_fan1, [0.65], y_fan2, [-0.1, -0.8]])
    
    pts = list(zip(xg, yg))
    codes = [Path.MOVETO] + [Path.LINETO]*(len(pts)-2) + [Path.CLOSEPOLY]
    path = Path(pts, codes)
    
    fc = "black" if filled else "white"
    patch = patches.PathPatch(path, facecolor=fc, edgecolor="black", lw=1.0 if not filled else 0.5, transform=trans, zorder=3)
    ax.add_patch(patch)

def draw_wind_swirl(ax):
    """Garis angin spiral konsentris yang halus mendampingi sebaran daun."""
    for i in range(35):
        t = np.linspace(0.2*np.pi, 5.5*np.pi, 120)
        r = 6 + 2.8 * t + np.random.uniform(-1.5, 1.5)
        x = 50 + r * np.cos(t + i*0.15)
        y = 50 + r * np.sin(t + i*0.15)
        ax.plot(x, y, color="black", lw=np.random.uniform(0.4, 1.2), alpha=np.random.uniform(0.2, 0.6), zorder=1)

def main():
    fig, ax = setup_ax()
    
    # 1. Garis pusaran angin
    draw_wind_swirl(ax)
    
    # 2. Sebaran daun melingkar dinamis tanpa penumpukan padat di pusat
    n_leaves = 220
    for i in range(n_leaves):
        t = 0.8 * np.pi + (i / n_leaves) * 5.2 * np.pi
        r = 8 + 2.5 * t + np.random.uniform(-4, 4)  # Mulai r dari 8 agar pusat tidak tumpat
        
        cx = 50 + r * np.cos(t)
        cy = 50 + r * np.sin(t)
        
        if cx < 3 or cx > 97 or cy < 3 or cy > 97:
            continue
            
        size = np.random.uniform(1.6, 3.8)
        angle = np.rad2deg(t) + 90 + np.random.uniform(-25, 25)
        filled = np.random.choice([True, False], p=[0.45, 0.55])
        
        if np.random.random() > 0.45:
            draw_maple(ax, cx, cy, size, angle, filled)
        else:
            draw_ginkgo(ax, cx, cy, size, angle, filled)
            
    save(fig, "abstract autumn wind spiral falling leaves dynamic flow pattern black white texture")

if __name__ == "__main__":
    main()