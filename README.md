# Python Design — Nirmana Generator

## Peraturan Project

### Format Output
- Rasio: 1:1 (Persegi)
- Resolusi: 4000 x 4000 px
- DPI: 300
- Format: JPG + SVG
- Suffix tanggal otomatis: `_DDMMYYYY` (contoh: `_12092026`)

### Struktur Folder
```
python-design/
├── parallel/
│   ├── code/
│   │   └── abstract_parallel_lines_*.py
│   └── output/
│       ├── jpg/
│       └── svg/
├── waves/
│   ├── code/
│   └── output/
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
1. Masuk folder kategori → `code/` (misal `parallel/code/`)
2. Buat file .py baru dengan nama full keyword mikrostok
3. Jalankan script dari folder `code/`
4. Output otomatis masuk ke `../output/jpg/` dan `../output/svg/`
5. Tanggal otomatis ditambahkan ke nama file output

### Penamaan File
- Format: `abstract_[deskripsi_pola]_[elemen]_[gaya]_[warna]_[kegunaan].py`
- Contoh: `abstract_parallel_lines_random_thickness_pattern_black_white_texture.py`
- Output: `abstract_parallel_lines_random_thickness_pattern_black_white_texture_12092026.jpg`

### Keyword Wajib
- `abstract` — deskripsi gaya
- `pattern` — tipe file
- `black_white` — warna
- `texture` — kegunaan

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
cd parallel/code
python abstract_parallel_lines_random_thickness_pattern_black_white_texture.py
```

### Gallery
Buka `gallery.html` di browser → klik "Open Folder" → pilih folder project ini.

### Lisensi
- Hasil generate dapat dijual di platform mikrostok
- Wajib disclosure sebagai AI/code-generated content
- Untuk penggunaan pribadi dan komersial
