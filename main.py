import sqlite3

DB = "space_book.db"


def koneksi():
    return sqlite3.connect(DB)


def init_db():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT, no_hp TEXT, username TEXT UNIQUE,
        password TEXT, role TEXT DEFAULT 'user')""")
    cur.execute("""CREATE TABLE IF NOT EXISTS fasilitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_fasilitas TEXT, jenis TEXT, harga_per_jam INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_fasilitas INTEGER, id_user INTEGER,
        tanggal TEXT, jam_mulai TEXT, jam_selesai TEXT,
        status_booking TEXT, status_bayar TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS pembayaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_booking INTEGER, metode TEXT,
        referensi TEXT, tanggal_bayar TEXT)""")

    if cur.execute("SELECT COUNT(*) FROM fasilitas").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO fasilitas (nama_fasilitas, jenis, harga_per_jam) VALUES (?,?,?)",
            [("Lapangan Futsal A", "Olahraga", 150000),
             ("Lapangan Badminton B", "Olahraga", 60000),
             ("Ruang Meeting Alpha", "Coworking", 100000),
             ("Ruang Meeting Beta", "Coworking", 100000)])

    if cur.execute("SELECT COUNT(*) FROM user WHERE role='admin'").fetchone()[0] == 0:
        cur.execute("INSERT INTO user (nama, no_hp, username, password, role) "
                    "VALUES ('Administrator','0800000000','admin','admin123','admin')")
    con.commit()
    con.close()


def registrasi():
    print("\n=== REGISTRASI ===")
    nama = input("Nama Lengkap : ").strip()
    no_hp = input("Nomor HP     : ").strip()
    username = input("Username     : ").strip()
    password = input("Password     : ").strip()

    if not nama or not username:
        print("ERROR: Nama dan username tidak boleh kosong.")
        return
    if not (no_hp.isdigit() and len(no_hp) >= 10):
        print("ERROR: Nomor HP minimal 10 digit angka.")
        return
    if len(password) < 6:
        print("ERROR: Password minimal 6 karakter.")
        return

    con = koneksi()
    cur = con.cursor()
    if cur.execute("SELECT id FROM user WHERE username=?", (username,)).fetchone():
        print("ERROR: Username sudah dipakai.")
    else:
        cur.execute("INSERT INTO user (nama, no_hp, username, password, role) "
                    "VALUES (?,?,?,?, 'user')", (nama, no_hp, username, password))
        con.commit()
        print("Registrasi berhasil. Silakan login.")
    con.close()


def login():
    print("\n=== LOGIN ===")
    username = input("Username : ").strip()
    password = input("Password : ").strip()
    con = koneksi()
    cur = con.cursor()
    data = cur.execute("SELECT id, nama, role FROM user WHERE username=? AND password=?",
                       (username, password)).fetchone()
    con.close()
    if data:
        print(f"Login Berhasil. Selamat datang, {data[1]}!")
        return data
    print("Username atau Password Salah")
    return None


def menu_awal():
    while True:
        print("\n===== SPACE BOOK =====")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            registrasi()
        elif pilih == "2":
            user = login()
            if user:
                
                if user[2] == "admin":
                    menu_admin(user)
                else:
                    menu_user(user)
        elif pilih == "3":
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak valid.")

def lihat_fasilitas():
    con = koneksi()
    cur = con.cursor()
    rows = cur.execute("SELECT id, nama_fasilitas, jenis, harga_per_jam FROM fasilitas").fetchall()
    con.close()
    print("\nID  Nama                  Jenis       Harga/Jam")
    for r in rows:
        print(f"{r[0]:<4}{r[1]:<22}{r[2]:<12}Rp {r[3]:,}")
    return rows


def tambah_fasilitas():
    nama = input("Nama fasilitas : ").strip()
    jenis = input("Jenis (Olahraga/Coworking) : ").strip()
    harga = input("Harga per jam : ").strip()
    if not nama or not jenis or not harga.isdigit():
        print("ERROR: Data tidak valid (harga harus angka).")
        return
    con = koneksi()
    con.execute("INSERT INTO fasilitas (nama_fasilitas, jenis, harga_per_jam) VALUES (?,?,?)",
                (nama, jenis, int(harga)))
    con.commit()
    con.close()
    print("Fasilitas berhasil ditambah.")


def ubah_fasilitas():
    lihat_fasilitas()
    id_f = input("ID fasilitas yang diubah : ").strip()
    nama = input("Nama baru : ").strip()
    jenis = input("Jenis baru : ").strip()
    harga = input("Harga baru : ").strip()
    if not id_f.isdigit() or not nama or not jenis or not harga.isdigit():
        print("ERROR: Data tidak valid.")
        return
    con = koneksi()
    cur = con.execute("UPDATE fasilitas SET nama_fasilitas=?, jenis=?, harga_per_jam=? WHERE id=?",
                      (nama, jenis, int(harga), int(id_f)))
    con.commit()
    con.close()
    print("Fasilitas diubah." if cur.rowcount else "ID tidak ditemukan.")


def hapus_fasilitas():
    lihat_fasilitas()
    id_f = input("ID fasilitas yang dihapus : ").strip()
    if not id_f.isdigit():
        print("ERROR: ID harus angka.")
        return
    con = koneksi()
    cur = con.execute("DELETE FROM fasilitas WHERE id=?", (int(id_f),))
    con.commit()
    con.close()
    print("Fasilitas dihapus." if cur.rowcount else "ID tidak ditemukan.")


def kelola_fasilitas():
    while True:
        print("\n--- KELOLA FASILITAS ---")
        print("1. Lihat  2. Tambah  3. Ubah  4. Hapus  5. Kembali")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            lihat_fasilitas()
        elif pilih == "2":
            tambah_fasilitas()
        elif pilih == "3":
            ubah_fasilitas()
        elif pilih == "4":
            hapus_fasilitas()
        elif pilih == "5":
            break
        else:
            print("Pilihan tidak valid.")


def menu_admin(user):
    while True:
        print("\n===== DASHBOARD ADMIN =====")
        print("1. Kelola Fasilitas")
        print("2. Lihat Booking (menyusul)")
        print("3. Validasi Pembayaran (menyusul)")
        print("4. Batalkan Booking (menyusul)")
        print("5. Laporan (menyusul)")
        print("6. Logout")
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            kelola_fasilitas()
        elif pilih == "6":
            print("Logout berhasil.")
            break
        elif pilih in ("2", "3", "4", "5"):
            print("Fitur ini menyusul.")
        else:
            print("Pilihan tidak valid.")


def menu_user(user):
    while True:
        print("\n===== SPACE BOOK =====")
        print("1. Lihat Fasilitas")
        print("2. Cek Ketersediaan Jadwal (menyusul)")
        print("3. Booking Fasilitas (menyusul)")
        print("4. Riwayat Booking (menyusul)")
        print("5. Pembayaran (menyusul)")
        print("6. Logout")
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            lihat_fasilitas()
        elif pilih == "2":
            cek_ketersediaan()
        elif pilih == "6":
            print("Logout berhasil.")
            break
        elif pilih in ("2", "3", "4", "5"):
            print("Fitur ini menyusul.")
        else:
            print("Pilihan tidak valid.")

from datetime import datetime

JAM_BUKA = 8
JAM_TUTUP = 22


def jam_ke_menit(jam):
    try:
        j = datetime.strptime(jam, "%H:%M")
        return j.hour * 60 + j.minute
    except ValueError:
        return None


def tanggal_valid(tgl):
    try:
        datetime.strptime(tgl, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def input_jadwal():
    id_f = input("ID Fasilitas         : ").strip()
    tanggal = input("Tanggal (DD-MM-YYYY) : ").strip()
    mulai = input("Jam Mulai (HH:MM)    : ").strip()
    selesai = input("Jam Selesai (HH:MM)  : ").strip()

    if not id_f.isdigit():
        print("ERROR: ID fasilitas harus angka.")
        return None
    if not tanggal_valid(tanggal):
        print("ERROR: Format tanggal salah. Contoh: 10-06-2026")
        return None
    m = jam_ke_menit(mulai)
    s = jam_ke_menit(selesai)
    if m is None or s is None:
        print("ERROR: Format jam salah. Contoh: 18:00")
        return None
    if m < JAM_BUKA * 60 or s > JAM_TUTUP * 60:
        print("ERROR: Jam operasional 08:00 - 22:00.")
        return None
    if s - m < 60:
        print("ERROR: Durasi booking minimal 1 jam.")
        return None

    con = koneksi()
    ada = con.execute("SELECT id FROM fasilitas WHERE id=?", (int(id_f),)).fetchone()
    con.close()
    if not ada:
        print("ERROR: ID fasilitas tidak ditemukan.")
        return None

    mulai = f"{m // 60:02d}:{m % 60:02d}"
    selesai = f"{s // 60:02d}:{s % 60:02d}"
    return int(id_f), tanggal, mulai, selesai


def cek_bentrok(id_f, tanggal, mulai, selesai):
    m_baru = jam_ke_menit(mulai)
    s_baru = jam_ke_menit(selesai)
    con = koneksi()
    rows = con.execute(
        "SELECT jam_mulai, jam_selesai FROM booking "
        "WHERE id_fasilitas=? AND tanggal=? AND status_booking != 'DIBATALKAN'",
        (id_f, tanggal)).fetchall()
    con.close()
    for jam_m, jam_s in rows:
        m_lama = jam_ke_menit(jam_m)
        s_lama = jam_ke_menit(jam_s)
        if m_baru < s_lama and s_baru > m_lama:
            return True
    return False


def tampil_jadwal_harian(id_f, tanggal):
    print(f"\nJadwal {tanggal}")
    for jam in range(JAM_BUKA, JAM_TUTUP):
        mulai = f"{jam:02d}:00"
        selesai = f"{jam + 1:02d}:00"
        status = "BOOKED" if cek_bentrok(id_f, tanggal, mulai, selesai) else "KOSONG"
        print(f"{mulai}-{selesai}  {status}")


def cek_ketersediaan():
    print("\n=== CEK KETERSEDIAAN JADWAL ===")
    lihat_fasilitas()
    data = input_jadwal()
    if not data:
        return
    id_f, tanggal, mulai, selesai = data
    if cek_bentrok(id_f, tanggal, mulai, selesai):
        print("Jadwal TIDAK tersedia (sudah dipakai).")
    else:
        print("Jadwal TERSEDIA.")
    tampil_jadwal_harian(id_f, tanggal)
if __name__ == "__main__":
    init_db()
    menu_awal()