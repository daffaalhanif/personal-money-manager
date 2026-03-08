from utils.query_helpers import run_select_df
from utils.formatters import show_dataframe, format_rupiah
from utils.input_helpers import safe_int_input


# === Menampilkan Basic STATISTIK (COUNT, SUM, AVG) by FLOW (ALL / IN / OUT) ===
def get_basic_stats(engine, flow=None) -> tuple[int, float, float]:
    """
    flow:
    - None -> ALL
    - "IN" -> Hanya transaksi IN
    - "OUT" -> Hanya transaksi OUT
    """
    if flow is None:
        query = """
            SELECT
                COUNT(*) AS total_transaksi,
                SUM(amount) AS total_amount,
                AVG(amount) AS avg_amount
            FROM transactions
        """
        params = None
    
    else:
        query = """
            SELECT
                COUNT(*) AS total_transaksi,
                SUM(amount) AS total_amount,
                AVG(amount) AS avg_amount
            FROM transactions
            WHERE flow = :flow
        """
        params = {"flow": flow}

    df = run_select_df(engine, query, params=params)

    if df.empty:
        print("(Gagal mengambil data statistik dari database.)")
        return 0, 0, 0

    total_trx = df.loc[0, "total_transaksi"] or 0
    total_amount = df.loc[0, "total_amount"] or 0
    avg_amount = df.loc[0, "avg_amount"] or 0

    return total_trx, total_amount, avg_amount

# === Menampilkan DATAFRAME STATISTIK per KATEGORI by FLOW (IN / OUT) ===
def show_stats_per_category_by_flow(engine, flow: str) -> None:
    flow = flow.upper().strip()

    print(f"\n------------ STATISTIK PER KATEGORI ({flow}) ----------")

    query = """
        SELECT
            c.category_name,
            COUNT(*) AS trx_count,
            SUM(t.amount) AS total_amount,
            AVG(t.amount) AS avg_amount
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.flow = :flow
        GROUP BY c.category_name
        ORDER BY total_amount DESC
    """

    df = run_select_df(engine, query, params={"flow": flow})

    if df.empty:
        print("(Data kosong / tidak ada baris.)")
        return
    
    df_display = df.copy()
    df_display["total_amount"] = df_display["total_amount"].apply(format_rupiah)
    df_display["avg_amount"] = df_display["avg_amount"].apply(format_rupiah)
    show_dataframe(df_display)

# ========== OPSI MENU 2: SHOW STATISTIK ==========
def show_statistik_menu(engine) -> None:
    while True:
        print("\n===== Menu 2: TAMPILKAN STATISTIK =====")
        print("1. Lihat Semua Statistik")
        print("2. Lihat Statistik IN")
        print("3. Lihat Statistik OUT")
        print("4. Lihat Statistik per Kategori (IN)")
        print("5. Lihat Statistik per Kategori (OUT)")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-5): ", range(6))
        
        if choice == 1:
            total_trx, total_amount, avg_amount = get_basic_stats(engine, flow=None)
            print("\n--------- STATISTIK SEMUA ---------")
            print(f"Total Transaksi    : {total_trx}")
            print(f"Total Nominal      : {format_rupiah(total_amount)}")
            print(f"Rata-Rata Nominal  : {format_rupiah(avg_amount)}")

        elif choice == 2:
            total_trx, total_amount, avg_amount = get_basic_stats(engine, flow="IN")
            print("\n---------- STATISTIK IN ----------")
            print(f"Total Transaksi   : {total_trx}")
            print(f"Total Nominal     : {format_rupiah(total_amount)}")
            print(f"Rata-Rata Nominal : {format_rupiah(avg_amount)}")

        elif choice == 3:
            total_trx, total_amount, avg_amount = get_basic_stats(engine, flow="OUT")
            print("\n--------- STATISTIK OUT ---------")
            print(f"Total Transaksi    : {total_trx}")
            print(f"Total Nominal      : {format_rupiah(total_amount)}")
            print(f"Rata-Rata Nominal  : {format_rupiah(avg_amount)}")

        elif choice == 4:
            show_stats_per_category_by_flow(engine, "IN")

        elif choice == 5:
            show_stats_per_category_by_flow(engine, "OUT")

        else:
            return