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

# Lee el contenido del archivo
with open('report.txt', 'r') as file:
    file_content = file.read()

# Prepara los datos para enviar
data = {
    'report_content': file_content,
    'system_info': {
        'hostname': hostname,
        'ip_address': ip_address,
        'mac_address': mac_address,
        'user_name': user_name,
        'company_id': '652b33d66dc78a4ee90ebfbb'
    }
}

json_data = json.dumps(data)

print(json_data)

# URL del endpoint de tu API
url = 'https://0dv9jpokia.execute-api.us-east-1.amazonaws.com/glass_clock_register_log'

# Envía una solicitud POST a la API
response = requests.post(url, json=data)

# Imprime la respuesta
print(response.text)

