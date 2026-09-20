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


def grow_cell(cx, cy, generation, max_generations, parent_angle=None):
    """Simulasi pertumbuhan sel biomorfik."""
    cells = []
    
    # Ukuran sel berdasarkan generasi
    cell_size = 2.0 + 1.5 * (max_generations - generation)
    
    # Bentuk sel (tidak sempurna, organik)
    n_points = 12 + generation * 2
    theta = np.linspace(0, 2 * np.pi, n_points)
    
    # Variasi bentuk organik
    radius_variation = np.random.uniform(0.8, 1.2, n_points)
    modulated_radius = cell_size * radius_variation
    
    x_cell = cx + modulated_radius * np.cos(theta)
    y_cell = cy + modulated_radius * np.sin(theta)
    
    cells.append((x_cell, y_cell, cx, cy, cell_size, generation))
    
    # Pembelahan sel (mitosis)
    if generation < max_generations:
        # Arah pembelahan
        if parent_angle is None:
            mitosis_angle = np.random.uniform(0, 2 * np.pi)
        else:
            mitosis_angle = parent_angle + np.random.uniform(-np.pi/4, np.pi/4)
        
        # Posisi sel anak
        child_distance = cell_size * 2.5
        
        for i in range(2):  # Dua sel anak
            child_angle = mitosis_angle + i * np.pi
            child_cx = cx + child_distance * np.cos(child_angle)
            child_cy = cy + child_distance * np.sin(child_angle)
            
            # Pertumbuhan rekursif
            child_cells = grow_cell(child_cx, child_cy, generation + 1, 
                                   max_generations, child_angle)
            cells.extend(child_cells)
    
    return cells


def biomorphic_cellular_growth():
    """Pola pertumbuhan sel biomorfik dengan pembelahan mitosis dan diferensiasi."""
    fig, ax = setup_ax()
    
    center_x, center_y = 50, 50
    
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    
    # Layer 1: Sel induk (stem cells)
    n_stem_cells = 5
    stem_cells = []
    
    for i in range(n_stem_cells):
        angle = i * 2 * np.pi / n_stem_cells
        distance = 8
        stem_x = center_x + distance * np.cos(angle)
        stem_y = center_y + distance * np.sin(angle)
        
        # Sel induk (besar, kompleks)
        stem_size = 4.0
        n_stem_points = 20
        theta_stem = np.linspace(0, 2 * np.pi, n_stem_points)
        
        # Bentuk tidak beraturan organik
        stem_modulation = 1 + 0.3 * np.sin(5 * theta_stem + i)
        x_stem = stem_x + stem_size * stem_modulation * np.cos(theta_stem)
        y_stem = stem_y + stem_size * stem_modulation * np.sin(theta_stem)
        
        ax.plot(x_stem, y_stem, color="black", linewidth=1.5, alpha=0.9)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_stem.min()), max(max_x, x_stem.max())
        min_y, max_y = min(min_y, y_stem.min()), max(max_y, y_stem.max())
        
        # Nukleus (inti sel)
        nucleus_size = stem_size * 0.4
        x_nucleus = stem_x + nucleus_size * np.cos(theta_stem)
        y_nucleus = stem_y + nucleus_size * np.sin(theta_stem)
        
        ax.plot(x_nucleus, y_nucleus, color="black", linewidth=0.8, alpha=0.7)
        
        stem_cells.append((stem_x, stem_y, stem_size))
    
    # Layer 2: Pertumbuhan sel diferensiasi
    all_cells = []
    
    for stem_x, stem_y, stem_size in stem_cells:
        # Pertumbuhan dari sel induk
        max_generations = 4
        cells_from_stem = grow_cell(stem_x, stem_y, 0, max_generations)
        all_cells.extend(cells_from_stem)
    
    # Gambar semua sel
    for x_cell, y_cell, cx, cy, cell_size, generation in all_cells:
        # Ketebalan berdasarkan generasi (sel lebih tua lebih tebal)
        lw = 0.6 + 0.4 * (max_generations - generation) / max_generations
        alpha = 0.5 + 0.3 * (max_generations - generation) / max_generations
        
        ax.plot(x_cell, y_cell, color="black", linewidth=lw, alpha=alpha)
        
        # Update bounding box
        min_x, max_x = min(min_x, x_cell.min()), max(max_x, x_cell.max())
        min_y, max_y = min(min_y, y_cell.min()), max(max_y, y_cell.max())
        
        # Organel dalam sel (berdasarkan jenis sel)
        if generation % 3 == 0:
            # Mitokondria (organel energi)
            n_mito = 3
            for m in range(n_mito):
                mito_angle = m * 2 * np.pi / n_mito
                mito_distance = cell_size * 0.6
                mito_x = cx + mito_distance * np.cos(mito_angle)
                mito_y = cy + mito_distance * np.sin(mito_angle)
                
                # Bentuk mitokondria (lonjong)
                mito_size = cell_size * 0.2
                mito_points = 8
                theta_mito = np.linspace(0, 2 * np.pi, mito_points)
                
                x_mito = mito_x + mito_size * (1 + 0.3 * np.cos(2*theta_mito)) * np.cos(theta_mito)
                y_mito = mito_y + mito_size * (1 + 0.3 * np.cos(2*theta_mito)) * np.sin(theta_mito)
                
                ax.plot(x_mito, y_mito, color="black", linewidth=0.3, alpha=0.6)
        
        if generation % 4 == 1:
            # Retikulum endoplasma
            n_er = 4
            for e in range(n_er):
                er_angle = e * 2 * np.pi / n_er
                er_distance = cell_size * 0.4
                er_x = cx + er_distance * np.cos(er_angle)
                er_y = cy + er_distance * np.sin(er_angle)
                
                # Bentuk retikulum (berliku-liku)
                er_size = cell_size * 0.15
                er_points = 20
                theta_er = np.linspace(0, 2 * np.pi, er_points)
                
                # Modulasi untuk bentuk berliku
                er_mod = 1 + 0.2 * np.sin(8 * theta_er)
                x_er = er_x + er_size * er_mod * np.cos(theta_er)
                y_er = er_y + er_size * er_mod * np.sin(theta_er)
                
                ax.plot(x_er, y_er, color="black", linewidth=0.2, alpha=0.5, linestyle="--")
    
    # Layer 3: Jaringan penghubung (extracellular matrix)
    n_connections = 80
    
    for _ in range(n_connections):
        # Pilih dua sel acak untuk dihubungkan
        if len(all_cells) < 2:
            continue
            
        idx1, idx2 = np.random.choice(len(all_cells), 2, replace=False)
        cell1 = all_cells[idx1]
        cell2 = all_cells[idx2]
        
        cx1, cy1 = cell1[2], cell1[3]
        cx2, cy2 = cell2[2], cell2[3]
        
        # Jarak antara sel
        distance = np.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2)
        
        # Hanya hubungkan sel yang cukup dekat
        if distance < 25:
            # Garis penghubung dengan pola organik
            n_connect_points = 15
            t_connect = np.linspace(0, 1, n_connect_points)
            
            # Kurva dengan variasi sinusoidal
            wave_freq = np.random.uniform(2, 5)
            wave_amp = np.random.uniform(0.5, 2.0)
            
            connect_x = []
            connect_y = []
            
            for t in t_connect:
                # Posisi linear
                base_x = cx1 + (cx2 - cx1) * t
                base_y = cy1 + (cy2 - cy1) * t
                
                # Offset sinusoidal
                perp_x = (cy2 - cy1) / distance
                perp_y = -(cx2 - cx1) / distance
                
                wave = wave_amp * np.sin(wave_freq * t * np.pi)
                
                connect_x.append(base_x + perp_x * wave)
                connect_y.append(base_y + perp_y * wave)
            
            ax.plot(connect_x, connect_y, color="black", linewidth=0.3, alpha=0.4)
    
    # Layer 4: Pembelahan mitosis aktif
    n_active_mitosis = 6
    
    for i in range(n_active_mitosis):
        mitosis_angle = i * 2 * np.pi / n_active_mitosis
        mitosis_radius = 30
        mitosis_x = center_x + mitosis_radius * np.cos(mitosis_angle)
        mitosis_y = center_y + mitosis_radius * np.sin(mitosis_angle)
        
        # Sel yang sedang membelah
        parent_size = 3.0
        n_parent_points = 16
        theta_parent = np.linspace(0, 2 * np.pi, n_parent_points)
        
        # Bentuk sel yang memanjang sebelum pembelahan
        elongation = 1 + 0.5 * np.cos(2 * theta_parent)
        x_parent = mitosis_x + parent_size * elongation * np.cos(theta_parent + mitosis_angle)
        y_parent = mitosis_y + parent_size * elongation * np.sin(theta_parent + mitosis_angle)
        
        ax.plot(x_parent, y_parent, color="black", linewidth=1.0, alpha=0.8)
        
        # Garis pembelahan
        cleavage_length = parent_size * 1.8
        cleavage_x = [mitosis_x - cleavage_length * np.cos(mitosis_angle),
                     mitosis_x + cleavage_length * np.cos(mitosis_angle)]
        cleavage_y = [mitosis_y - cleavage_length * np.sin(mitosis_angle),
                     mitosis_y + cleavage_length * np.sin(mitosis_angle)]
        
        ax.plot(cleavage_x, cleavage_y, color="black", linewidth=0.6, alpha=0.7, linestyle=":")
        
        # Sel anak yang baru terbentuk
        for child in range(2):
            child_angle = mitosis_angle + child * np.pi
            child_distance = parent_size * 1.2
            child_x = mitosis_x + child_distance * np.cos(child_angle)
            child_y = mitosis_y + child_distance * np.sin(child_angle)
            
            child_size = parent_size * 0.6
            n_child_points = 12
            theta_child = np.linspace(0, 2 * np.pi, n_child_points)
            
            x_child = child_x + child_size * np.cos(theta_child)
            y_child = child_y + child_size * np.sin(theta_child)
            
            ax.plot(x_child, y_child, color="black", linewidth=0.5, alpha=0.6)
            
            # Update bounding box
            min_x, max_x = min(min_x, x_child.min()), max(max_x, x_child.max())
            min_y, max_y = min(min_y, y_child.min()), max(max_y, y_child.max())
    
    # Layer 5: Apoptosis (kematian sel terprogram)
    n_apoptosis = 4
    
    for i in range(n_apoptosis):
        apo_angle = i * 2 * np.pi / n_apoptosis + np.pi/4
        apo_radius = 35
        apo_x = center_x + apo_radius * np.cos(apo_angle)
        apo_y = center_y + apo_radius * np.sin(apo_angle)
        
        # Sel yang mengalami apoptosis
        apo_size = 2.5
        n_apo_points = 20
        theta_apo = np.linspace(0, 2 * np.pi, n_apo_points)
        
        # Bentuk tidak beraturan (sel sekarat)
        apo_modulation = 1 + 0.4 * np.random.uniform(-1, 1, n_apo_points)
        x_apo = apo_x + apo_size * apo_modulation * np.cos(theta_apo)
        y_apo = apo_y + apo_size * apo_modulation * np.sin(theta_apo)
        
        ax.plot(x_apo, y_apo, color="black", linewidth=0.7, alpha=0.6, linestyle="--")
        
        # Fragmen sel (apoptotic bodies)
        n_fragments = 5
        for f in range(n_fragments):
            frag_angle = apo_angle + f * 2 * np.pi / n_fragments
            frag_distance = apo_size * 1.5
            frag_x = apo_x + frag_distance * np.cos(frag_angle)
            frag_y = apo_y + frag_distance * np.sin(frag_angle)
            
            frag_size = apo_size * 0.3
            n_frag_points = 8
            theta_frag = np.linspace(0, 2 * np.pi, n_frag_points)
            
            x_frag = frag_x + frag_size * np.cos(theta_frag)
            y_frag = frag_y + frag_size * np.sin(theta_frag)
            
            ax.plot(x_frag, y_frag, color="black", linewidth=0.3, alpha=0.4)
            
            # Update bounding box
            min_x, max_x = min(min_x, x_frag.min()), max(max_x, x_frag.max())
            min_y, max_y = min(min_y, y_frag.min()), max(max_y, y_frag.max())
    
    # Framing dinamis
    cx_final = (min_x + max_x) / 2.0
    cy_final = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    pad = max(w, h) / 2.0 + 3.0
    
    ax.set_xlim(cx_final - pad, cx_final + pad)
    ax.set_ylim(cy_final - pad, cy_final + pad)
    
    save(fig, "biomorphic cellular growth")


if __name__ == "__main__":
    biomorphic_cellular_growth()