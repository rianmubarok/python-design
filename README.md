# Python Design — Nirmana Generator

## Peraturan Project

### Format Output
- Rasio: 1:1 (Persegi)
- Resolusi: 4000 x 4000 px
- DPI: 300
- Format: JPG + SVG + EPS
- Suffix tanggal otomatis: `_DDMMYYYY` (contoh: `_12092026`)

### Struktur Folder
Setiap kategori memakai struktur yang sama:

```
python-design/
├── parallel/
│   ├── code/          # script generator (.py)
│   ├── output/        # draft (belum disubmit)
│   │   ├── jpg/
│   │   ├── svg/
│   │   └── eps/
│   ├── submitted/     # sudah disubmit ke mikrostok
│   │   ├── jpg/
│   │   ├── svg/
│   │   └── eps/
│   └── trash/         # verisi yang dibuang
├── grid/
├── optical/
├── waves/
├── radial/
├── contour/
├── spiral/
├── geometric/
├── organic/
├── dynamic/
├── gallery.html
└── README.md
```

Kategori lain mengikuti pola yang sama (`code/`, `output/`, `submitted/`, dan `trash/` bila ada).

### Alur Kerja Folder
1. Script menulis hasil ke `output/` (draft).
2. Desain yang sudah disubmit dipindah ke `submitted/`.
3. Desain yang ditolak atau tidak dipakai dipindah ke `trash/`.

`output/` dan `submitted/` tidak di-commit (file terlalu besar). Folder `code/` dan `trash/` mengikuti aturan git yang ada.

### Cara Tambah Variasi Baru
1. Masuk folder kategori → `code/` (misal `parallel/code/`)
2. Buat file .py baru dengan nama full keyword mikrostok
3. Jalankan script dari folder `code/`
4. Output otomatis masuk ke `../output/jpg/`, `../output/svg/`, dan `../output/eps/`
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

Gallery membaca JPG dari:
- `output/jpg` → **Draft**
- `submitted/jpg` → **Submitted**
- `trash/jpg` → **Trash**