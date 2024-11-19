from tkinter import filedialog, Tk
import fitz  # PyMuPDF
import pandas as pd
from PIL import Image
import pytesseract
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def select_pdf_file():
    """Abre un cuadro de diálogo para seleccionar un archivo PDF."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleccione un archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")],
        initialdir="C:/Users/TuUsuario/Downloads",
    )
    root.destroy()
    return file_path


def split_pdf_by_pages(pdf_path, output_dir):
    """Divide un PDF en páginas individuales y las guarda como archivos PDF separados."""
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        output_pdf = fitz.open()
        output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        output_path = f"{output_dir}/socio_page_{page_num + 1}.pdf"
        output_pdf.save(output_path)
        output_pdf.close()
        print(f"Página {page_num + 1} guardada en: {output_path}")

    pdf_document.close()
    print(f"Todas las páginas fueron separadas y guardadas en: {output_dir}")


def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF usando OCR."""
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        image_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(image_bytes))

        image = image.resize((image.width * 2, image.height * 2))
        page_text = pytesseract.image_to_string(image)
        extracted_text += f"--- Página {page_num + 1} ---\n{page_text}\n"

    pdf_document.close()
    return extracted_text


def create_training_data(label_csv, output_csv):
    """Genera un conjunto de datos con texto extraído de PDFs y sus etiquetas."""
    data = pd.read_csv(label_csv)
    texts, categories = [], []

    for index, row in data.iterrows():
        pdf_text = extract_text_from_pdf(row["file_path"])
        texts.append(pdf_text)
        categories.append(row["categoria"])

    training_data = pd.DataFrame({"texto": texts, "categoria": categories})
    training_data.to_csv(output_csv, index=False)
    print(f"Conjunto de datos guardado en: {output_csv}")
