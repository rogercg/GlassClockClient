from datetime import timedelta
import tkinter as tk
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

        self.geometry("625x480")
        # Abrir programa en el lado derecho inferior de la pc
        self.geometry("+1000+500")

        ttk.Style("darkly")

        self.title("Configuración de objetivos")

        canvas_presentation = tk.Canvas(self)
        canvas_presentation.pack()

        frame_title = tk.Frame(canvas_presentation)
        frame_title.grid(row=0, column=0, padx=0, pady=10, sticky="w")
        self.title = ttk.Label(frame_title, text="Configuración", bootstyle="success.TLabel", font=("Arial", 20))
        self.title.pack(fill="x", expand=True)

        frame_description = tk.Frame(canvas_presentation)
        frame_description.grid(row=0, column=0, padx=0, pady=10, sticky="w")
        self.description = ttk.Label(frame_title, text="Registra el nombre de tus aplicaciones a utilizar y selecciona su categoria. \nNo olvides platearte un objetivo real para recibir tu feedback inteligente.", bootstyle="light.TLabel", font=("Arial", 11))
        self.description.pack(fill="x", expand=True)

        canvas_listbox = tk.Canvas(self)
        canvas_listbox.pack()

        # Frame para Listbox y Scrollbar
        listbox_frame = tk.Frame(canvas_listbox)
        listbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=4)

        # Listbox para mostrar las aplicaciones y sus categorías
        self.apps_listbox = tk.Listbox(listbox_frame, height=10, width=75)
        self.apps_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.apps_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Scrollbar para Listbox
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.apps_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.apps_listbox.yview)

        canvas_form = tk.Canvas(self, width=200, height=200)
        canvas_form.pack()

        # App Name
        app_name_frame_form = tk.Frame(canvas_form)
        app_name_frame_form.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        Label()
        self.app_name_lbl = Label(app_name_frame_form, bootstyle="light", text="Nombre de la aplicación")
        self.app_name_lbl.pack(fill="both", expand=True) 
        Entry()
        self.app_name_txt = Entry(app_name_frame_form, width=34, bootstyle="secondary")
        self.app_name_txt.pack(fill="both", expand=True) 

        # Category Name
        app_category_frame_form = tk.Frame(canvas_form)
        app_category_frame_form.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        Label()
        self.app_name_lbl = Label(app_category_frame_form, bootstyle="light", text="Categoria de la aplicación")
        self.app_name_lbl.pack(fill="both", expand=True) 
        type_app = ["Productiva", "Neutra", "Distractora"]
        Combobox()
        self.app_type_cbo = Combobox(app_category_frame_form, width=34, values=type_app, bootstyle="secondary")
        self.app_type_cbo.pack(fill="both", expand=True)

        canvas_button = tk.Canvas(self, width=200, height=200)
        canvas_button.pack()

        # Buttons
        buttons_frame_form1 = tk.Frame(canvas_button)
        buttons_frame_form1.grid(row=4, column=0, padx=10, pady=10)
        Button()
        self.save_btn = Button(buttons_frame_form1, width=20 ,bootstyle="success", text="Agregar")
        self.save_btn.pack(fill="x", expand=True)

        buttons_frame_form2 = tk.Frame(canvas_button)
        buttons_frame_form2.grid(row=4, column=1, padx=10, pady=10)
        Button()
        self.edit_btn = Button(buttons_frame_form2, width=20, bootstyle="warning", text="Editar")
        self.edit_btn.pack(fill="x", expand=True)
        Button()

        buttons_frame_form3 = tk.Frame(canvas_button)
        buttons_frame_form3.grid(row=4, column=2, padx=10, pady=10)
        self.delete_btn = Button(buttons_frame_form3, width=20, bootstyle="danger", text="Eliminar")
        self.delete_btn.pack(fill="x", expand=True)
        
        self.load_apps()

    def load_apps(self):
        # Limpiar la Listbox
        self.apps_listbox.delete(0, tk.END)

        # Leer las aplicaciones del archivo
        apps = self.read_apps_from_file("apps.txt")
        
        # Añadir las aplicaciones a la Listbox
        for app in apps:
            app_str = f"{app['name']} - {app['category']}"
            self.apps_listbox.insert(tk.END, app_str)
    
    def read_apps_from_file(self, filename):
        apps = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(", ")
                    if len(parts) == 2:
                        app_data = {
                            "name": parts[0],
                            "category": parts[1]
                        }
                        apps.append(app_data)
        except FileNotFoundError:
            # Si el archivo no existe, simplemente devolvemos una lista vacía
            pass
        return apps

    def on_listbox_select(self, event):
        # Obtener el índice del elemento seleccionado
        index = self.apps_listbox.curselection()[0]
        app_str = self.apps_listbox.get(index)

        # Extraer el nombre y la categoría de la aplicación del string
        app_name, app_category = app_str.split(" - ")

        # Actualizar los campos con los detalles de la aplicación seleccionada
        self.app_name_txt.delete(0, tk.END)
        self.app_name_txt.insert(0, app_name)
        self.app_type_cbo.set(app_category)

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

