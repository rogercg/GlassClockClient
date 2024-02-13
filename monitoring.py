import threading

import os
import json

estado_monitoreo_archivo = 'status.json'

def detener_ejecucion_monitoreo(stop):
    with open(estado_monitoreo_archivo, 'w') as archivo:
        json.dump({'activo': True, 'stop': stop}, archivo)

def actualizar_estado_monitoreo(estado):
    with open(estado_monitoreo_archivo, 'w') as archivo:
        json.dump({'activo': estado, 'stop': False}, archivo)

def obtener_estado_monitoreo():
    if not os.path.exists(estado_monitoreo_archivo):
        return False
    with open(estado_monitoreo_archivo, 'r') as archivo:
        estado = json.load(archivo)
    return estado.get('activo', False)

def start_monitoring(monitor_apps, runtime_hours, data, window, activate):
    print("window: ")
    print(window)
    if not obtener_estado_monitoreo() or activate:
        actualizar_estado_monitoreo(True)
        monitoring_thread = threading.Thread(target=monitor_apps, args=(runtime_hours, data, window,))
        monitoring_thread.start()
    else:
        print("El monitoreo ya está en ejecución.")

