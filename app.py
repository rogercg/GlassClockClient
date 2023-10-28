import time
import psutil
import datetime
import sys
import platform
import pygetwindow as gw
from datetime import datetime, timedelta    

# Diccionario para almacenar el tiempo de uso de cada aplicación
app_usage = {}
last_active_app = None
last_update_time = None

# Función para obtener el nombre de la aplicación activa en el frente
def get_active_window_title():
    active_window_name = None
    if sys.platform in ['linux', 'linux2']:
        try:
            import subprocess
            active_window_name = str(subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"]))
            active_window_pid = str(subprocess.check_output(["xprop", "-id", active_window_name.split()[5], "WM_CLIENT_MACHINE"]))
            active_window_name = active_window_pid.split('=')[1].split(',')[0].strip(' "')
        except subprocess.CalledProcessError:
            pass
    elif sys.platform in ['Windows', 'win32', 'cygwin']:
        try:
            active_window_name = gw.getActiveWindow().title
        except Exception:
            pass
    return active_window_name

start_time = datetime.now()

# Función para actualizar el reporte
def update_report():
    global app_usage, start_time, last_active_app, last_update_time

    # Calcular cuánto tiempo se gastó en la última aplicación
    end_time = datetime.now()
    time_spent = end_time - start_time

    # Agregar el tiempo gastado a la aplicación correspondiente en el diccionario de uso de la aplicación
    if last_active_app in app_usage:
        app_usage[last_active_app] += time_spent
    else:
        app_usage[last_active_app] = time_spent

    # Restablecer el tiempo de inicio para la nueva aplicación
    start_time = datetime.now()

    # Escribir el reporte a un archivo txt
    with open('report.txt', 'w') as f:
        for app, usage in app_usage.items():
            print(app, usage)
            formatted_time = str(timedelta(seconds=usage.total_seconds()))
            f.write(f'{app}| {end_time.strftime("%Y-%m-%d")}| {formatted_time}\n')

    # Actualizar el último tiempo de actualización
    last_update_time = end_time

while True:
    # Obtener la aplicación activa actualmente
    active_app = get_active_window_title()

    # Si la aplicación activa ha cambiado
    if active_app != last_active_app:
        # Calcular cuánto tiempo se gastó en la última aplicación
        end_time = datetime.now()
        time_spent = end_time - start_time

        # Agregar el tiempo gastado a la aplicación correspondiente en el diccionario de uso de la aplicación
        if last_active_app in app_usage:
            app_usage[last_active_app] += time_spent
        else:
            app_usage[last_active_app] = time_spent

        # Restablecer el tiempo de inicio para la nueva aplicación
        start_time = datetime.now()

    # Actualizar el reporte cada 3 minutos
    if last_update_time is None or (datetime.now() - last_update_time).total_seconds() >= 60:
        update_report()

    # Actualizar la última aplicación activa
    last_active_app = active_app

    time.sleep(1)
