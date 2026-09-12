# Python Design — Nirmana Generator

## Peraturan Project

### Format Output
- Rasio: 1:1 (Persegi)
- Resolusi: 4000 x 4000 px
- DPI: 300
- Format: PNG + SVG

### Struktur Folder
```
python-design/
├── parallel/
│   ├── parallel_random.py
│   ├── parallel_gradient.py
│   └── output/png/ & svg/
├── waves/
│   ├── zigzag_wave.py
│   └── output/png/ & svg/
├── radial/
├── grid/
├── contour/
├── spiral/
├── optical/
├── geometric/
├── organic/
├── dynamic/
├── gallery.html
└── README.md
```

### Cara Tambah Variasi Baru
1. Masuk folder kategori (misal `parallel/`)
2. Buat file .py baru dengan nama variasi
3. Jalankan script
4. Output otomatis masuk ke `output/png/` dan `output/svg/`

### Penamaan File
- Gunakan bahasa Inggris
- Format: `[kategori]_[variasi]`
- Contoh: `parallel_random.py`, `zigzag_wave.py`
- Hindari spasi, gunakan underscore (`_`)

### Prasyarat
- Python 3.x
- Matplotlib
- NumPy

### Instalasi
```bash
pip install matplotlib numpy
```

### Menjalankan
```bash
cd parallel
python parallel_random.py
```

### Gallery
Buka `gallery.html` di browser, klik "Open Folder", pilih folder project ini.

### Lisensi
- Hasil generate dapat dijual di platform mikrostok
- Wajib disclosure sebagai AI/code-generated content
- Untuk penggunaan pribadi dan komersial
