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
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
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


def draw():
    """DNA double helix flow with base pair interactions and genetic information."""
    fig, ax = setup_ax()
    
    n_lines = 2000
    steps = 180
    step_size = 0.35
    
    # DNA parameters
    helix_radius = 15
    helix_pitch = 20  # Distance per full turn
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Find nearest helix axis (vertical lines at x = 25, 50, 75)
            helix_centers = [25, 50, 75]
            distances = [abs(x - hx) for hx in helix_centers]
            nearest_helix = helix_centers[np.argmin(distances)]
            
            # Distance from helix axis
            r_from_axis = abs(x - nearest_helix)
            
            # Height along helix
            z = y
            
            # Double helix flow
            if r_from_axis < helix_radius:
                # Two counter-rotating strands
                helix_angle = z / helix_pitch * 2 * np.pi
                
                # Strand 1 (right-handed helix)
                strand1_x = nearest_helix + helix_radius * 0.7 * np.cos(helix_angle)
                strand1_target = np.abs(x - strand1_x)
                
                # Strand 2 (right-handed helix, 180° phase shift)
                strand2_x = nearest_helix + helix_radius * 0.7 * np.cos(helix_angle + np.pi)
                strand2_target = np.abs(x - strand2_x)
                
                # Flow toward nearest strand
                if strand1_target < strand2_target:
                    target_x = strand1_x
                    strand_id = 1
                else:
                    target_x = strand2_x
                    strand_id = 2
                
                # Helical flow
                dx = (target_x - x) * 0.1
                
                # Upward flow with helical twist
                helix_tangent_y = 1.0
                helix_tangent_x = -helix_radius * np.sin(helix_angle) * 2 * np.pi / helix_pitch
                
                if strand_id == 2:
                    helix_tangent_x *= -1  # Opposite twist for second strand
                
                dy = helix_tangent_y * 0.3
                dx += helix_tangent_x * 0.1
                
                # Base pair hydrogen bonding (attraction between strands)
                if r_from_axis < helix_radius * 0.5:
                    # Inside the helix - base pair region
                    base_pair_period = 3.4  # Angstroms scaled
                    base_position = (z % base_pair_period) / base_pair_period
                    
                    # Simulate base pair types (A-T, G-C)
                    if base_position < 0.4 or (0.6 < base_position < 0.9):  # Base pair regions
                        # Strong lateral attraction
                        center_attraction = (nearest_helix - x) * 0.3
                        dx += center_attraction
                        
                        # Vertical flow follows base stacking
                        dy += 0.2 * np.sin(z / base_pair_period * 2 * np.pi)
                
                # Major and minor groove effects
                groove_angle = helix_angle % (2 * np.pi)
                if 0.2 < groove_angle / (2 * np.pi) < 0.4:  # Major groove
                    dx *= 1.2  # Enhanced flow
                elif 0.6 < groove_angle / (2 * np.pi) < 0.8:  # Minor groove
                    dx *= 0.8  # Reduced flow
                
            else:
                # Outside helix - random diffusion with slight bias toward helix
                dx = np.random.normal(0, 0.5) + (nearest_helix - x) * 0.02
                dy = np.random.normal(0, 0.5)
            
            # DNA packaging effects (supercoiling)
            supercoil_strength = np.sin(y * 0.1) * 0.1
            dx += supercoil_strength * np.cos(y * 0.05)
            dy += supercoil_strength * 0.5
            
            # Transcription bubble (localized unwinding)
            bubble_centers = [30, 70]
            for bubble_y in bubble_centers:
                bubble_dist = np.sqrt((y - bubble_y)**2 + (x - nearest_helix)**2)
                if bubble_dist < 8:
                    # Unwinding flow
                    unwind_strength = (8 - bubble_dist) / 8 * 0.4
                    dx += unwind_strength * (x - nearest_helix)
                    dy += unwind_strength * np.sign(y - bubble_y)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.2, linewidth=0.8)
            
    save(fig, "abstract flow dna double helix genetic code pattern black white texture")


if __name__ == "__main__":
    draw()