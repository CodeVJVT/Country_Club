import sqlite3

def collect_feedback(response_id, rating, comments):
    """Guarda el feedback de una respuesta."""
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            response_id INTEGER,
            rating INTEGER,
            comments TEXT
        )
    ''')
    cursor.execute("INSERT INTO feedback (response_id, rating, comments) VALUES (?, ?, ?)", (response_id, rating, comments))
    conn.commit()
    conn.close()
