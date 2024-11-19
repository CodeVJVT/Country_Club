import re

def preprocess_text(text):
    """Limpia y preprocesa el texto extraído."""
    text = re.sub(r"[\‘\’\“\”]", "'", text)  # Reemplazar comillas extrañas
    text = re.sub(r"\s+", " ", text)  # Reemplazar múltiples espacios por uno
    text = re.sub(r"\n+", "\n", text)  # Eliminar saltos de línea redundantes
    return text
