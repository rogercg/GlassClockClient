import tkinter as tk
from tkinter import Label, Text
from tkinter.ttk import Button
import requests  # Biblioteca para consumir el endpoint

class FeedbackWindow(tk.Toplevel):
    def __init__(self, response, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response  # Guardar la respuesta del login
        self.geometry("700x500+800+300")  # Tamaño y posición: Alto x Ancho + X + Y
        self.resizable(False, False)  # No se puede cambiar el tamaño
        self.title("Análisis Personalizado de Productividad")

        # Título atractivo
        Label(self, text="Tu productividad en un vistazo", font=("Arial", 20, "bold")).pack(pady=20)

        # Descripción guía
        Label(
            self,
            text="Basado en tu actividad reciente, podré generar un análisis de tu rendimiento\n"
                 "y consejos personalizados para mejorar tu productividad.",
            font=("Arial", 12),
            wraplength=550,
            justify="center"
        ).pack(pady=10)

        # Área para mostrar el feedback generado
        Label(self, text="Feedback Personalizado:", font=("Arial", 12, "bold")).pack(pady=5, anchor="w", padx=20)

        self.feedback_area = Text(self, wrap="word", height=8, width=60, state="disabled", bg="#f0f0f0", font=("Arial", 10))
        self.feedback_area.pack(pady=10, padx=20, fill="both", expand=False)

        # Botón para solicitar feedback
        self.analyze_button = Button(
            self, width=20,
            text="Solicitar Feedback",
            bootstyle="success",
            command=self.generate_feedback
        )
        self.analyze_button.pack(pady=15)

        # Botón para salir
        Button(self, width=20, text="Salir", bootstyle="danger", command=self.destroy).pack(pady=10)

        # Mensaje inicial
        self.load_initial_feedback()

    def load_initial_feedback(self):
        """
        Muestra un mensaje inicial en el área de texto.
        """
        initial_feedback = "Presiona el botón 'Solicitar Feedback' para generar tu análisis personalizado."
        self.update_feedback_area(initial_feedback)

    def generate_feedback(self):
        """
        Consume el endpoint para obtener el feedback personalizado.
        """
        try:
            # URL del endpoint
            url = "http://localhost:3000/api/generate_feedback"  # Reemplaza con tu API real

            # Datos necesarios del response
            token = self.response.get("token")
            email = self.response["data"].get("email")
            company_id = self.response["data"].get("company_id")

            # Headers para la autenticación
            headers = {'Authorization': f'Bearer {token}'}

            # Payload con datos necesarios
            payload = {
                "email": email,
                "company_id": company_id
            }

            # Realiza la solicitud POST
            response = requests.post(url, json=payload, headers=headers)

            print("print(response.json()): ")
            print(response.json())

            if response.status_code == 200:
                # Si la respuesta es exitosa, extraer el feedback
                feedback = response.json().get("feedback", "No se pudo obtener el feedback.")
                self.update_feedback_area(feedback)
            else:
                # Si la solicitud falla, mostrar un mensaje de error
                self.update_feedback_area("Error al obtener el feedback. Intenta de nuevo más tarde.")
        except Exception as e:
            # Manejo de errores generales
            self.update_feedback_area(f"Error de conexión: {str(e)}")

    def update_feedback_area(self, feedback_text):
        """
        Actualiza el área de texto con el feedback proporcionado.
        """
        self.feedback_area.config(state="normal")  # Habilitar edición temporalmente
        self.feedback_area.delete("1.0", tk.END)  # Limpiar el área de texto
        self.feedback_area.insert("1.0", feedback_text)  # Insertar el nuevo feedback
        self.feedback_area.config(state="disabled")  # Deshabilitar edición nuevamente
