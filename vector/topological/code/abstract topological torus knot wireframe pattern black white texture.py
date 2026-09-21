import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

SIZE = 4000
DPI = 300
SEED = 42
DATE = datetime.now().strftime("%d%m%Y")

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
JPG_DIR = OUTPUT_DIR / "jpg"
SVG_DIR = OUTPUT_DIR / "svg"
JPG_DIR.mkdir(parents=True, exist_ok=True)
SVG_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(SEED)


def setup_ax():
    fig, ax = plt.subplots(figsize=(SIZE / DPI, SIZE / DPI), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_facecolor("white")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    jpg_path = JPG_DIR / f"{name} {DATE}.jpg"
    svg_path = SVG_DIR / f"{name} {DATE}.svg"
    fig.savefig(jpg_path, dpi=DPI, pad_inches=0, facecolor="white")
    fig.savefig(svg_path, format="svg", pad_inches=0, facecolor="white")
    plt.close(fig)
    print(f"Tersimpan: {jpg_path} | {svg_path}")


def abstract_topological_torus_knot_wireframe_pattern_black_white_texture():
    """Generates a Torus Knot (p, q) wireframe design."""
    fig, ax = setup_ax()
    
    # Torus knot parameters (p = winding around center, q = winding through hole)
    p = 5
    q = 7
    
    # To create a wireframe, we will draw multiple offset strands
    n_strands = 18
    t = np.linspace(0, 2 * np.pi, 2000)
    
    for i in range(n_strands):
        # Offset angle for this strand
        offset = (i / n_strands) * 2 * np.pi
        
        # Base torus knot
        r = np.cos(q * t) + 2
        x = r * np.cos(p * t)
        y = r * np.sin(p * t)
        z = -np.sin(q * t)
        
        # Expand it slightly into a tube by adding an offset normal vector
        # Approximate normal and binormal for tube generation
        dx = -p * r * np.sin(p * t) - q * np.sin(q * t) * np.cos(p * t)
        dy = p * r * np.cos(p * t) - q * np.sin(q * t) * np.sin(p * t)
        dz = -q * np.cos(q * t)
        
        # Normalize tangent
        mag = np.sqrt(dx**2 + dy**2 + dz**2)
        tx, ty, tz = dx/mag, dy/mag, dz/mag
        
        # Simple up vector trick for normal
        up_x, up_y, up_z = 0, 0, 1
        
        # Cross product (Tangent x Up)
        nx = ty * up_z - tz * up_y
        ny = tz * up_x - tx * up_z
        nz = tx * up_y - ty * up_x
        
        n_mag = np.sqrt(nx**2 + ny**2 + nz**2)
        nx, ny, nz = nx/n_mag, ny/n_mag, nz/n_mag
        
        # Cross product (Tangent x Normal) = Binormal
        bx = ty * nz - tz * ny
        by = tz * nx - tx * nz
        bz = tx * ny - ty * nx
        
        # Tube radius
        tube_r = 0.4
        
        # Add the offset to the base path
        x_strand = x + tube_r * (np.cos(offset) * nx + np.sin(offset) * bx)
        y_strand = y + tube_r * (np.cos(offset) * ny + np.sin(offset) * by)
        z_strand = z + tube_r * (np.cos(offset) * nz + np.sin(offset) * bz)
        
        # Isometric projection
        proj_x = x_strand * np.cos(np.pi/6) - y_strand * np.cos(np.pi/6)
        proj_y = x_strand * np.sin(np.pi/6) + y_strand * np.sin(np.pi/6) + z_strand
        
        # Dynamic line width based on Z (depth)
        lw = 1.0 + (z_strand + 2.5) * 0.3
        # In matplotlib we can't easily vary line width per segment using a single line plot,
        # so we just use an average or a thin line. Let's stick to a thin line and low alpha.
        
        ax.plot(proj_x, proj_y, color="black", linewidth=0.8, alpha=0.6)
        
    save(fig, "abstract topological torus knot wireframe pattern black white texture")


if __name__ == "__main__":
    abstract_topological_torus_knot_wireframe_pattern_black_white_texture()
