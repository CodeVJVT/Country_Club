import pandas as pd

def export_results_to_excel(results, filename="resultados.xlsx"):
    """Exporta los resultados a un archivo Excel."""
    df = pd.DataFrame(results, columns=["ID", "Página", "Categoría", "Texto"])
    df.to_excel(filename, index=False)
    print(f"Resultados exportados a {filename}")
