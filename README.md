# Python Design — Nirmana Generator

Generative art menggunakan Python untuk stock vector dan stock video.

---

## Struktur Project

```
python-design/
├── vector/                    # Semua kategori desain vektor
│   ├── concentric/
│   ├── contour/
│   ├── dynamic/
│   ├── flow/
│   ├── fractal/
│   ├── geometric/
│   ├── grid/
│   ├── halloween/
│   ├── opart/
│   ├── optical/
│   ├── organic/
│   ├── parallel/
│   ├── radial/
│   ├── sound/
│   ├── spiral/
│   ├── topological/
│   └── waves/
├── video/                     # Animated pattern untuk stock video
│   └── concentric/
├── task/                      # Catatan dan rencana kerja
│   ├── vector.md
│   └── video.md
├── metadata/                  # Keyword dan metadata mikrostok
├── gallery.html
└── README.md
```

---

## Struktur Setiap Kategori Vector

```
vector/<category>/
├── code/          # script generator (.py)
├── output/        # draft hasil render (tidak di-commit)
│   ├── jpg/
│   ├── svg/
│   └── eps/
├── submitted/     # sudah disubmit ke mikrostok (tidak di-commit)
│   ├── jpg/
│   ├── svg/
│   └── eps/
└── trash/         # versi yang dibuang
```

---

## Struktur Setiap Kategori Video

```
video/<category>/
├── code/          # script generator (.py)
├── output/        # hasil render MP4 (tidak di-commit)
│   ├── vertical/     # 2160×3840  9:16
│   ├── landscape/    # 3840×2160  16:9
│   └── square/       # 2160×2160  1:1
├── submitted/     # sudah disubmit (tidak di-commit)
│   ├── vertical/
│   ├── landscape/
│   └── square/
└── trash/
```

---

## Format Output Vector

| Spec | Value |
|------|-------|
| Rasio | 1:1 (persegi) |
| Resolusi | 4000 × 4000 px |
| DPI | 300 |
| Format | JPG + SVG + EPS |
| Suffix | ` DDMMYYYY` otomatis |

---

## Format Output Video

| Spec | Value |
|------|-------|
| Container | MP4 |
| Codec | H.264 (libx264) |
| FPS | 30 |
| Durasi | 10 detik |
| Audio | Tidak ada |
| CRF | 18 |
| Priority | Vertical 9:16 → Landscape 16:9 → Square 1:1 |

---

## Alur Kerja

1. Script menulis hasil ke `output/` (draft).
2. Desain yang sudah disubmit dipindah ke `submitted/`.
3. Desain yang ditolak atau tidak dipakai dipindah ke `trash/`.

`output/` dan `submitted/` **tidak di-commit** (file terlalu besar).  
Folder `code/` dan `trash/` mengikuti git seperti biasa.

---

## Penamaan File

- Format: `abstract [deskripsi] [elemen] [style] [warna] [kegunaan].py`
- Contoh: `abstract parallel lines random thickness pattern black white texture.py`
- Output: `abstract parallel lines random thickness pattern black white texture 21092026.jpg`

---

## Prasyarat

```bash
pip install matplotlib numpy pillow
```

Untuk video, ffmpeg harus tersedia di PATH.

---

## Cara Menjalankan

**Vector:**
```bash
cd vector/parallel/code
python "abstract parallel lines random thickness pattern black white texture.py"
```

**Video:**
```bash
cd video/concentric/code
python anim_concentric_waves.py
```

---

## Gallery

Buka `gallery.html` di browser → klik "Open Folder" → pilih folder project ini.

Gallery membaca JPG dari subfolder `output/jpg`, `submitted/jpg`, dan `trash/jpg` di setiap kategori.
