import sqlite3


def inspect_data():
    """Imprime el contenido de la tabla documentos para verificar el texto almacenado."""
    conn = sqlite3.connect("document_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, pagina, categoria, texto FROM documentos")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Página: {row[1]}, Categoría: {row[2]}")
            print(f"Texto:\n{row[3][:500]}\n{'-'*50}")
    else:
        print("No hay datos en la tabla documentos.")


if __name__ == "__main__":
    inspect_data()
