# Recibir los parametros del login(credenciales) e invocar al back para devolverle la repsuesta al invocador
import requests
import time
import os
import json
import socket
import getpass
import uuid

# URL de tu API para el inicio de sesión y para enviar el reporte
LOGIN_URL = 'https://glass-clock-27bb4a1792ef.herokuapp.com/api/signin'
ACTIVATE_URL = 'https://glass-clock-27bb4a1792ef.herokuapp.com/api/signin'
# 'http://localhost:3000/api/signin'

# Datos de inicio de sesión del usuario

# Función para realizar el inicio de sesión
def login(login_data):
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code == 200:
        print('Inicio de sesión exitoso')
        print('data:', response.json())
        return response.json()  # Retorna el token si el inicio de sesión es exitoso
    else:
        print('Error de inicio de sesión:', response.text)
        return None
    
def activate_clock(user_data):
    headers = {'Authorization': f'Bearer {user_data["token"]}'}
    response = requests.post(ACTIVATE_URL, json=user_data, headers=headers)
    if response.status_code == 200:
        print('Inicio de sesión exitoso')
        print('data:', response.json())
        return response.json()  # Retorna el token si el inicio de sesión es exitoso
    else:
        print('Error de inicio de sesión:', response.text)
        return None