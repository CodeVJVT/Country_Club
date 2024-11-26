import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import fitz  # PyMuPDF
from database import create_database, save_page_data
from classify_module import classify_document
import pytesseract
import io
import cv2
import numpy as np
import re

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image, scale_factor=2):
    """Aplica mejoras a la imagen y aumenta la resolución."""
    width, height = image.size
    image = image.resize((width * scale_factor, height * scale_factor), Image.LANCZOS)
    gray = image.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)
    gray = gray.filter(ImageFilter.MedianFilter(size=3))
    img_np = np.array(gray)
    _, img_thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(img_thresh)


def clean_extracted_text(text):
    """Limpia errores comunes en el texto extraído por OCR."""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"ACTUALZACION", "ACTUALIZACION", text, flags=re.IGNORECASE)
    text = re.sub(r"TRUNLLO", "TRUJILLO", text, flags=re.IGNORECASE)
    text = re.sub(r"[^\w\s,.@]", "", text)
    return text


class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Clasificador de Documentos PDF con Navegación y Previsualización"
        )

        create_database()

        self.pdf_document = None
        self.current_page = 0
        self.zoom_scale = 1.0
        self.rotation_angle = 0

        # Botón para seleccionar el PDF
        self.select_button = tk.Button(
            root, text="Seleccionar PDF", command=self.select_and_load_pdf
        )
        self.select_button.pack(pady=10)

        # Canvas para mostrar la imagen
        self.canvas = tk.Canvas(root, width=300, height=400)
        self.canvas.pack(pady=10)

        # Navegación entre páginas
        nav_frame = tk.Frame(root)
        self.prev_button = tk.Button(
            nav_frame, text="<< Página Anterior", command=self.prev_page
        )
        self.next_button = tk.Button(
            nav_frame, text="Página Siguiente >>", command=self.next_page
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack(side=tk.LEFT, padx=5)
        nav_frame.pack()

        # Etiqueta para mostrar la página actual
        self.page_label = tk.Label(root, text="Página: 0 / 0")
        self.page_label.pack(pady=5)

        # Controles de zoom y rotación
        zoom_frame = tk.Frame(root)
        self.zoom_in_button = tk.Button(zoom_frame, text="Zoom +", command=self.zoom_in)
        self.zoom_out_button = tk.Button(
            zoom_frame, text="Zoom -", command=self.zoom_out
        )
        self.rotate_button = tk.Button(
            zoom_frame, text="Rotar", command=self.rotate_image
        )

        self.zoom_in_button.pack(side=tk.LEFT, padx=5)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)
        self.rotate_button.pack(side=tk.LEFT, padx=5)
        zoom_frame.pack(pady=5)

        # Área de texto para mostrar el texto extraído y clasificado
        self.text_box = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=80, height=20
        )
        self.text_box.pack(padx=10, pady=10)

        # Botones para guardar resultados
        self.save_button = tk.Button(
            root, text="Guardar Resultados", command=self.save_results
        )
        self.save_button.pack(pady=5)

        self.save_all_button = tk.Button(
            root, text="Guardar Todo en la BD", command=self.save_all_to_database
        )
        self.save_all_button.pack(pady=5)

    def select_and_load_pdf(self):
        """Selecciona y carga el archivo PDF."""
        file_path = filedialog.askopenfilename(
            title="Seleccione un archivo PDF", filetypes=[("Archivos PDF", "*.pdf")]
        )
        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.current_page = 0
            self.zoom_scale = 1.0
            self.rotation_angle = 0
            self.display_page()

    def display_page(self):
        """Muestra la página actual del PDF."""
        if self.pdf_document:
            page = self.pdf_document[self.current_page]
            pix = page.get_pixmap()
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            preprocessed_image = preprocess_image(image, scale_factor=5)
            self.show_preview(preprocessed_image)
            custom_config = r"--oem 3 --psm 6"
            text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
            text = clean_extracted_text(text)
            category = classify_document(text)

            # Mostrar el texto y la categoría en el área de texto
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"--- Página {self.current_page + 1} ---\n")
            self.text_box.insert(tk.END, f"Categoría: {category}\n")
            self.text_box.insert(tk.END, f"Texto:\n{text}\n")

            self.page_label.config(
                text=f"Página: {self.current_page + 1} / {len(self.pdf_document)}"
            )

            save_page_data(self.current_page + 1, category, text)

    def save_all_to_database(self):
        """Guarda todas las páginas del PDF actual en la base de datos."""
        if self.pdf_document:
            for page_num in range(len(self.pdf_document)):
                page = self.pdf_document[page_num]
                pix = page.get_pixmap()
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                preprocessed_image = preprocess_image(image, scale_factor=5)
                custom_config = r"--oem 3 --psm 6"
                text = pytesseract.image_to_string(
                    preprocessed_image, config=custom_config
                )
                text = clean_extracted_text(text)
                category = classify_document(text)
                save_page_data(page_num + 1, category, text)

            print(f"Todas las páginas del PDF han sido guardadas en la base de datos.")
        else:
            print("No se ha cargado ningún PDF.")

    def show_preview(self, image):
        """Muestra una vista previa de la imagen en el canvas."""
        img_rotated = image.rotate(self.rotation_angle, expand=True)
        img_resized = img_rotated.resize(
            (int(300 * self.zoom_scale), int(400 * self.zoom_scale))
        )
        img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

    def next_page(self):
        """Muestra la siguiente página del PDF."""
        if self.pdf_document and self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.display_page()

    def prev_page(self):
        """Muestra la página anterior del PDF."""
        if self.pdf_document and self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def zoom_in(self):
        """Aumenta el zoom."""
        self.zoom_scale += 0.1
        self.display_page()

    def zoom_out(self):
        """Disminuye el zoom."""
        if self.zoom_scale > 0.1:
            self.zoom_scale -= 0.1
            self.display_page()

    def rotate_image(self):
        """Rota la imagen de la página."""
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.display_page()

    def save_results(self):
        """Guarda los resultados en un archivo de texto."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
            title="Guardar Resultados",
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_box.get(1.0, tk.END))
            print(f"Resultados guardados en: {file_path}")


# Iniciar la aplicación
root = tk.Tk()
app = PDFViewerApp(root)
root.mainloop()
