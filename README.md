# Python Design — Nirmana Generator

## Peraturan Project

### Format Output
- Rasio: 1:1 (Persegi)
- Resolusi: 4000 x 4000 px
- DPI: 300
- Format: JPG + SVG + EPS
- Suffix tanggal otomatis: ` DDMMYYYY` (contoh: ` 12092026`)

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
├── halloween/
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
- Format: `abstract [deskripsi_pola] [elemen] [gaya] [warna] [kegunaan].py`
- Contoh: `abstract parallel lines random thickness pattern black white texture.py`
- Output: `abstract parallel lines random thickness pattern black white texture 12092026.jpg`

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
python "abstract parallel lines random thickness pattern black white texture.py"
```

### Gallery
Buka `gallery.html` di browser → klik "Open Folder" → pilih folder project ini.

Gallery membaca JPG dari:
- `output/jpg` → **Draft**
- `submitted/jpg` → **Submitted**
- `trash/jpg` → **Trash**