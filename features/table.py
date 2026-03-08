import pandas as pd
from utils.query_helpers import run_select_df
from utils.formatters import show_dataframe, format_rupiah
from utils.input_helpers import safe_int_input, safe_flow_input


# === Menampilkan Tabel CATEGORIES dan Return DataFrame ===
def show_categories(engine, flow=None) -> pd.DataFrame:
    if flow is None:
        print("\n---- TABEL KATEGORI (SEMUA) ----")
        query = """
            SELECT category_id, category_name, flow
            FROM categories
            ORDER BY category_id
        """
        df = run_select_df(engine, query)
        show_dataframe(df)
        return df
    
    flow = flow.upper().strip()

    print(f"\n------ TABEL KATEGORI {flow} ------")
    query = """
        SELECT category_id, category_name, flow
        FROM categories
        WHERE flow = :flow
        ORDER BY category_id
    """
    df = run_select_df(engine, query, params={"flow": flow})
    show_dataframe(df)
    return df

# === Mengambil DataFrame Transaksi (raw, tanpa print, tanpa format) ===
def get_transactions_df(engine) -> pd.DataFrame:
    query = """
        SELECT
            t.trx_id,
            t.trx_date,
            t.flow,
            c.category_name,
            t.amount,
            t.note
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.trx_date DESC, t.trx_id DESC
    """
    return run_select_df(engine, query)

# === Menampilkan Tabel TRANSACTIONS (JOIN category_name) ALL DATA ===
def show_transactions_view_all(engine) -> None:
    print(f"\n------------------------------ TABEL TRANSAKSI (SEMUA) ------------------------------")

    df = get_transactions_df(engine)

    if df.empty:
        print("(Data kosong / tidak ada baris.)")
        return

    df_display = df.copy()
    df_display["amount"] = df_display["amount"].apply(format_rupiah)
    show_dataframe(df_display)
    print(f"Total: {len(df)} transaksi\n")

# === Menampilkan Tabel TRANSACTIONS (JOIN category_name) dengan Default LIMIT: 20 ===
def show_transactions_latest(engine, limit: int = 20) -> None:
    print(f"\n---------------------------- TABEL TRANSAKSI (TERBARU {limit}) --------------------------")
    query = """
        SELECT
            t.trx_id,
            t.trx_date,
            t.flow,
            c.category_name,
            t.amount,
            t.note
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.trx_date DESC, t.trx_id DESC
        LIMIT :limit
    """
    df = run_select_df(engine, query, params={"limit": limit})

    if df.empty:
        print("(Data kosong / tidak ada baris.)")
        return

    df_display = df.copy()
    df_display["amount"] = df_display["amount"].apply(format_rupiah)
    show_dataframe(df_display)

# === Menampilkan Table TRANSACTIONS by FLOW (IN / OUT) dengan Default LIMIT: 20 ===
def show_transactions_filter_flow(engine, flow: str, limit: int = 20) -> None:
    flow = flow.upper().strip()
    
    print(f"\n---------------------- TABEL TRANSAKSI (FLOW {flow} - LIMIT {limit}) ----------------------")
    query = """
        SELECT
            t.trx_id,
            t.trx_date,
            t.flow,
            c.category_name,
            t.amount,
            t.note
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.flow = :flow
        ORDER BY t.trx_date DESC, t.trx_id DESC
        LIMIT :limit
    """
    df = run_select_df(engine, query, params={"flow": flow, "limit": limit})

    if df.empty:
        print("(Data kosong / tidak ada baris.)")
        return

    df_display = df.copy()
    df_display["amount"] = df_display["amount"].apply(format_rupiah)
    show_dataframe(df_display)

# ========== OPSI MENU 1: SHOW TABLE ==========
def show_table_menu(engine) -> None:
    while True:
        print("\n=== Menu 1: TAMPILKAN TABEL ===")
        print("1. Tabel Kategori")
        print("2. Tabel Transaksi")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-2): ", range(3))

        if choice == 1:
            while True:
                print("\n--- Sub-Menu 1: TABEL KATEGORI ---")
                print("1. Lihat Semua Kategori")
                print("2. Lihat Kategori IN")
                print("3. Lihat Kategori OUT")
                print("0. Kembali\n")

                sub = safe_int_input("Pilih menu (0-3): ", range(4))

                if sub == 1:
                    show_categories(engine)
                elif sub == 2:
                    show_categories(engine, flow="IN")
                elif sub == 3:
                    show_categories(engine, flow="OUT")
                else:
                    break

        elif choice == 2:
            while True:
                print("\n-------- Sub-Menu 2: TABEL TRANSAKSI -------")
                print("1. Lihat Semua Transaksi")
                print("2. Lihat Transaksi Terbaru (20)")
                print("3. Lihat Transaksi berdasarkan Flow (IN/OUT)")
                print("0. Kembali\n")

                sub = safe_int_input("Pilih menu (0-3): ", range(4))

                if sub == 1:
                    show_transactions_view_all(engine)
                elif sub == 2:
                    show_transactions_latest(engine)
                elif sub == 3:
                    flow = safe_flow_input("\nMasukkan flow (IN/OUT/0=Kembali): ")
                    if flow is None:
                        continue
                    show_transactions_filter_flow(engine, flow)
                else:
                    break

        else:
            return