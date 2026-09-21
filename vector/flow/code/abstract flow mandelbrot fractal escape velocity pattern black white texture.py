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


def mandelbrot_escape_time(cx, cy, max_iter=100):
    """Calculate escape time for Mandelbrot set."""
    z = 0 + 0j
    c = cx + cy * 1j
    
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iter


def mandelbrot_gradient(cx, cy, epsilon=0.001):
    """Estimate gradient of escape time function."""
    escape_center = mandelbrot_escape_time(cx, cy)
    escape_right = mandelbrot_escape_time(cx + epsilon, cy)
    escape_up = mandelbrot_escape_time(cx, cy + epsilon)
    
    grad_x = (escape_right - escape_center) / epsilon
    grad_y = (escape_up - escape_center) / epsilon
    
    return grad_x, grad_y


def draw():
    """Flow based on Mandelbrot set escape velocity gradients."""
    fig, ax = setup_ax()
    
    n_lines = 2000
    steps = 150
    step_size = 0.4
    
    # Mandelbrot coordinate mapping
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -2.0, 2.0
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for _ in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            # Convert to Mandelbrot coordinates
            mx = x_min + (x / 100) * (x_max - x_min)
            my = y_min + (y / 100) * (y_max - y_min)
            
            # Get escape time and gradient
            escape_time = mandelbrot_escape_time(mx, my, max_iter=50)
            grad_x, grad_y = mandelbrot_gradient(mx, my, epsilon=0.01)
            
            # Flow direction based on gradient
            if escape_time < 50:  # Outside Mandelbrot set
                # Flow along iso-escape-time lines (perpendicular to gradient)
                dx = -grad_y * 0.1
                dy = grad_x * 0.1
                
                # Add attraction to set boundary
                boundary_attraction = (50 - escape_time) / 50 * 0.05
                dx += -grad_x * boundary_attraction
                dy += -grad_y * boundary_attraction
                
            else:  # Inside Mandelbrot set
                # Chaotic flow based on Julia set dynamics
                z = mx + my * 1j
                
                # Iterate a few times to get flow direction
                z_next = z*z + (mx + my * 1j)
                flow_complex = z_next - z
                
                dx = flow_complex.real * 10
                dy = flow_complex.imag * 10
                
                # Add orbit behavior
                orbit_length = 0
                z_orbit = z
                for _ in range(20):
                    z_orbit = z_orbit*z_orbit + (mx + my * 1j)
                    orbit_length += abs(z_orbit - z)
                
                # Flow based on orbit stability
                orbit_factor = min(orbit_length / 10, 1.0)
                dx *= orbit_factor
                dy *= orbit_factor
            
            # Add fractal noise for detail
            fractal_scale = 5.0
            noise_x = np.sin(mx * fractal_scale) * np.cos(my * fractal_scale) * 0.2
            noise_y = np.cos(mx * fractal_scale) * np.sin(my * fractal_scale) * 0.2
            
            dx += noise_x
            dy += noise_y
            
            # Zoom effects (approach or recede from set)
            zoom_center_x, zoom_center_y = 50, 50  # Canvas center
            zoom_factor = 0.01
            zoom_dx = (x - zoom_center_x) * zoom_factor
            zoom_dy = (y - zoom_center_y) * zoom_factor
            
            if escape_time > 30:  # Deep inside set
                dx -= zoom_dx  # Zoom in
                dy -= zoom_dy
            elif escape_time < 10:  # Far outside set
                dx += zoom_dx  # Zoom out
                dy += zoom_dy
            
            # Convert back to canvas coordinates
            scale_x = 100 / (x_max - x_min)
            scale_y = 100 / (y_max - y_min)
            dx *= scale_x
            dy *= scale_y
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.25, linewidth=0.7)
            
    save(fig, "abstract flow mandelbrot fractal escape velocity pattern black white texture")


if __name__ == "__main__":
    draw()