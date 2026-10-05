# Black Box Testing - VeriPixel

Dokumen ini berisi rancangan pengujian black box untuk aplikasi web VeriPixel berdasarkan fungsionalitas yang terlihat dari sisi pengguna.

## 1. Tujuan Pengujian

Menguji apakah aplikasi dapat menerima input pengguna, memproses gambar, menampilkan hasil deteksi, serta mengelola riwayat deteksi sesuai yang diharapkan.

## 2. Ruang Lingkup

Pengujian mencakup fitur-fitur berikut:
- Halaman utama aplikasi
- Upload gambar
- Deteksi gambar real vs AI-generated
- Tampilan hasil deteksi
- Riwayat deteksi
- Hapus satu item riwayat
- Bersihkan seluruh riwayat

## 3. Prasyarat

Sebelum pengujian, pastikan:
- Aplikasi berjalan dengan benar di browser
- File model yang dibutuhkan tersedia
- Tersedia contoh gambar dengan format JPG/JPEG/PNG
- Browser mendukung upload file dan drag & drop

## 4. Test Case

| ID | Scenario | Langkah Uji | Hasil Yang Diharapkan |
|---|---|---|---|
| TC-01 | Membuka halaman utama | Buka URL aplikasi di browser | Halaman utama tampil dengan judul VeriPixel, bagian Deteksi, Hasil, History, dan tombol upload |
| TC-02 | Upload gambar valid JPG | Pilih file gambar berformat JPG lalu klik tombol upload | Aplikasi memproses gambar, menampilkan label hasil deteksi, confidence, gambar asli, dan heatmap Grad-CAM |
| TC-03 | Upload gambar valid PNG | Pilih file gambar berformat PNG lalu klik tombol upload | Aplikasi menerima file, memproses dengan sukses, dan menampilkan hasil deteksi |
| TC-04 | Upload gambar valid JPEG | Pilih file gambar berformat JPEG lalu klik tombol upload | Aplikasi menerima file, memproses dengan sukses, dan menampilkan hasil deteksi |
| TC-05 | Upload file kosong | Klik tombol upload tanpa memilih file | Aplikasi menolak proses dan menampilkan pesan "Silakan pilih file gambar terlebih dahulu." |
| TC-06 | Upload format tidak didukung | Pilih file dengan format selain JPG/JPEG/PNG, misalnya GIF | Aplikasi menolak proses dan menampilkan pesan bahwa format file tidak didukung |
| TC-07 | Upload file melebihi batas ukuran | Pilih file berukuran > 20 MB | Aplikasi menolak upload dan menampilkan pesan/penolakan terkait batas ukuran file |
| TC-08 | Drag and drop file | Seret gambar valid ke area dropzone | Nama file muncul di area upload, lalu proses deteksi berjalan saat form dikirim |
| TC-09 | Menampilkan hasil deteksi | Setelah upload berhasil | Bagian Hasil menampilkan label, skor confidence, gambar asli, dan visualisasi Grad-CAM |
| TC-10 | Menyimpan riwayat deteksi | Lakukan beberapa kali upload gambar valid | Setiap deteksi berhasil muncul di bagian History dengan identitas deteksi, label, confidence, dan timestamp |
| TC-11 | Menghapus satu riwayat deteksi | Klik tombol hapus pada salah satu item History | Item yang dipilih hilang dari History dan tidak muncul lagi di daftar |
| TC-12 | Membersihkan seluruh riwayat | Klik tombol hapus semua History | Semua item History terhapus dan halaman menampilkan status kosong |
| TC-13 | Mengakses ulang halaman setelah history dihapus | Setelah history dibersihkan, refresh halaman | Aplikasi tetap berjalan normal dan tidak menampilkan data history yang lama |
| TC-14 | Mengupload gambar dengan nama file yang panjang | Pilih gambar dengan nama file panjang | Aplikasi tetap bisa memproses, dan nama file tampil sesuai yang diupload |
| TC-15 | Mengulang proses deteksi berkali-kali | Upload beberapa gambar secara berurutan | Setiap upload menghasilkan hasil terbaru yang tampil di bagian Hasil, dan riwayat bertambah sesuai order waktu |

## 5. Catatan Tambahan

- Pengujian ini fokus pada perilaku aplikasi dari sisi pengguna, sehingga tidak memerlukan pemahaman detail implementasi internal.
- Jika ingin, pengujian ini bisa dikembangkan menjadi format Excel, CSV, atau test script otomatis (misalnya Selenium/Playwright).
