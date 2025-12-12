import sqlite3
from pathlib import Path

DB_PATH = Path("Encryptor.db")

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = 1")
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        username TEXT NOT NULL,
        inputfile TEXT NOT NULL,
        outputfile TEXT NOT NULL,
        action TEXT NOT NULL,
        timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
    )
    """)

    connection.commit()
    connection.close()

