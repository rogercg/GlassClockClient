import os
import uuid
import requests
import json
import socket
import getpass

# Obtén la información del sistema
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
mac_address = ':'.join(['{:02x}'.format((uuid.UUID(int=uuid.getnode())).fields[-1] & 0xff) for _ in range(6)])
user_name = getpass.getuser()


# Función para enviar los datos del reporte
def send_report(data):
    # Obtén la información del sistema (esto puede ir en una función separada)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.UUID(int=uuid.getnode())).fields[-1] & 0xff) for _ in range(6)])
    user_name = getpass.getuser()

    # Lee el contenido del archivo de reporte
    with open('report-2-horas.txt', 'r', encoding='utf-8', errors='replace') as file:
        file_content = file.read()

    # Prepara los datos para enviar
    data = {
        'report_content': file_content,
        'system_info': {
            'hostname': hostname,
            'ip_address': ip_address,
            'mac_address': mac_address,
            'user_name': user_name
        },
        'user_info': {
            'company_id': data.company_id,
            'email': data.email
        }
    }

    headers = {'Authorization': f'Bearer {data.token}'}
    response = requests.post('http://localhost:3000/api/register_log', json=data, headers=headers)
    print('Respuesta del servidor:', response.text)

    # Borrar el archivo de reporte si el envío fue exitoso
    if response.status_code == 200:
        os.remove('report-2-horas.txt')

