# Xpense Insight
Personal Money Manager - Capstone M1

Aplikasi CLI untuk mencatat dan menganalisis keuangan pribadi.
Dibangun dengan Python dan MySQL, dengan fitur manajemen transaksi, statistik, dan visualisasi data.

---

## Fitur

- Tampilkan Tabel - Lihat data kategori dan transaksi
- Statistik - Ringkasan COUNT, SUM, AVG per flow dan kategori
- Visualisasi - Chart visualisasi data keuangan
- Tambah Data - Tambah transaksi dan kategori baru
- Hapus Data - Hapus transaksi dan kategori

---

## Struktur Project
```
m1-personal-money-manager/
    main.py                         <- entry point, jalankan program dari sini
    db/
        connection.py               <- koneksi ke database MySQL
    utils/
        input_helpers.py            <- validasi semua input user
        query_helpers.py            <- eksekusi query SQL (SELECT, INSERT, DELETE)
        formatters.py               <- format rupiah dan tampilan dataframe
    features/
        table.py                    <- Feature 1: tampilkan tabel kategori & transaksi
        statistic.py                <- Feature 2: statistik COUNT, SUM, AVG
        visualization.py            <- Feature 3: chart visualisasi data
        add_data.py                 <- Feature 4: tambah transaksi dan kategori
        delete_data.py              <- Feature 5: hapus transaksi dan kategori
    m1_capst_money_manager.sql      <- schema database + 100 data transaksi
    requirements.txt                <- daftar library yang dibutuhkan
    .env                            <- kredensial database (tidak di-push ke GitHub)
```

---

## Cara Menjalankan

### Prasyarat
- Python 3.11+
- MySQL Server aktif

### Step 1 - Clone Repository
```bash
git clone https://github.com/daffaalhanif/m1-personal-money-manager.git
cd m1-personal-money-manager
```

### Step 2 - Buat dan Aktifkan Virtual Environment
```bash
python -m venv .venv
```

Mac/Linux:
```bash
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

### Step 3 - Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 - Import Database ke MySQL
```bash
mysql -u root -p < m1_capst_money_manager.sql
```

Atau buka MySQL Workbench, lalu jalankan file `m1_capst_money_manager.sql` secara manual.

File ini otomatis membuat database `m1_capst_money_manager` beserta tabel dan 100 seed data transaksi.

### Step 5 - Buat File .env
Buat file baru bernama `.env` di root folder, isi dengan:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password_mysql_kamu
DB_PORT=3306
DB_NAME=m1_capst_money_manager
```

Sesuaikan `DB_USER` dan `DB_PASSWORD` dengan kredensial MySQL kamu.

### Step 6 - Jalankan Program
```bash
python main.py
```

---

## Tech Stack

- Python 3.11+  : Bahasa pemrograman utama
- SQLAlchemy    : Koneksi dan eksekusi query database
- pandas        : Manipulasi dan tampilan data
- matplotlib    : Visualisasi chart
- seaborn       : Styling visualisasi
- python-dotenv : Load konfigurasi dari .env
- mysql-connector-python : MySQL Driver