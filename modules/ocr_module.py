import os
from tkinter import filedialog, Tk
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Función para seleccionar un archivo PDF
def select_pdf_file():
    """Abre un cuadro de diálogo para seleccionar un archivo PDF."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")],
        initialdir="C:/Users/TRAUCO TELLO/Downloads",
    )
    root.destroy()
    return file_path


# Función para extraer el texto de cada página y guardar las imágenes
def extract_text_and_save_images(pdf_path, output_dir):
    """Extrae texto de un archivo PDF usando OCR y guarda las imágenes de las páginas."""
    pdf_document = fitz.open(pdf_path)

    # Verificar si el directorio de salida existe, si no, crearlo
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extracted_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Convierte la página a imagen
        pix = page.get_pixmap()
        image_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(image_bytes))

        # Guardar la imagen en el directorio de salida
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        image.save(image_path)
        print(f"Página {page_num + 1} guardada como imagen: {image_path}")

        # Realizar OCR sobre la imagen
        image_text = pytesseract.image_to_string(image)

        # Guardar el texto extraído de la página
        extracted_text += f"--- Página {page_num + 1} ---\n{image_text}\n"

    pdf_document.close()
    return extracted_text


# Función para guardar el texto extraído en un archivo .txt
def save_text_to_file(text, filename):
    """Guarda el texto extraído en un archivo de texto."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Texto guardado en: {filename}")


# Función principal para ejecutar todo el proceso
def process_pdf():
    # Seleccionamos el archivo PDF
    pdf_path = select_pdf_file()

    if pdf_path:
        # Definir el directorio de salida para las imágenes
        output_dir = "output_docs"

        # Extraer texto y guardar imágenes
        extracted_text = extract_text_and_save_images(pdf_path, output_dir)

        # Guardar el texto extraído en un archivo .txt
        text_filename = os.path.join(output_dir, "extracted_text.txt")
        save_text_to_file(extracted_text, text_filename)


if __name__ == "__main__":
    process_pdf()
