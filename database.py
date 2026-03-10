import sqlite3
import os

DB_PATH = os.path.join("database", "carbon_data.db")


def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transport REAL,
        electricity REAL,
        food TEXT,
        emission REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_activity(transport, electricity, food, emission):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO activities (transport, electricity, food, emission)
    VALUES (?, ?, ?, ?)
    """, (transport, electricity, food, emission))

    conn.commit()
    conn.close()


def fetch_all_activities():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM activities")

    data = cursor.fetchall()

    conn.close()

    return data