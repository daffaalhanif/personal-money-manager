from datetime import datetime, date


# === Input 'ANGKA' Aman Agar Program Tidak Crash Jika User Salah Input ===
def safe_int_input(prompt: str, pilihan_valid=None) -> int:
    while True:
        user_input = input(prompt).strip()
        
        if user_input == "":
            print("Input tidak boleh kosong. Coba lagi.\n")
            continue

        if not user_input.isdigit():
            print("Input harus angka bulat. Coba lagi.\n")
            continue

        angka = int(user_input)

        if pilihan_valid is not None and angka not in pilihan_valid:
            print(f"Pilihan tidak valid. Pilih salah satu: {sorted(pilihan_valid)}\n")
            continue

        return angka

# === Input 'TANGGAL' Aman dengan Format YYYY-MM-DD ===
def safe_date_input(prompt: str) -> date:
    while True:
        date_str = input(prompt).strip()

        if date_str == "0":
            return None

        if date_str == "":
            today = datetime.now().date()
            print(f"\nBerhasil input menggunakan tanggal hari ini: {today}")
            return today

        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            return parsed_date
        
        except ValueError:
            print("Format tanggal harus YYYY-MM-DD. (Contoh: 2026-12-01)\n")

# === Input 'AMOUNT' Aman (Boleh INT / FLOAT) dengan Syarat > 0 ===
def safe_amount_input(prompt: str) -> float:
    while True:
        amount_str = input(prompt).strip()

        if amount_str == "":
            print("Input tidak boleh kosong.")
            continue
        
        try:
            amount = float(amount_str)
        except ValueError:
            print("Amount harus berupa angka. (Contoh: 50000)")
            continue

        if amount < 0:
            print("Amount tidak boleh negatif. Coba lagi.")
            continue

        if amount == 0:
            return None

        return amount

# === Input 'FLOW' Aman dengan Pilihan Valid (IN/OUT) ===
def safe_flow_input(prompt: str) -> str:
    while True:
        flow = input(prompt).strip().upper()

        if flow == "0":
            return None

        if flow == "":
            print("Input tidak boleh kosong.")
            continue

        if flow in ("IN", "OUT"):
            return flow
        
        print('Flow harus "IN" / "OUT" / "0" (Kembali).')

# === Input 'KONFIRMASI' Aman (Y/N) -> (Return: True jika Y, False jika N) ===
def safe_confirm_input(prompt: str) -> bool:
    while True:
        confirm = input(prompt).strip().upper()

        if confirm == "":
            print('Input tidak boleh kosong. Masukkan "Y" atau "N".')
            continue

        if confirm == "Y":
            return True
        
        if confirm == "N":
            return False
        
        print('Input harus "Y" atau "N".')