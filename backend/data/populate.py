import sqlite3

DB_PATH = "mydb.db"

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_plants (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                plant TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                soil_ph REAL,
                last_temperature REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Database and table created successfully.")

if __name__ == "__main__":
    create_tables()