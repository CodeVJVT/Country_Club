def classify_document(text):
    """Clasifica el texto extraído en una categoría."""
    if "penal" in text.lower():
        return "Reporte Penal"
    elif "infocorp" in text.lower():
        return "Reporte Infocorp"
    elif "tributario" in text.lower():
        return "Reporte Tributario"
    elif "carta" in text.lower():
        return "Carta"
    else:
        return "Desconocido"
