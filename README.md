# Bogor Travel — Sistem Rekomendasi Tempat Wisata

Proyek ini adalah aplikasi rekomendasi tempat wisata di Bogor yang dikemas sebagai aplikasi web (Flask) dan dilengkapi notebook untuk model deep learning (autoencoder). Aplikasi menyediakan antarmuka sederhana untuk menguji rekomendasi berbasis kemiripan konten (similarity matrix) serta filter jarak (radius) dari tempat sumber.

---

## Isi repository (ringkasan hasil analisa)
- DL_Recommendation_System_Autoencoder_Bogor.ipynb  
  Notebook Jupyter yang berisi eksperimen model rekomendasi (autoencoder / deep learning), preprocessing, dan pembuatan matriks similaritas / model. Ini adalah sumber eksperimen dan dokumentasi analitik.
- app.py  
  Aplikasi Flask utama. Memuat dataset, memuat `similarity_matrix.npy`, menyediakan halaman web dan endpoint API untuk melakukan rekomendasi. Logika utama:
  - Rute web: `/`, `/model`, `/recommender`, `/author`
  - API: `POST /api/recommend` menerima JSON dan mengembalikan rekomendasi
- df_wisata_bogor_final_prepared.csv  
  Dataset tempat wisata Bogor (data final yang sudah diprepare). Dipakai oleh app untuk menampilkan metadata dan lokasi.
- similarity_matrix.npy  
  Matriks similaritas antara tempat (precomputed). Digunakan untuk memilih tempat yang mirip secara konten.
- preprocessor.pkl  
  Artefak preprocessing (pickle). Digunakan kemungkinan di notebook dan/atau pipeline preprocessing.
- requirements.txt  
  Daftar dependensi minimal yang dibutuhkan untuk menjalankan aplikasi.
- templates/ (direktori)  
  Folder halaman HTML (template Jinja2) yang digunakan Flask. (Isi folder tidak ditampilkan dalam ringkasan; pastikan direktori ini berisi `index.html`, `recommender.html`, dll.)
- static/ (direktori)  
  Asset statis (CSS/JS/gambar) untuk aplikasi web. (Isi folder tidak ditampilkan dalam ringkasan.)

Catatan ukuran berkas penting:
- similarity_matrix.npy — file biner matriks (~7 MB)
- df_wisata_bogor_final_prepared.csv — dataset (~650 KB)

---

## Fitur utama
- Rekomendasi tempat wisata berdasarkan matriks similaritas + filter jarak (haversine).
- Antarmuka web untuk memilih tempat sumber dan menampilkan rekomendasi.
- Endpoint API JSON untuk integrasi / pengujian otomatis.
- Notebook eksperimen model (autoencoder) untuk membangun atau memperbarui matriks similaritas.

---

## Prasyarat
- Python 3.8+ direkomendasikan
- Sistem operasi: Linux / macOS / Windows
- Pastikan file-file berikut berada di root project (atau di path yang sama dengan app.py):
  - df_wisata_bogor_final_prepared.csv
  - similarity_matrix.npy
  - preprocessor.pkl (jika notebook / bagian pipeline membutuhkan)

---

## Instalasi & Menjalankan (lokal)
1. Clone repository:
   git clone https://github.com/mariouskono/bogor-travel.git
2. Masuk direktori:
   cd bogor-travel
3. Buat virtualenv dan aktifkan (opsional tetapi direkomendasikan):
   python -m venv venv
   - macOS / Linux: source venv/bin/activate
   - Windows: venv\Scripts\activate
4. Install dependensi:
   pip install -r requirements.txt
   (Jika ada paket tambahan yang diperlukan oleh notebook, pasang sesuai kebutuhan, mis. jupyter, tensorflow/keras, scikit-learn)
5. Jalankan aplikasi Flask:
   python app.py
6. Buka browser dan akses:
   http://127.0.0.1:5000/

Jika Flask berjalan di mode debug (default pada `app.py`), server akan otomatis reload saat ada perubahan.

---

## Penggunaan API
Endpoint: POST /api/recommend  
Content-Type: application/json

Body JSON:
{
  "place": "Nama Tempat Sumber",
  "top_n": 5,           // opsional, default 5
  "radius": 50          // jarak maksimum (km), opsional, default 100
}

Contoh request (curl):
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"place": "Kebun Raya Bogor", "top_n": 5, "radius": 20}'

Respons (contoh, JSON):
{
  "source": {"nama": "Kebun Raya Bogor", "lat": -6.594, "lon": 106.799},
  "recommendations": [
    {
      "nama": "Istana Bogor",
      "kategori": "...",
      "rating": 4.5,
      "jumlah_rating": 123,
      "kecamatan": "...",
      "kabupaten_kota": "...",
      "lat": -6.597,
      "lon": 106.800,
      "sim": "92.3%",
      "dist": "0.45 km",
      "image": "https://...",
      "gmaps": "https://maps.google.com/..."
    },
    ...
  ]
}

Perilaku penting:
- API memeriksa apakah tempat sumber ada di dataset. Jika tidak ditemukan, akan mengembalikan error 404.
- Jarak dihitung dengan rumus haversine dan hasil difilter dengan `radius`.
- Nilai NaN untuk gambar atau district akan digantikan placeholder/default.

---

## Tentang model / notebook
Notebook `DL_Recommendation_System_Autoencoder_Bogor.ipynb` berisi langkah-langkah untuk:
- Preprocessing text/fitur
- Membangun autoencoder untuk embedding/representasi
- Menghitung matriks similaritas antar tempat
- Menyimpan artefak (mis. `similarity_matrix.npy`, `preprocessor.pkl`)

Jika ingin memperbarui matriks similaritas, jalankan notebook (atau skrip yang relevan) dan simpan kembali file `similarity_matrix.npy` yang baru.

---

## Troubleshooting singkat
- Error loading data saat menjalankan app.py:
  - Pastikan file CSV dan .npy berada di direktori kerja yang sama dengan `app.py`.
  - Periksa permission file.
- Jika server Flask tidak jalan karena dependensi:
  - Periksa `requirements.txt`. Tambahkan paket yang diperlukan (notebook mungkin butuh lebih banyak paket seperti tensorflow/keras).
- Jika template HTML tidak ditemukan:
  - Pastikan folder `templates/` ada dan berisi file HTML yang diperlukan (`index.html`, `recommender.html`, dll).

---

## Kontribusi & Lisensi
- Jika ingin berkontribusi, buka issue / pull request di repository.
- Tidak ada file LICENSE di repository — tambahkan lisensi yang sesuai jika ingin membuka proyek untuk publik.

---

## Kontak / Kredit
- Author: (informasi author dapat dilihat di halaman `/author` aplikasi)
- Repository: https://github.com/mariouskono/bogor-travel

---
