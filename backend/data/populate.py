import sqlite3

DB_PATH = "mydb.db"

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farms (
                farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                latitude REAL,
                longitude REAL,
                soil_type TEXT,
                soil_ph REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plants (
                plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER,
                plant_type TEXT,
                last_temperature REAL,
                planted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(farm_id) REFERENCES farms(farm_id)
            );
        """)
        conn.commit()
        print("Database and tables created successfully.")

if __name__ == "__main__":
    create_tables()