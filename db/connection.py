import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


# === Membuat dan Connect 'SQLAlchemy Engine' dari Konfigurasi di File .env ===
def create_engine_from_env():
    load_dotenv()

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "3306")

    try:
        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(url)

        with engine.connect() as _:
            pass

        print("Koneksi ke database berhasil.")
        return engine
    
    except Exception as e:
        print("Gagal terhubung ke database.")
        print(f"Detail error: '{e}'")
        return None