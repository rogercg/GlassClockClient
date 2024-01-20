from datetime import timedelta
import tkinter as tk
from ttkbootstrap import Style
# from tkinter.tix import Meter
from tkinter.ttk import Button, Combobox, Entry, Label
import traceback
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta

from collections import defaultdict


class ConfigWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("480x350+1000+500")  # Tamaño y posición
        Style(theme='darkly')  # Tema

        self.title("GlassClock")

        # Título
        title_label = Label(self, text="Inicio de sesión", bootstyle="light", font=("Arial", 20))
        title_label.pack(pady=(10, 0), padx=(10, 10), fill="x")

        # Descripción
        description_label = Label(self, text="Su empleador le debe de haber enviado un correo con sus credenciales.", bootstyle="light", font=("Arial", 10))
        description_label.pack(pady=(10, 10), padx=(10, 10), fill="x")

        # Título
        space = Label(self, text="", bootstyle="light", font=("Arial", 10))
        space.pack(pady=(0, 0), padx=(10, 10), fill="x")

        # Correo electrónico
        email_label = Label(self, text="Correo electrónico", bootstyle="light")
        email_label.pack(fill="x", padx=10)
        email_entry = Entry(self, bootstyle="secondary")
        email_entry.pack(pady=(0, 10), padx=10, fill="x")

        # Contraseña
        password_label = Label(self, text="Contraseña", bootstyle="light")
        password_label.pack(fill="x", padx=10)
        password_entry = Entry(self, bootstyle="secondary", show="*")
        password_entry.pack(pady=(0, 0), padx=10, fill="x")

        space = Label(self, text="", bootstyle="light", font=("Arial", 10))
        space.pack(pady=(0, 0), padx=(10, 10), fill="x")

        # Botones
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=(0, 5), fill="x")
        login_button = Button(button_frame, text="INGRESAR", bootstyle="success", width=26)
        login_button.pack(side=tk.LEFT, fill="x", padx=(10, 10), expand=True)
        cancel_button = Button(button_frame, text="CANCELAR", bootstyle="secondary", width=26)
        cancel_button.pack(side=tk.RIGHT, fill="x", padx=(10, 10), expand=True)

        # Enlace para recuperar clave
        recover_password_label = ttk.Label(self, text="Recuperar clave", bootstyle="light", cursor="hand2")
        recover_password_label.pack(pady=(5, 0))
        recover_password_label.bind("<Button-1>", self.on_recover_password_clicked)

    def on_recover_password_clicked(self, event):
        # Aquí puedes agregar la lógica para manejar la recuperación de clave
        print("Recuperar clave clickeado")

    def on_closing(self):
        self.is_listening = False  # Detener el hilo de reconocimiento de audio
        self.destroy()


if __name__ == "__main__":
    try:
        window = ConfigWindow()
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.mainloop()
    except Exception as e:
        with open('error_log.txt', 'w') as f:
            f.write(str(e) + "\n")
            f.write(traceback.format_exc())

