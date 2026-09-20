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


def quantum_interference_waveform():
    """Pola interferensi kuantum dengan gelombang probabilistik dan kolaps fungsi gelombang."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Parameter sistem kuantum
    n_energy_levels = 8
    n_wave_points = 200
    
    # Layer 1: Orbital elektron (fungsi gelombang probabilistik)
    for level in range(n_energy_levels):
        energy = level + 1
        orbital_radius = 5 + energy * 4.5
        
        # Fungsi gelombang radial (probabilitas)
        theta = np.linspace(0, 2 * np.pi, n_wave_points)
        
        for harmonic in range(1, 4):  # Harmonik orbital
            # Fungsi gelombang dengan interferensi
            wave_function = np.sin(energy * theta * harmonic) * np.cos(harmonic * theta * 2)
            probability_density = np.abs(wave_function) ** 2
            
            # Radius orbital dengan modulasi gelombang
            modulated_radius = orbital_radius * (1 + 0.15 * probability_density)
            
            x_orbital = center_x + modulated_radius * np.cos(theta)
            y_orbital = center_y + modulated_radius * np.sin(theta)
            
            # Ketebalan berdasarkan probabilitas
            lw = 0.4 + 0.8 * (probability_density.max() / 2)
            alpha = 0.3 + 0.4 * (level / n_energy_levels)
            
            ax.plot(x_orbital, y_orbital, color="black", linewidth=lw, alpha=alpha)
            
            # Update bounding box
            min_x, max_x = min(min_x, x_orbital.min()), max(max_x, x_orbital.max())
            min_y, max_y = min(min_y, y_orbital.min()), max(max_y, y_orbital.max())
            
            # Titik kuantum (partikel teramati)
            if np.random.random() < 0.3:  # Probabilitas observasi
                obs_theta = np.random.choice(theta)
                obs_radius = orbital_radius * (1 + 0.15 * np.abs(np.sin(energy * obs_theta * harmonic)))
                obs_x = center_x + obs_radius * np.cos(obs_theta)
                obs_y = center_y + obs_radius * np.sin(obs_theta)
                
                # Ukuran titik berdasarkan tingkat energi
                marker_size = 0.5 + 0.8 * (energy / n_energy_levels)
                ax.plot(obs_x, obs_y, marker="o", markersize=marker_size, 
                        color="black", alpha=0.7)
    
    # Layer 2: Interferensi gelombang de Broglie
    n_interference_sources = 5
    source_positions = []
    
    for i in range(n_interference_sources):
        angle = i * 2 * np.pi / n_interference_sources
        distance = 15 + np.random.uniform(-3, 3)
        source_x = center_x + distance * np.cos(angle)
        source_y = center_y + distance * np.sin(angle)
        source_positions.append((source_x, source_y))
        
        # Sumber gelombang
        ax.plot(source_x, source_y, marker="*", markersize=3, 
                color="black", alpha=0.9)
    
    # Pola interferensi
    grid_size = 80
    x_grid = np.linspace(center_x - 25, center_x + 25, grid_size)
    y_grid = np.linspace(center_y - 25, center_y + 25, grid_size)
    
    interference_intensity = np.zeros((grid_size, grid_size))
    
    for i, sx in enumerate(x_grid):
        for j, sy in enumerate(y_grid):
            total_wave = 0
            for source_x, source_y in source_positions:
                distance = np.sqrt((sx - source_x)**2 + (sy - source_y)**2)
                wavelength = 3.0 + np.random.uniform(0.5, 1.5)
                phase = 2 * np.pi * distance / wavelength
                total_wave += np.cos(phase)
            
            interference_intensity[j, i] = np.abs(total_wave) / n_interference_sources
    
    # Kontur interferensi
    levels = np.linspace(0.1, 0.9, 8)
    contour = ax.contour(x_grid, y_grid, interference_intensity, levels=levels,
                        colors="black", linewidths=0.6, alpha=0.5)
    
    # Update bounding box dari grid (simpler approach)
    min_x, max_x = min(min_x, x_grid.min()), max(max_x, x_grid.max())
    min_y, max_y = min(min_y, y_grid.min()), max(max_y, y_grid.max())
    
    # Layer 3: Kolaps fungsi gelombang (pengukuran kuantum)
    n_measurements = 12
    measurement_angles = np.linspace(0, 2 * np.pi, n_measurements, endpoint=False)
    
    for i, angle in enumerate(measurement_angles):
        measurement_radius = 32
        measurement_x = center_x + measurement_radius * np.cos(angle)
        measurement_y = center_y + measurement_radius * np.sin(angle)
        
        # "Pengukuran" menyebabkan kolaps
        collapse_lines = 8
        for line in range(collapse_lines):
            line_angle = angle + line * (2 * np.pi / collapse_lines)
            line_length = 6 + np.random.uniform(0, 3)
            
            end_x = measurement_x + line_length * np.cos(line_angle)
            end_y = measurement_y + line_length * np.sin(line_angle)
            
            ax.plot([measurement_x, end_x], [measurement_y, end_y], 
                   color="black", linewidth=0.5, alpha=0.6)
        
        # Efek kolaps (gelombang berhenti)
        collapse_waves = 5
        for wave in range(collapse_waves):
            wave_radius = 2 + wave * 1.5
            wave_x = measurement_x + wave_radius * np.cos(angle + np.pi/2)
            wave_y = measurement_y + wave_radius * np.sin(angle + np.pi/2)
            
            # Garis gelombang terputus
            ax.plot(wave_x, wave_y, marker="x", markersize=1.2, 
                    color="black", alpha=0.5)
    
    # Layer 4: Superposisi kuantum
    n_superpositions = 6
    superposition_radius = 18
    
    for i in range(n_superpositions):
        super_angle = i * 2 * np.pi / n_superpositions
        super_x = center_x + superposition_radius * np.cos(super_angle)
        super_y = center_y + superposition_radius * np.sin(super_angle)
        
        # State superposisi (multiple states overlapping)
        n_states = 3
        for state in range(n_states):
            state_angle = super_angle + state * (2 * np.pi / n_states)
            state_radius = 4
            
            # State yang tumpang tindih
            state_points = []
            for t in np.linspace(0, 2 * np.pi, 50):
                x_state = super_x + state_radius * np.cos(t + state_angle)
                y_state = super_y + state_radius * np.sin(t + state_angle)
                state_points.append((x_state, y_state))
            
            state_points.append(state_points[0])  # Tutup loop
            x_state = [p[0] for p in state_points]
            y_state = [p[1] for p in state_points]
            
            ax.plot(x_state, y_state, color="black", linewidth=0.4, 
                    alpha=0.4, linestyle="--")
            
            # Update bounding box
            min_x, max_x = min(min_x, min(x_state)), max(max_x, max(x_state))
            min_y, max_y = min(min_y, min(y_state)), max(max_y, max(y_state))
    
    # Layer 5: Entanglement kuantum (keterkaitan)
    n_entangled_pairs = 4
    entanglement_radius = 22
    
    for pair in range(n_entangled_pairs):
        angle1 = pair * 2 * np.pi / n_entangled_pairs
        angle2 = angle1 + np.pi / 2  # Partner entangled
        
        # Partikel entangled
        ent1_x = center_x + entanglement_radius * np.cos(angle1)
        ent1_y = center_y + entanglement_radius * np.sin(angle1)
        ent2_x = center_x + entanglement_radius * np.cos(angle2)
        ent2_y = center_y + entanglement_radius * np.sin(angle2)
        
        # Garis entanglement (keterkaitan)
        n_ent_lines = 15
        for line in range(n_ent_lines):
            t = line / (n_ent_lines - 1)
            
            # Kurva entanglement
            ent_x = (1-t)**3 * ent1_x + 3*(1-t)**2*t*(ent1_x+3) + \
                   3*(1-t)*t**2*(ent2_x-3) + t**3*ent2_x
            ent_y = (1-t)**3 * ent1_y + 3*(1-t)**2*t*(ent1_y+3) + \
                   3*(1-t)*t**2*(ent2_y-3) + t**3*ent2_y
            
            ax.plot(ent_x, ent_y, marker=".", markersize=0.3, 
                    color="black", alpha=0.3)
        
        # Partikel entangled
        ax.plot(ent1_x, ent1_y, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
        ax.plot(ent2_x, ent2_y, marker="o", markersize=1.5, 
                color="black", alpha=0.8)
        
        # Update bounding box
        min_x, max_x = min(min_x, ent1_x, ent2_x), max(max_x, ent1_x, ent2_x)
        min_y, max_y = min(min_y, ent1_y, ent2_y), max(max_y, ent1_y, ent2_y)
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "quantum interference waveform")


if __name__ == "__main__":
    quantum_interference_waveform()