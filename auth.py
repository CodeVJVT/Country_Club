import sqlite3


def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(username, password):
    """Función para crear un usuario (solo para pruebas)."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()
    conn.close()
