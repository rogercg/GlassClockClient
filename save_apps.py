import uuid
import requests
import json
import socket
import getpass

# Prepara los datos para enviar
data = {
    "companyId": "algunaIDdeCompañia",
    "applications": [
        {
            "application_name": "Youtube",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "Google Chrome",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Visual Studio Code",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Discord",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "Spotify",
            "application_type_id": "652b16c65b0cfc8cd1a722fa"
        },
        {
            "application_name": "Microsoft Teams",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Zoom",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Dota",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "League of Legends",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "Whatsapp",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "Twitter",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "X",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "Instagram",
            "application_type_id": "652b16c65b0cfc8cd1a722f9"
        },
        {
            "application_name": "AWS",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Amazon",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        },
        {
            "application_name": "Azure",
            "application_type_id": "652b16c65b0cfc8cd1a722f8"
        }
    ]
}


print(data)

# URL del endpoint de tu API
url = 'https://0dv9jpokia.execute-api.us-east-1.amazonaws.com/glass_clock_register_log'

# Envía una solicitud POST a la API
response = requests.post(url, json=data)

# Imprime la respuesta
print(response.text)

