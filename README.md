# Python Design — Nirmana Generator

## Peraturan Project

### Format Output
- Rasio: 1:1 (Persegi)
- Resolusi: 4000 x 4000 px
- DPI: 300
- Format: PNG + SVG

### Penamaan File
- Gunakan bahasa Inggris
- Format: `[deskripsi_utama]_[elemen_desain]_[gaya]_[variasi]`
- Contoh: `parallel_gradient_lines_pattern_abstract_texture`
- Hindari spasi, gunakan underscore (`_`)

### Struktur Folder
```
python-design/
├── batch_XX_[kategori].py
├── output/
│   └── batch_XX_[kategori]/
│       ├── png/
│       └── svg/
└── README.md
```

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
python batch_XX_[kategori].py
```

### Lisensi
- Hasil generate dapat dijual di platform mikrostok
- Wajib disclosure sebagai AI/code-generated content
- Untuk penggunaan pribadi dan komersial
