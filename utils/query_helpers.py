import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError



# === Menjalankan Query 'SELECT' ===
def run_select_df(engine, query: str, params=None) -> pd.DataFrame:
    """
    - query: string SQL
    - params: dict untuk parameter query (Ex: {"limit": 20})
    'parameter' dipakai jika query butuh parameter tambahan (Ex: LIMIT :limit)
    """
    try:
        sql_query = text(query)
        df = pd.read_sql(sql_query, engine, params=params)
        return df
    
    except Exception as e:
        print("Query gagal dijalankan")
        print(f"Detail error: {e}\n")
        return pd.DataFrame()
    
# === Menjalankan Query 'Non-SELECT' (INSERT / UPDATE / DELETE) ===
def run_execute(engine, query: str, params=None) -> bool:
    """
    - engine.begin() akan otomatis COMMIT jika tidak ada error,
    dan akan otomatis ROLLBACK jika ada error.
    - IntegrityError (duplikat / FK violation) di-raise ke caller.
    """
    try:
        sql = text(query)
        with engine.begin() as connection:
            connection.execute(sql, params or {})
        return True
    
    except IntegrityError:
        raise
    
    except Exception as e:
        print("Query gagal dijalankan.")
        print(f"Detail error: {e}\n")
        return False