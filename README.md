# SPACE-BOOK

**Smart Reservation and Booking Management System** untuk lapangan olahraga dan coworking space.

Final Project Mata Kuliah **Dasar Pemrograman**
Dosen Pengampu: Dr. Ir. Chaerur Rozikin, S.Kom., M.Kom

- Nama :
-        Ghifari Ahmad
-        Hilman
-        Keisya
- NIM :
-       2610631140162
-       2610631140140
-       2610631140147
- Kelas : E

## Deskripsi

SPACE-BOOK adalah aplikasi berbasis terminal (CLI) untuk mengelola pemesanan fasilitas secara digital. Aplikasi ini menggantikan pencatatan manual lewat buku atau WhatsApp yang sering menimbulkan jadwal bentrok, slot sulit dilacak, dan riwayat booking tidak terdokumentasi.

## Teknologi

- Python 3
- SQLite (modul bawaan `sqlite3`)
- Git dan GitHub

## Fasilitas

| ID | Nama Fasilitas | Jenis | Harga/Jam |
|----|----------------------|-----------|------------|
| 1 | Lapangan Futsal A | Olahraga | Rp 150.000 |
| 2 | Lapangan Badminton B | Olahraga | Rp 60.000 |
| 3 | Ruang Meeting Alpha | Coworking | Rp 100.000 |
| 4 | Ruang Meeting Beta | Coworking | Rp 100.000 |

Jam operasional: **08.00 - 22.00**. Durasi booking minimal **1 jam**.

## Fitur

### Sudah selesai

- Registrasi dan login (validasi nomor HP minimal 10 digit, password minimal 6 karakter)
- Login berdasarkan peran (user dan admin)
- Lihat fasilitas
- Kelola fasilitas oleh admin (tambah, ubah, hapus)
- Cek ketersediaan jadwal beserta tampilan jadwal harian (KOSONG / BOOKED)
- Validasi bentrok jadwal
- Rekomendasi slot kosong jika jadwal bentrok
- Booking fasilitas dengan kode booking (contoh: BK0001) dan status awal `MENUNGGU PEMBAYARAN`

### Dalam pengerjaan

- Riwayat booking
- Simulasi pembayaran (Transfer Bank dan Bayar di Tempat)
- Lihat booking, validasi pembayaran, dan pembatalan booking oleh admin
- Laporan penggunaan

## Cara Menjalankan

1. Pastikan Python 3 sudah terpasang.
2. Clone repository ini:
   ```
   git clone https://github.com/ghifariahmad2401-create/space-book.git
   cd space-book
   ```
3. Jalankan program:
   ```
   python main.py
   ```
4. Database `space_book.db` akan dibuat otomatis saat program pertama kali dijalankan.

## Akun Admin Default

| Username | Password |
|----------|----------|
| Budi Santoso | 123456|

Akun user dibuat lewat menu **Registrasi**.

## Alur Status Booking

```
MENUNGGU PEMBAYARAN -> MENUNGGU VERIFIKASI -> LUNAS -> SELESAI
MENUNGGU PEMBAYARAN -> DIBATALKAN
```

## Struktur Database

- **user**: id, nama, no_hp, username, password, role
- **fasilitas**: id, nama_fasilitas, jenis, harga_per_jam
- **booking**: id, id_fasilitas, id_user, tanggal, jam_mulai, jam_selesai, status_booking, status_bayar, nama_penyewa, no_hp, catatan
- **pembayaran**: id, id_booking, metode, referensi, tanggal_bayar

## Struktur Project

```
space-book/
├── main.py          # S
