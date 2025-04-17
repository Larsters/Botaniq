import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "mydb.db")

def get_connection():
    """Get a new database connection."""
    return sqlite3.connect(DB_PATH)

def insert_or_update_user_plant(user_id, plant, latitude, longitude, username, soil_ph=None, last_temperature=None):
    """Insert or update a user's plant record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_plants (user_id, plant, latitude, longitude, username, soil_ph, last_temperature)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                plant=excluded.plant,
                latitude=excluded.latitude,
                longitude=excluded.longitude,
                username=excluded.username,
                soil_ph=excluded.soil_ph,
                last_temperature=excluded.last_temperature,
                timestamp=CURRENT_TIMESTAMP
        """, (user_id, plant, latitude, longitude, username, soil_ph, last_temperature))
        conn.commit()

def get_user_plant(user_id):
    """Retrieve a user's plant record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_plants WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def get_all_users():
    """Retrieve all user plant records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_plants")
        return cursor.fetchall()