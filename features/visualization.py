import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from utils.query_helpers import run_select_df
from utils.formatters import rupiah_axis_formatter
from utils.input_helpers import safe_int_input


# === Helper Function -> Save Chart to PNG ===
def save_chart(filename: str) -> None:
    save = input("\nSimpan chart sebagai PNG? (Y/N): ").strip().upper()
    if save == "Y":
        full_path = f"charts/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        plt.savefig(full_path, dpi=150, bbox_inches="tight")
        print(f"\nBerhasil Tersimpan: {full_path}")

# === Menampilkan 'BAR CHART' Frekuensi Transaksi per Kategori (IN & OUT) ===
def plot_trx_count_per_category(engine) -> None:
    query = """
        SELECT
            c.category_name,
            t.flow,
            COUNT(*) AS total_trx
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        GROUP BY c.category_name, t.flow
        ORDER BY total_trx DESC
    """

    # Query Range Waktu
    query_range = """
        SELECT MIN(trx_date) AS tgl_awal, MAX(trx_date) AS tgl_akhir
        FROM transactions
    """

    df = run_select_df(engine, query)
    df_range = run_select_df(engine, query_range)

    if df.empty:
        print("(Data kosong, chart tidak dapat ditampilkan.)\n")
        return
    
    tgl_awal = df_range.loc[0,  "tgl_awal"].strftime("%d %b %Y")
    tgl_akhir = df_range.loc[0,  "tgl_akhir"].strftime("%d %b %Y")

    df_in = df[df["flow"] == "IN"].sort_values("total_trx", ascending=False)
    df_out = df[df["flow"] == "OUT"].sort_values("total_trx", ascending=False)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    sns.barplot(data=df_in, x="total_trx", y="category_name", color="#27ae60", ax=ax1)
    sns.barplot(data=df_out, x="total_trx", y="category_name", color="#e74c3c", ax=ax2)

    ax1.set_title("Frekuensi Transaksi - IN")
    ax1.set_xlabel("Jumlah Transaksi")
    ax1.set_ylabel("Kategori")

    ax2.set_title("Frekuensi Transaksi - OUT")
    ax2.set_xlabel("Jumlah Transaksi")
    ax2.set_ylabel("Kategori")

    plt.suptitle(f"Frekuensi Transaksi per Kategori\n{tgl_awal} - {tgl_akhir}", fontsize=13, fontweight="bold")
    plt.tight_layout()

    save_chart("Bar_Frekuensi_Transaksi_per_Kategori")
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

    save_chart("Bar_Plot_Top5_Out_Categories")
    plt.show()
    plt.close()

# === Menampilkan 'GROUPED BAR' Monthly Cashflow IN vs OUT per Bulan ===
def plot_monthly_cashflow(engine) -> None:
    query = """
        SELECT
            DATE_FORMAT(trx_date, '%b %Y') AS month,
            DATE_FORMAT(trx_date, '%Y-%m') AS month_sort,
            flow,
            SUM(amount) AS total_amount
        FROM transactions
        GROUP BY month_sort, month, flow
        ORDER BY month_sort
    """
    df = run_select_df(engine, query)

    if df.empty:
        print("(Data kosong, chart tidak dapat ditampilkan.)")
        return
    
    pivot = df.pivot_table(
        index=["month_sort", "month"],
        columns="flow",
        values="total_amount",
        fill_value=0
    ).reset_index()

    x = range(len(pivot))
    width = 0.35

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    ax.bar([i - width/2 for i in x], pivot.get("IN", 0), width, label="IN", color='#27ae60')
    ax.bar([i + width/2 for i in x], pivot.get("OUT", 0), width, label="OUT", color='#e74c3c')

    plt.title("Monthly Cashflow: IN vs OUT")
    plt.xlabel("Bulan")
    plt.ylabel("Total Nominal")
    plt.xticks(list(x), pivot["month"].tolist())

    ax.yaxis.set_major_formatter(plt.FuncFormatter(rupiah_axis_formatter))
    plt.legend()
    plt.tight_layout()
    save_chart("Grouped_Bar_Monthly_Cashflow_IN_OUT")
    plt.show()
    plt.close()

# ========== OPSI MENU 3: DATA VISUALIZATION ==========
def show_visualization_menu(engine) -> None:
    while True:
        print("\n============ Menu 3: Visualisasi Data ===========")
        print("1. Frekuensi Transaksi per Kategori IN & OUT")
        print("2. Top 5 Kategori Pengeluaran Terbesar")
        print("3. Monthly Cashflow IN & OUT")
        print("0. Kembali\n")

        choice = safe_int_input("Pilih menu (0-3): ", range(4))

        if choice == 1:
            plot_trx_count_per_category(engine)
        elif choice == 2:
            plot_top5_out_categories(engine)
        elif choice == 3:
            plot_monthly_cashflow(engine)
        else:
            return