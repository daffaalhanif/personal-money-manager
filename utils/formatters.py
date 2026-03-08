import pandas as pd

# === Menampilkan 'DATAFRAME' ===
def show_dataframe(df: pd.DataFrame) -> None:
    if df.empty:
        print("(Data kosong / tidak ada baris.)\n")
        return
    
    print(df.to_string(index=False))
    print("")

# === Menerapkan format rupiah dengan "." sebagai pemisah angka ===
def format_rupiah(amount: float) -> str:
    formatted = f"{amount:,.0f}"
    return f"Rp {formatted.replace(',', '.')}"

# === Formatter rupiah untuk label axis chart ===
def rupiah_axis_formatter(x, pos):
    return f"Rp {x:,.0f}".replace(',', '.')