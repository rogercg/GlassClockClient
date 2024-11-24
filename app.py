from datetime import timedelta
from functools import partial
import os
import platform
import sys
import threading
import tkinter as tk
from ttkbootstrap import Style
# from tkinter.tix import Meter
from tkinter.ttk import Button, Combobox, Entry, Label
import traceback
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime, timedelta

from collections import defaultdict
from clock import monitor_apps

from login_service import activate_clock, login

import pystray
from pystray import Menu, MenuItem

import pystray
from pystray import MenuItem as item

from PIL import Image

from monitoring import detener_ejecucion_monitoreo, obtener_estado_monitoreo, start_monitoring



basedir = None

# Detecta si la aplicación se está ejecutando como un .exe o como un script Python
if getattr(sys, 'frozen', False):
    # Si se ejecuta como .exe, usa el directorio temporal de PyInstaller
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)

monitoring_lock = threading.Lock()

class AppWindow(tk.Tk):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.geometry("480x350+1000+500")  # Tamaño y posición
        self.resizable(False, False)  # No se puede cambiar el tamaño
        Style(theme='darkly')  # Tema

        self.title("GlassClock")

        self.icono_bandeja = None

        # self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Accede al archivo icon.ico usando el directorio 
        if platform.system() == 'Windows':
            icon_path = os.path.join(basedir, 'favicon.ico')
            self.iconbitmap(icon_path)
        else:
            icon_path = os.path.join(basedir, 'favicon.xbm')

        # Título
        title_label = Label(self, text="Inicio de sesión", bootstyle="light", font=("Arial", 20))
        title_label.pack(pady=(10, 0), padx=(20, 20), fill="x")

        # Descripción
        description_label = Label(self, text="Su empleador le debe de haber enviado un correo con sus credenciales.", bootstyle="light", font=("Arial", 10))
        description_label.pack(pady=(10, 10), padx=(20, 20), fill="x")

        # Título
        space = Label(self, text="", bootstyle="light", font=("Arial", 10))
        space.pack(pady=(0, 0), padx=(20, 20), fill="x")

        # Correo electrónico
        self.email_label = Label(self, text="Correo electrónico", bootstyle="light")
        self.email_label.pack(fill="x", padx=20)
        self.email_entry = Entry(self, bootstyle="secondary")
        self.email_entry.pack(pady=(0, 10), padx=20, fill="x")

        # Contraseña
        self.password_label = Label(self, text="Contraseña", bootstyle="light")
        self.password_label.pack(fill="x", padx=20)
        self.password_entry = Entry(self, bootstyle="secondary", show="*")
        self.password_entry.pack(pady=(0, 0), padx=20, fill="x")

        space = Label(self, text="", bootstyle="light", font=("Arial", 10))
        space.pack(pady=(0, 0), padx=(20, 20), fill="x")

        # Botones
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=(0, 5), fill="x")
        login_button = Button(button_frame, text="INGRESAR", bootstyle="success", width=26)
        login_button.pack(side=tk.LEFT, fill="x", padx=(10, 10), expand=True)
        login_button.bind("<Button-1>", self.on_login_clicked)
        cancel_button = Button(button_frame, text="CANCELAR", bootstyle="secondary", width=26)
        cancel_button.pack(side=tk.RIGHT, fill="x", padx=(10, 10), expand=True)

        # Enlace para recuperar clave
        recover_password_label = ttk.Label(self, text="Recuperar clave", bootstyle="light", cursor="hand2")
        recover_password_label.pack(pady=(5, 0))
        recover_password_label.bind("<Button-1>", self.on_recover_password_clicked)

        self.is_stop_monitoring = False
        self.option_menu_status_change = "Detener"
    
    # Acción a realizar cuando se intente cerrar la ventana
    def on_closing(self):
        self.withdraw()  # Ocultar la ventana
        self.create_tray_icon()  # Crear y mostrar el ícono en la bandeja del sistema

    def cerrar_aplicacion(self):
        if self.icono_bandeja:
            self.icono_bandeja.stop()  # Detener el ícono de la bandeja
        self.destroy()  # Cerrar la 
        
    def actualizar_menu_tray_icon(self):
        if self.is_stop_monitoring:
            texto_item_monitoreo = "Iniciar"
        else:
            texto_item_monitoreo = "Detener"

        # Define las funciones de los ítems del menú aquí dentro para capturar el contexto actual
        def show_window(icon, item):
            icon.stop()
            self.icono_bandeja = None
            self.after(0, self.deiconify)

        def exit_icon(icon, item):
            icon.stop()
            self.quit()

        # Actualiza el menú del ícono de la bandeja
        self.icono_bandeja.menu = pystray.Menu(
            item(texto_item_monitoreo, self.detener_monitoreo),
            item('Mostrar', show_window),
            item('Salir', exit_icon)
        )

        # Actualiza el ícono para reflejar los cambios
        self.icono_bandeja.update_menu()

    

    def detener_monitoreo(self, icon, item):
        # Detener el monitoreo: modificar el valor de status.json
        self.is_stop_monitoring = not self.is_stop_monitoring
        detener_ejecucion_monitoreo(self.is_stop_monitoring)
        # Llama a actualizar_menu_tray_icon para reflejar el cambio en el menú
        self.actualizar_menu_tray_icon()

    def create_tray_icon(self):
        def exit_icon(icon, item):
            icon.stop()
            window.quit()  # Termina el bucle principal de tkinter
            # self.destroy()  # Destruye la ventana
        
        
        def show_window(icon, item):
            icon.stop()
            self.icono_bandeja = None  # Resetear el ícono de la bandeja
            self.after(0, self.deiconify)  # Mostrar la ventana
        
        # Cargar la imagen usando PIL
        image_path = os.path.join(basedir, 'favicon-32x32.png')
        image = Image.open(image_path)
        # image = Image.open("favicon-32x32.png")  # Asegúrate de tener un icono adecuado
        if self.is_stop_monitoring:
            self.option_menu_status_change = "Iniciar"
        else:
            self.option_menu_status_change = "Detener"
        
        # menu_item_detener_monitoreo = partial(detener_monitoreo, self)  # Aquí se usa partial para pasar `self`

        self.icono_bandeja = pystray.Icon("test_icon", image, "Mi Aplicación", menu=pystray.Menu(
            item(self.option_menu_status_change, self.detener_monitoreo),
            item('Mostrar', show_window),
            item('Salir', exit_icon)))


        icon_thread = threading.Thread(target=self.icono_bandeja.run)
        icon_thread.start()
    
    def on_login_clicked(self, event):
        # Aquí puedes agregar la lógica para manejar el inicio de sesión
        print("Ingresar clickeado")
        login_data = {
            'email': self.email_entry.get(),
            'password': self.password_entry.get()
        }
        response = login(login_data)
        activate = activate_clock(response)
        # activate = activate_clock(response)
        print("activate:")
        print(activate)
        if(response):
            # self.destroy()
            self.on_closing()
            if not obtener_estado_monitoreo() or activate["data"]:
                # Llama a la función para comenzar el monitoreo            
                start_monitoring(monitor_apps, response["data"]["hours_x_day"], response, activate["data"], self)
            else:
                print("El monitoreo ya está en ejecución.")

            # # Iniciar el monitoreo
            # monitoring_thread = start_monitoring(monitor_apps, response["data"]["hours_x_day"], response)

            # # Para cerrar la aplicación y el hilo después de 8 horas:
            # monitoring_thread.join(timeout=8*3600)  # Tiempo en segundos

            # # Si el hilo sigue vivo después de 8 horas, detenerlo
            # if monitoring_thread.is_alive():
            #     monitor_apps.stop_thread = True
            #     monitoring_thread.join()
            
    # Función para iniciar el monitoreo en un hilo
    # def start_monitoring(self, response):
    #     with monitoring_lock:
    #         if not hasattr(self, 'monitoring_thread') or not self.monitoring_thread.is_alive():
    #             self.monitoring_thread = threading.Thread(
    #                 target=monitor_apps,
    #                 args=(response["data"]["hours_x_day"], response,)
    #             )
    #             self.monitoring_thread.start()
    #         else:
    #             print("El monitoreo ya está en ejecución.")
    #     return self.monitoring_thread

    def on_recover_password_clicked(self, event):
        # Aquí puedes agregar la lógica para manejar la recuperación de clave
        print("Recuperar clave clickeado")


if __name__ == "__main__":
    try:
        window = AppWindow()
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.mainloop()
    except Exception as e:
        with open('error_log.txt', 'w') as f:
            f.write(str(e) + "\n")
            f.write(traceback.format_exc())

