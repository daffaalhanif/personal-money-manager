import seaborn as sns
import matplotlib.pyplot as plt
from utils.query_helpers import run_select_df
from utils.formatters import rupiah_axis_formatter
from utils.input_helpers import safe_int_input


# === Menampilkan 'HISTOGRAM' untuk Kolom AMOUNT dari Tabel TRANSACTIONS ===
def plot_histogram_amount(engine) -> None:
    query = """
        SELECT amount, flow
        FROM transactions
    """
    df = run_select_df(engine, query)

    if df.empty:
        print("(Data transaksi kosong, histogram tidak dapat ditampilkan.)\n")
        return

    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x="amount", bins=15, hue="flow", multiple="stack")

    plt.title("Distribusi Nominal Transaksi (IN vs OUT)")
    plt.xlabel("Nominal Transaksi")
    plt.ylabel("Jumlah Transaksi")

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(rupiah_axis_formatter))
    plt.tight_layout()
    plt.show()
    plt.close()

# === Menampilkan 'BAR PLOT' Top 5 KATEGORI OUT Berdasarkan TOTAL AMOUNT (SUM) ===
def plot_top5_out_categories(engine) -> None:
    query = """
        SELECT
            c.category_name,
            SUM(t.amount) AS total_out
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.flow = 'OUT'
        GROUP BY c.category_name
        ORDER BY total_out DESC
        LIMIT 5
    """
    df = run_select_df(engine, query)

    if df.empty:
        print("(Tidak ada data untuk ditampilkan.)\n")
        return
    
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=df, x="total_out", y="category_name")

    plt.title("Top 5 Kategori Pengeluaran Terbesar")
    plt.xlabel("Total Pengeluaran")
    plt.ylabel("Kategori")

    ax.xaxis.set_major_formatter(plt.FuncFormatter(rupiah_axis_formatter))
    plt.tight_layout()
    plt.show()
    plt.close()

# ========== OPSI MENU 3: DATA VISUALIZATION ==========
def show_visualization_menu(engine) -> None:
    while True:
        print("\n============ Menu 3: Visualisasi Data ===========")
        print("1. Distribusi Nominal Transaksi (Histogram)")
        print("2. Top 5 Kategori Pengeluaran Terbesar (Bar Plot)")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-2): ", range(3))

        if choice == 1:
            plot_histogram_amount(engine)
        elif choice == 2:
            plot_top5_out_categories(engine)
        else:
            return