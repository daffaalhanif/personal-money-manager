from sqlalchemy.exc import IntegrityError
from utils.query_helpers import run_execute
from utils.formatters import format_rupiah
from utils.input_helpers import (
    safe_int_input,
    safe_date_input,
    safe_amount_input,
    safe_flow_input,
    safe_confirm_input
)
from features.table import show_categories


# === ADD DATA Transaksi ke Tabel TRANSACTIONS ===
def add_transaction(engine) -> None:
    """
    Flow:
    1) Input trx_date
    2) Input amount
    3) Input flow (IN / OUT)
    4) Pilih category_id (Tampilkan categories dulu)
    5) Input note (Opsional. Boleh kosong)
    6) INSERT ke table transactions
    """
    print("\n--------------------- TAMBAH TRANSAKSI ---------------------")

    trx_date = safe_date_input("Masukkan trx_date (YYYY-MM-DD) [Enter = Tanggal hari ini, 0=Kembali]: ")
    if trx_date is None:
        print("\nKembali ke menu sebelumnya.")
        return
    
    amount = safe_amount_input("\nMasukkan amount (> 0) [0=Kembali]: ")
    if amount is None:
        print("\nKembali ke menu sebelumnya.")
        return

    flow = safe_flow_input("\nMasukkan flow transaksi (IN/OUT/0=Kembali): ")
    if flow is None:
        print("\nKembali ke menu sebelumnya.")
        return

    print("\nDaftar Kategori (Sesuai flow transaksi):")
    df_cat = show_categories(engine, flow=flow)

    if df_cat.empty:
        print(f"Tambahkan kategori flow {flow} terlebih dahulu.\n")
        return
    
    valid_ids = set(df_cat["category_id"])

    while True:
        category_id = safe_int_input("Pilih category_id (0=Kembali): ")

        if category_id == 0:
            print("\nKembali ke menu sebelumnya.")
            return

        if category_id in valid_ids:
            break

        print("category_id tidak sesuai. Pilih dari daftar Tabel Kategori.")

    category_name = df_cat.loc[df_cat["category_id"] == category_id, "category_name"].values[0]

    note = input("\nMasukkan note (Opsional, Enter untuk skip): ").strip()
    if note == "":
        note = None

    print(f"\n--- Ringkasan Transaksi ---")
    print(f"Tanggal : {trx_date}")
    print(f"Amount : {format_rupiah(amount)}")
    print(f"Flow : {flow}")
    print(f"Kategori : {category_name}")
    print(f"Note : {note if note else '-'}")

    if not safe_confirm_input("\nKonfirmasi tambah transaksi ini? (Y/N): "):
        print("\nTambah Transaksi dibatalkan.")
        return

    query = """
        INSERT INTO transactions (trx_date, amount, flow, category_id, note)
        VALUES (:trx_date, :amount, :flow, :category_id, :note)
    """
    params = {
        "trx_date": trx_date,
        "amount": amount,
        "flow": flow,
        "category_id": category_id,
        "note": note
    }

    success = run_execute(engine, query, params=params)
    if success:
        print(f"\nTransaksi berhasil ditambahkan! ({category_name} | {flow} | {format_rupiah(amount)})")

# === ADD DATA New Category ke Tabel CATEGORIES ===
def add_category(engine) -> None:
    """
    Flow:
    1) Show tabel categories (ALL)
    2) Input nama category baru
    3) Validasi tidak boleh kosong
    4) Flow wajib IN atau OUT
    5) Handle duplicate (UNIQUE category_name)
    6) INSERT ke table categories
    """
    print("\n--------- TAMBAH KATEGORI ---------")
    print("Daftar Kategori saat ini:")
    show_categories(engine)

    print("Silakan tambah kategori baru.")

    while True:
        category_name = input("\nMasukkan category_name (0=Kembali): ").strip()

        if category_name == "0":
            print("\nKembali ke menu sebelumnya.")
            return

        if category_name == "":
            print("category_name tidak boleh kosong.")
            continue

        if not all(c.isalpha() or c.isspace() for c in category_name):
            print("category_name hanya boleh berisi huruf dan spasi. (Contoh: Food, Daily Transport)")
            continue

        break

    flow = safe_flow_input("\nMasukkan flow category (IN/OUT/0=Kembali): ")
    if flow is None:
        print("\nKembali ke menu sebelumnya.")
        return

    query = """
        INSERT INTO categories (category_name, flow)
        VALUES (:category_name, :flow)
    """

    try:
        run_execute(engine, query, {"category_name": category_name, "flow": flow})
        
        print(f"\nKategori baru berhasil ditambahkan! ({category_name} | {flow})")
        print("\nDaftar Kategori terbaru:")
        show_categories(engine)

    except IntegrityError:
        print("\nKategori sudah ada (duplikat). Silakan pakai nama lain.")

# ========== OPSI MENU 4: ADD DATA ==========
def add_data_menu(engine) -> None:
    while True:
        print("\n=== Menu 4: TAMBAH DATA ===")
        print("1. Tambah Transaksi")
        print("2. Tambah Kategori")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-2): ", range(3))

        if choice == 1:
            add_transaction(engine)
        elif choice == 2:
            add_category(engine)
        else:
            return