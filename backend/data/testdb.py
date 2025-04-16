from connect import get_connection

def test_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Connected! Tables in DB:", tables)
    except Exception as e:
        print("DB connection failed:", e)

if __name__ == "__main__":
    test_db()