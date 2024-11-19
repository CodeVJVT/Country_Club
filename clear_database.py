import sqlite3

def clear_table():
    """Elimina todos los datos de la tabla 'documentos'."""
    conn = sqlite3.connect('document_data.db')
    cursor = conn.cursor()
    
    # Vaciar la tabla
    cursor.execute("DELETE FROM documentos")
    conn.commit()
    
    # Reiniciar el contador de IDs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='documentos'")
    conn.commit()
    
    conn.close()
    print("Todos los datos de la tabla 'documentos' han sido eliminados.")

if __name__ == "__main__":
    clear_table()
