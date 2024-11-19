import sqlite3

def log_query(user, query):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            query TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("INSERT INTO logs (user, query) VALUES (?, ?)", (user, query))
    conn.commit()
    conn.close()

def get_statistics():
    """Devuelve estadísticas básicas del uso del chatbot."""
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT query, COUNT(*) as count FROM logs GROUP BY query ORDER BY count DESC LIMIT 5")
    stats = cursor.fetchall()
    conn.close()
    return stats
