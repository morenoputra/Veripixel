# VeriPixel — Deteksi Gambar Real vs AI-Generated

Aplikasi web Flask untuk skripsi deteksi citra AI-generated menggunakan
EfficientNet-B0 (transfer learning) dan visualisasi Grad-CAM, dengan riwayat
deteksi tersimpan di SQLite.

## Struktur Proyek

```
veripixel/
├── app.py                 # Routing Flask (upload, hasil, history)
├── inference.py            # Load model + prediksi + Grad-CAM
├── db.py                   # Akses database SQLite (riwayat deteksi)
├── requirements.txt
├── model/
│   └── model_efficientnet_b0.pth   # <-- taruh file bobot hasil training di sini
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── fonts.css        # @font-face lokal (Space Grotesk, Inter, JetBrains Mono)
│   ├── js/main.js
│   ├── vendor/
│   │   ├── bootstrap/       # Bootstrap 5.3.3 CSS+JS (di-bundle lokal, tidak pakai CDN)
│   │   └── fonts/           # file .woff2
│   ├── images/
│   │   ├── logo-icon.png    # ikon logo (navbar, hero scan card)
│   │   └── logo-full.png    # logo lengkap + wordmark (empty state)
│   └── uploads/             # gambar asli & heatmap tersimpan otomatis di sini
└── templates/
    └── index.html
```

> **Catatan:** Bootstrap dan seluruh font di-bundle langsung di dalam proyek (bukan lewat CDN),
> jadi aplikasi tetap tampil normal walau dijalankan tanpa koneksi internet — cocok untuk demo
> saat sidang di kampus dengan jaringan yang tidak stabil.

## 1. Instalasi

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> Jika komputer tidak memiliki GPU, `torch` akan otomatis berjalan di CPU
> (lebih lambat, tapi tetap berfungsi untuk keperluan demo skripsi).

## 2. Menyiapkan Model

Salin file bobot hasil training (`model_efficientnet_b0.pth`, hasil dari
notebook `Skripsi_Training_EfficientNet_*.ipynb`) ke folder `model/`.

Struktur arsitektur di `inference.py` **harus identik** dengan yang dipakai
saat training (EfficientNet-B0 + `classifier[1] = nn.Linear(in_features, 1)`),
supaya `load_state_dict()` tidak error.

## 3. Menjalankan Aplikasi

```bash
python app.py
```

Buka `http://127.0.0.1:5000` di browser.

## 4. Cara Kerja Singkat

1. Pengguna mengunggah gambar (JPG/JPEG/PNG, maks. 20MB) di bagian **Deteksi**.
2. `inference.py` melakukan preprocessing (resize 224×224, normalisasi ImageNet),
   menjalankan model, dan menghitung Grad-CAM dari layer konvolusi terakhir
   (`model.features[-1]`).
3. Gambar asli & heatmap disimpan ke `static/uploads/`, hasil (label,
   confidence, nama file) disimpan ke tabel `detections` di `veripixel.db`.
4. Halaman menampilkan hasil terbaru di bagian **Hasil**, dan seluruh riwayat
   di bagian **History** (bisa dihapus per-item atau semuanya).

## 5. Dokumentasi Pengujian

Untuk dokumen pengujian black box aplikasi, lihat [black-box-testing.md](black-box-testing.md).

## 6. Kustomisasi

- **Ganti warna/tema**: ubah variabel CSS di `static/css/style.css` bagian `:root`.
- **Threshold klasifikasi**: default 0.5 pada `inference.py` (`prob_real >= 0.5`).
- **Ukuran maksimal upload**: `MAX_CONTENT_LENGTH` di `app.py`.
- **Lokasi database**: `DB_PATH` di `db.py` (default: `veripixel.db` di root proyek).

# Veripixel
