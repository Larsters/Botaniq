import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "mydb.db")

def get_connection():
    """Get a new database connection."""
    return sqlite3.connect(DB_PATH)

def insert_or_update_user(user_id, username):
    """Insert or update a user record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username
        """, (user_id, username))
        conn.commit()

def insert_farm(user_id, name, latitude, longitude, soil_type=None, soil_ph=None):
    """Insert a new farm record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO farms (user_id, name, latitude, longitude, soil_type, soil_ph)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, latitude, longitude, soil_type, soil_ph))
        conn.commit()
        return cursor.lastrowid

def insert_plant(farm_id, plant_type, last_temperature):
    """Insert a new plant record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO plants (farm_id, plant_type, last_temperature)
            VALUES (?, ?, ?)
        """, (farm_id, plant_type, last_temperature))
        conn.commit()
        return cursor.lastrowid