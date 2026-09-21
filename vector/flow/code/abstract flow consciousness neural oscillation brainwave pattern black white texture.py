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
    """Consciousness-inspired flow with neural oscillations and brainwave patterns."""
    fig, ax = setup_ax()
    
    n_lines = 2000
    steps = 200
    step_size = 0.3
    
    # Brain regions with different oscillation frequencies
    brain_regions = [
        (20, 20, 8.0),   # Alpha waves (relaxed awareness)
        (80, 20, 13.0),  # Beta waves (focused attention)
        (20, 80, 4.0),   # Theta waves (creativity, meditation)
        (80, 80, 30.0),  # Gamma waves (consciousness binding)
        (50, 50, 1.0),   # Delta waves (deep states)
    ]
    
    for _ in range(n_lines):
        x_path, y_path = [], []
        
        x = np.random.uniform(0, 100)
        y = np.random.uniform(0, 100)
        
        for step in range(steps):
            x_path.append(x)
            y_path.append(y)
            
            dx, dy = 0, 0
            
            # Neural oscillations from different brain regions
            for rx, ry, frequency in brain_regions:
                dist = np.sqrt((x - rx)**2 + (y - ry)**2) + 0.1
                
                # Oscillation strength decreases with distance
                oscillation_strength = 10.0 / (dist + 1)
                
                # Phase of oscillation
                phase = step * frequency * 0.01
                
                # Traveling wave
                wave_speed = frequency * 0.5
                spatial_phase = dist * 0.1
                traveling_wave = np.sin(phase - spatial_phase)
                
                # Flow direction influenced by oscillation
                angle_to_region = np.arctan2(y - ry, x - rx)
                
                # Radial component (inward/outward based on oscillation)
                radial_strength = oscillation_strength * traveling_wave * 0.02
                dx += np.cos(angle_to_region) * radial_strength
                dy += np.sin(angle_to_region) * radial_strength
                
                # Tangential component (circular flow)
                tangential_strength = oscillation_strength * np.cos(phase) * 0.01
                dx += -np.sin(angle_to_region) * tangential_strength
                dy += np.cos(angle_to_region) * tangential_strength
            
            # Consciousness emergence (global integration)
            # Calculate "global workspace" activity
            global_activity = 0
            for rx, ry, frequency in brain_regions:
                region_dist = np.sqrt((x - rx)**2 + (y - ry)**2)
                if region_dist < 25:  # Within influence
                    phase = step * frequency * 0.01
                    global_activity += np.sin(phase) / (region_dist + 1)
            
            # Consciousness "binding" - when global activity is high
            if abs(global_activity) > 0.5:
                binding_strength = abs(global_activity) * 0.1
                
                # Flow toward center (integration)
                center_x, center_y = 50, 50
                dx += (center_x - x) * binding_strength * 0.02
                dy += (center_y - y) * binding_strength * 0.02
                
                # Synchronization effects
                sync_phase = global_activity * step * 0.005
                dx += 0.2 * np.sin(sync_phase + x * 0.1)
                dy += 0.2 * np.cos(sync_phase + y * 0.1)
            
            # Default mode network (resting state connectivity)
            default_centers = [(30, 50), (70, 50)]
            for dmx, dmy in default_centers:
                dm_dist = np.sqrt((x - dmx)**2 + (y - dmy)**2)
                if dm_dist < 20:
                    # Low-frequency oscillations
                    dm_phase = step * 0.5 * 0.01
                    dm_strength = (20 - dm_dist) / 20 * 0.15
                    
                    # Flow along default mode connections
                    if dmx < 50:  # Left hemisphere
                        target_x, target_y = 70, 50  # Connect to right
                    else:  # Right hemisphere
                        target_x, target_y = 30, 50  # Connect to left
                    
                    connection_dx = (target_x - x) * dm_strength * np.sin(dm_phase)
                    connection_dy = (target_y - y) * dm_strength * np.sin(dm_phase)
                    
                    dx += connection_dx * 0.1
                    dy += connection_dy * 0.1
            
            # Attention networks (top-down modulation)
            attention_focus = (50 + 20 * np.sin(step * 0.003), 
                             50 + 15 * np.cos(step * 0.002))
            
            att_dist = np.sqrt((x - attention_focus[0])**2 + (y - attention_focus[1])**2)
            if att_dist < 15:
                attention_strength = (15 - att_dist) / 15 * 0.3
                
                # Enhanced flow toward focus
                dx += (attention_focus[0] - x) * attention_strength * 0.05
                dy += (attention_focus[1] - y) * attention_strength * 0.05
                
                # Increased local connectivity
                local_noise_x = np.random.normal(0, attention_strength)
                local_noise_y = np.random.normal(0, attention_strength)
                dx += local_noise_x
                dy += local_noise_y
            
            # Quantum effects in consciousness (Penrose-Hameroff theory)
            quantum_coherence = np.sin(step * 40.0 * 0.01)  # High-frequency quantum oscillations
            if abs(quantum_coherence) > 0.9:  # Quantum coherence events
                # Sudden non-local connections
                quantum_jump_x = np.random.normal(0, 2)
                quantum_jump_y = np.random.normal(0, 2)
                dx += quantum_jump_x
                dy += quantum_jump_y
            
            # Memory consolidation (hippocampal replay)
            if 40 < x < 60 and 45 < y < 55:  # Hippocampal region
                replay_frequency = 7.0  # Theta rhythm
                replay_phase = step * replay_frequency * 0.01
                
                # Sharp-wave ripples
                if np.sin(replay_phase) > 0.8:
                    ripple_strength = 0.4
                    dx += ripple_strength * np.cos(x * 0.2 + y * 0.15)
                    dy += ripple_strength * np.sin(x * 0.15 + y * 0.2)
            
            mag = np.sqrt(dx**2 + dy**2) + 0.0001
            x += (dx / mag) * step_size
            y += (dy / mag) * step_size
            
            if x < 0 or x > 100 or y < 0 or y > 100:
                break
                
        if len(x_path) > 1:
            ax.plot(x_path, y_path, color="black", alpha=0.15, linewidth=0.8)
            
    save(fig, "abstract flow consciousness neural oscillation brainwave pattern black white texture")


if __name__ == "__main__":
    draw()