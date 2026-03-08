from sqlalchemy.exc import IntegrityError
from utils.query_helpers import run_select_df, run_execute
from utils.formatters import show_dataframe, format_rupiah
from utils.input_helpers import safe_int_input, safe_confirm_input
from features.table import get_transactions_df


# === DELETE DATA Transaksi dari Tabel TRANSACTIONS by trx_id ===
def delete_transaction(engine) -> None:
    """
    Flow:
    1) Tampilkan seluruh transaksi
    2) User pilih trx_id (0=Kembali)
    3) Validasi trx_id terdaftar
    4) Konfirmasi hapus
    5) Delete
    """
    print("\n--------------------------------- HAPUS TRANSAKSI --------------------------------")

    df = get_transactions_df(engine)

    if df.empty:
        print("(Tidak ada transaksi untuk dihapus.)")
        return

    df_display = df.copy()
    df_display["amount"] = df_display["amount"].apply(format_rupiah)
    show_dataframe(df_display)

    valid_ids = set(df["trx_id"])

    while True:
        trx_id = safe_int_input("Masukkan trx_id yang mau dihapus (0=Kembali): ")
        if trx_id == 0:
            print("Kembali ke menu sebelumnya.")
            return
        if trx_id in valid_ids:
            break
        print("trx_id tidak ditemukan. Pilih dari tabel di atas.")

    row = df[df["trx_id"] == trx_id].iloc[0]

    print(f"\nTransaksi yang akan dihapus:")
    print(f"ID       : {row['trx_id']}")
    print(f"Tanggal  : {row['trx_date']}")
    print(f"Flow     : {row['flow']}")
    print(f"Kategori : {row['category_name']}")
    print(f"Amount   : {format_rupiah(row['amount'])}")
    print(f"Note     : {row['note']}")

    if not safe_confirm_input("\nYakin hapus transaksi ini? (Y/N): "):
        print("\nHapus transaksi dibatalkan.")
        return
    
    query = """
        DELETE FROM transactions
        WHERE trx_id = :trx_id
    """
    success = run_execute(engine, query, params={"trx_id": trx_id})

    if success:
        print(f"\nTransaksi berhasil dihapus! (ID {trx_id} | {row['flow']} | {row['category_name']} | {format_rupiah(row['amount'])})")

# === DELETE DATA Category dari Tabel CATEGORIES by category_id ===
def delete_category(engine) -> None:
    """
    Flow:
    1) Tampilkan category_id terdaftar
    2) User pilih category_id (0=Kembali)
    3) Validasi category_id terdaftar
    4) Validasi gagal hapus category jika masih dipakai di tabel transactions
    5) Konfirmasi hapus
    6) Delete
    """
    print("\n------- HAPUS KATEGORI -------")

    query_list_category = """
        SELECT category_id, category_name, flow
        FROM categories
        ORDER BY category_id
    """
    df = run_select_df(engine, query_list_category)

    if df.empty:
        print("(Tidak ada kategori untuk dihapus.)")
        return
    
    show_dataframe(df)
    
    valid_ids = set(df["category_id"])

    while True:
        category_id = safe_int_input("Masukkan category_id yang mau dihapus (0=Kembali): ")
        if category_id == 0:
            print("\nKembali ke menu sebelumnya.")
            return
        if category_id in valid_ids:
            break
        print("category_id tidak ada di daftar. Pilih dari tabel kategori yang ditampilkan.\n")

    row = df[df['category_id'] == category_id].iloc[0]

    print(f"\nKategori yang akan dihapus:")
    print(f"ID   : {row['category_id']}")
    print(f"Nama : {row['category_name']}")
    print(f"Flow : {row['flow']}")

    if not safe_confirm_input("\nYakin hapus kategori ini? (Y/N): "):
        print("\nHapus kategori dibatalkan.")
        return
    
    query_delete_category = """
        DELETE FROM categories
        WHERE category_id = :category_id
    """

    try:
        run_execute(engine, query_delete_category, {"category_id": category_id})

        print(f"\nKategori berhasil dihapus! ({row['category_name']} | {row['flow']})")

    except IntegrityError:
        print("Gagal: Kategori ini masih dipakai oleh transaksi yang ada.")

# ========== OPSI MENU 5: DELETE DATA ==========
def delete_data_menu(engine) -> None:
    while True:
        print("\n=== Menu 5: HAPUS DATA ===")
        print("1. Hapus Transaksi")
        print("2. Hapus Kategori")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-2): ", range(3))

        if choice == 1:
            delete_transaction(engine)
        elif choice == 2:
            delete_category(engine)
        else:
            return