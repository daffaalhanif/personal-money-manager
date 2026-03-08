from db.connection import create_engine_from_env
from utils.input_helpers import safe_int_input
from features.table import show_table_menu
from features.statistic import show_statistik_menu
from features.visualization import show_visualization_menu
from features.add_data import add_data_menu
from features.delete_data import delete_data_menu


def main() -> None:
    print("\n======= Xpense Insight =======")

    engine = create_engine_from_env()
    if engine is None:
        print("\nProgram berhenti karena tidak bisa terhubung ke database.")
        return
    
    try:
        while True:
            print("\n====== MAIN MENU ======")
            print("1. Tampilkan Tabel")
            print("2. Tampilkan Statistik")
            print("3. Visualisasi Data")
            print("4. Tambah Data")
            print("5. Hapus Data")
            print("0. Keluar")
            print("=======================\n")

            choice = safe_int_input("Pilih menu (0-5): ", range(6))

            if choice == 1:
                show_table_menu(engine)
            elif choice == 2:
                show_statistik_menu(engine)
            elif choice == 3:
                show_visualization_menu(engine)
            elif choice == 4:
                add_data_menu(engine)
            elif choice == 5:
                delete_data_menu(engine)
            else:
                print("\nTerima kasih, program dihentikan.")
                break
    
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan (Ctrl+C). Terima kasih.")

    finally:
        engine.dispose()
        print("Koneksi database berhasil ditutup.\n")

if __name__ == "__main__":
    main()
