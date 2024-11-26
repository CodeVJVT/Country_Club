import sqlite3


def create_database():
    """Crea la base de datos y la tabla 'documentos' si no existen."""
    conn = sqlite3.connect("document_data.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pagina INTEGER,
            categoria TEXT,
            texto TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def query_database(query):
    """Consulta la base de datos para buscar coincidencias de texto."""
    conn = sqlite3.connect("document_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos WHERE texto LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return results


def query_by_category(category):
    """Consulta por categoría específica."""
    conn = sqlite3.connect("document_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos WHERE categoria = ?", (category,))
    results = cursor.fetchall()
    conn.close()
    return results


def save_page_data(pagina, categoria, texto):
    """Guarda los datos de una página en la base de datos."""
    conn = sqlite3.connect("document_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documentos (pagina, categoria, texto) VALUES (?, ?, ?)",
        (pagina, categoria, texto),
    )
    conn.commit()
    conn.close()
