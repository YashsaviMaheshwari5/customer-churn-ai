import sqlite3
import hashlib

# --- CONNECTION ---
def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

# --- CREATE TABLE ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# --- HASH PASSWORD ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- ADD USER ---
def add_user(email, password):
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed)
        )
        conn.commit()
        return True
    except:
        return False

# --- LOGIN USER ---
def login_user(email, password):
    hashed = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hashed)
    )
    return cursor.fetchone()