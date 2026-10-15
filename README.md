# Automated Log Analysis

Proyek sederhana untuk mensimulasikan log autentikasi dan mendeteksi aktivitas login mencurigakan secara otomatis menggunakan Python dan pandas.

Proyek ini terdiri dari dua bagian: **generator** yang membuat data log palsu (termasuk simulasi serangan), dan **analyzer** yang membaca log tersebut lalu melaporkan pola yang mencurigakan.

## Fitur

- **Generator log** (`generate_logs.py`)
  - Membuat 60 login normal dari jaringan internal (`192.168.1.x`)
  - Mensimulasikan serangan brute force: 15 percobaan gagal beruntun dari satu IP ke akun `hr_admin_01`
  - Mensimulasikan akun yang berhasil dibobol: satu login sukses dari IP penyerang setelah rangkaian gagal
  - Menyimpan hasilnya ke `auth_logs.csv`
- **Analyzer** (`analyze_logs.py`)
  - **Brute force**: banyak login gagal dari satu IP ke satu akun
  - **Password spraying**: satu IP gagal login ke banyak akun berbeda
  - **Kemungkinan akun terkompromi**: login sukses dari IP yang sama setelah rangkaian gagal, dalam jendela waktu tertentu

## Struktur Proyek

```
Automated Log Analysis/
├── generate_logs.py    # membuat data log simulasi
├── analyze_logs.py     # menganalisis log dan membuat laporan
├── requirements.txt    # dependensi Python
├── .gitignore
└── README.md
```

## Persyaratan

- Python 3.9 atau lebih baru
- pandas

## Cara Menjalankan

1. Clone repositori ini lalu masuk ke foldernya:

   ```bash
   git clone https://github.com/USERNAME/NAMA-REPO.git
   cd NAMA-REPO
   ```

2. Pasang dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Buat data log simulasi:

   ```bash
   python generate_logs.py
   ```

4. Jalankan analisis:

   ```bash
   python analyze_logs.py
   ```

> **Catatan:** `generate_logs.py` harus dijalankan lebih dulu, karena `analyze_logs.py` membaca file `auth_logs.csv` yang dihasilkannya.

## Format Data

File `auth_logs.csv` memiliki kolom berikut:

| Kolom | Keterangan |
|---|---|
| `timestamp` | Waktu kejadian (format ISO) |
| `user_id` | Nama akun yang dipakai untuk login |
| `source_ip` | Alamat IP asal login |
| `event_type` | Jenis event (`LOGIN`) |
| `user_agent` | Klien yang dipakai (browser atau script) |
| `location` | Lokasi asal login |
| `status` | `SUCCESS` atau `FAILED` |

## Cara Kerja Deteksi

| Deteksi | Logika | Parameter |
|---|---|---|
| Brute force | Menghitung login `FAILED` per pasangan `source_ip` + `user_id` | `THRESHOLD = 5` |
| Password spraying | Menghitung jumlah akun berbeda yang gagal login per `source_ip` | `THRESHOLD = 5` |
| Akun terkompromi | Mencari login `SUCCESS` dari IP dan akun yang sama setelah rangkaian gagal | `WINDOW = 10 menit` |

Nilai `THRESHOLD` dan `WINDOW` bisa diubah di bagian atas `analyze_logs.py` sesuai kebutuhan.

## Contoh Output

IP penyerang berbeda tiap kali generator dijalankan karena dibuat secara acak.

```
======================================
   SUSPICIOUS LOGIN ANALYSIS REPORT
======================================

[1] BRUTE FORCE DETECTION:
source_ip     user_id
203.0.113.38  hr_admin_01    15
dtype: int64

[1b] PASSWORD SPRAYING DETECTION:
No spraying detected.

[2] POSSIBLE ACCOUNT COMPROMISE:
             timestamp      user_id     source_ip event_type                             user_agent location   status
75 2026-08-20 08:54:30  hr_admin_01  203.0.113.38      LOGIN  Python-urllib/3.10 (Automated Script)  Unknown  SUCCESS
```

Penjelasan hasil:

- IP `203.0.113.38` gagal login 15 kali ke akun `hr_admin_01`, tanda brute force.
- Tidak ada password spraying, karena hanya satu akun yang diserang.
- Ada login sukses dari IP yang sama tepat setelah rangkaian gagal, dengan user agent berupa script otomatis. Ini pola khas akun yang berhasil dibobol.

## Keterbatasan

- Data sepenuhnya simulasi, bukan log sistem sungguhan.
- Deteksi brute force saat ini menghitung total kegagalan tanpa memperhatikan jendela waktu, sehingga serangan lambat dan login gagal yang tersebar berbulan-bulan bisa terhitung sama.
- Belum ada deteksi serangan terdistribusi (satu akun diserang dari banyak IP).

## Rencana Pengembangan

- [ ] Deteksi brute force dengan sliding window
- [ ] Simulasi serangan terdistribusi
- [ ] Deteksi impossible travel berdasarkan lokasi
- [ ] Ekspor laporan ke file (CSV atau HTML)
- [ ] Pengujian otomatis dengan pytest

## Catatan

Semua data pada proyek ini adalah simulasi. Rentang IP `203.0.113.0/24` adalah blok TEST-NET-3 yang disediakan khusus untuk dokumentasi dan contoh.
