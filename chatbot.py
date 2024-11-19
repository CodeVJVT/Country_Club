import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
from database import query_database, query_by_category
from export import export_results_to_excel
from logs import log_query, get_statistics
from feedback import collect_feedback
from utils import show_help

qa_pipeline = pipeline(
    "question-answering", model="distilbert-base-cased-distilled-squad"
)


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot de Consulta Documental")
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=80, height=20, state="disabled"
        )
        self.chat_display.pack(padx=10, pady=10)
        self.user_input = tk.Entry(root, width=70)
        self.user_input.pack(pady=5)
        self.user_input.bind("<Return>", self.send_message)
        button_frame = tk.Frame(root)
        self.send_button = tk.Button(
            button_frame, text="Enviar", command=self.send_message
        )
        self.exit_button = tk.Button(button_frame, text="Salir", command=self.root.quit)
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.exit_button.pack(side=tk.LEFT, padx=5)
        button_frame.pack()

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text:
            self.display_message(f"Tú: {user_text}")
            response = self.handle_command(user_text)
            self.display_message(f"Bot: {response}")
            self.user_input.delete(0, tk.END)

    def handle_command(self, command):
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
            return chatbot_response(command)

    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")


root = tk.Tk()
app = ChatbotApp(root)
root.mainloop()
