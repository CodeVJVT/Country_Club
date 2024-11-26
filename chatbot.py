import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
from database import (
    query_database,
    query_by_category,
)  # Asegúrate de que query_database devuelva la página
from export import export_results_to_excel
from logs import log_query, get_statistics
from feedback import collect_feedback
from utils import show_help

# Inicializamos el pipeline de pregunta-respuesta
qa_pipeline = pipeline(
    "question-answering", model="distilbert-base-cased-distilled-squad"
)


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de Consulta Documental")

        # Pantalla de chat
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=80, height=20, state="disabled"
        )
        self.chat_display.pack(padx=10, pady=10)

        # Entrada del usuario
        self.user_input = tk.Entry(root, width=70)
        self.user_input.pack(pady=5)
        self.user_input.bind("<Return>", self.send_message)

        # Botones de enviar y salir
        button_frame = tk.Frame(root)
        self.send_button = tk.Button(
            button_frame, text="Enviar", command=self.send_message
        )
        self.exit_button = tk.Button(button_frame, text="Salir", command=self.root.quit)
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.exit_button.pack(side=tk.LEFT, padx=5)
        button_frame.pack()

    def send_message(self, event=None):
        """Envía el mensaje del usuario y muestra la respuesta del bot."""
        user_text = self.user_input.get().strip()
        if user_text:
            self.display_message(f"Tú: {user_text}")
            response = self.handle_command(user_text)
            self.display_message(f"Bot: {response}")
            self.user_input.delete(0, tk.END)

    def handle_command(self, command):
        """Maneja los comandos del usuario."""
        if command.lower() == "ayuda":
            return show_help()
        elif command.startswith("Categoría:"):
            category = command.split(":", 1)[1].strip()
            results = query_by_category(category)
            return f"Resultados para la categoría '{category}': {len(results)} encontrados."
        elif command.startswith("Exportar"):
            results = query_database("")  # Exporta todo
            export_results_to_excel(results)
            return "Resultados exportados."
        elif command.startswith("Estadísticas"):
            stats = get_statistics()
            return f"Consultas más frecuentes: {stats}"
        elif command.startswith("Feedback"):
            _, response_id, rating, *comments = command.split(",")
            collect_feedback(int(response_id), int(rating), " ".join(comments))
            return "Gracias por tu feedback."
        else:
            return self.chatbot_response(
                command
            )  # Llamar a la función chatbot_response

    def chatbot_response(self, command):
        """Genera una respuesta utilizando el modelo de QA de transformers."""
        context, pages = (
            self.get_document_context()
        )  # Obtener el contexto (texto completo de los documentos)

        # Usar el modelo de QA para obtener una respuesta
        result = qa_pipeline(question=command, context=context)

        # Buscar las páginas relevantes para la respuesta
        relevant_pages = self.get_relevant_pages(command, pages)

        # Devolver la respuesta generada junto con las páginas relevantes
        return f"{result['answer']}\n(Encontrado en las páginas: {', '.join(map(str, relevant_pages))})"

    def get_document_context(self):
        """Recupera el texto completo de los documentos para usarlo como contexto y las páginas asociadas."""
        documents = query_database("")  # Recupera todos los documentos

        context = []
        pages = []

        for doc in documents:
            text = doc[3]  # Asumimos que el texto está en la columna 3
            context.append(text)  # Agrega el texto del documento al contexto
            pages.append(
                doc[1]
            )  # Asumimos que el número de la página está en la columna 1

        return (
            "\n".join(context),
            pages,
        )  # Devuelve el texto combinado y las páginas correspondientes

    def get_relevant_pages(self, question, pages):
        """Obtiene las páginas relevantes en las que se encuentra la respuesta."""
        relevant_pages = []

        # Aquí buscamos en el contexto (texto completo de los documentos) si la respuesta contiene fragmentos de la pregunta
        # Simplemente buscamos la pregunta en el texto de cada página
        context, _ = self.get_document_context()
        for i, page_text in enumerate(context):
            if (
                question.lower() in page_text.lower()
            ):  # Si el texto de la página contiene la pregunta
                relevant_pages.append(pages[i])  # Agregamos la página correspondiente

        return relevant_pages

    def display_message(self, message):
        """Muestra el mensaje en el área de chat."""
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")


# Crear la ventana principal de la aplicación
root = tk.Tk()
app = ChatbotApp(root)
root.mainloop()
