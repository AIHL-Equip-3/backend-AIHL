import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Configuración de cliente y URLs
# Cargar variables de entorno desde el archivo .env
load_dotenv()

CLIENT_ID = "gencat.vass.cat"
CLIENT_SECRET = "bc41139f-1546-4076-ba4b-00b0ef509ea1"
AUTH_URL = "https://identitats-pre.aoc.cat/o/oauth2/auth"
TOKEN_URL = "https://identitats-pre.aoc.cat/o/oauth2/token"
USER_INFO_URL = "https://identitats-pre.aoc.cat/serveis-rest/getUserInfo"
REDIRECT_URI = "https://identitats-pre.aoc.cat/users/auth/idcat_mobil/callback"  # Cambia si es necesario
# Solicita las credenciales
usuario = "41667838A"
telefono = "+34653554846"

# Fase 1: Solicitar autorización
def solicitar_codigo_autorizacion():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "autenticacio_usuari",
        "approval_prompt": "auto"
    }
    response = requests.get(AUTH_URL, params=params)
    print(f"Por favor, ve a esta URL para autorizar: {response.url}")
    codigo_autorizacion = input("Introduce el código de autorización que recibiste: ")
    return codigo_autorizacion

# Fase 2: Intercambiar el código por un token de acceso
def intercambiar_codigo_por_token(codigo_autorizacion):
    data = {
        "grant_type": "authorization_code",
        "code": codigo_autorizacion,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error al obtener el token de acceso:", response.json())
        return None

# Fase 3: Acceder a información de usuario con el token de acceso
def obtener_informacion_usuario(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(USER_INFO_URL, headers=headers)
    if response.status_code == 200:
        print("Información de usuario:", response.json())
    else:
        print("Error al obtener información de usuario:", response.json())

# Proceso completo de autenticación
def login():
    codigo_autorizacion = solicitar_codigo_autorizacion()
    token = intercambiar_codigo_por_token(codigo_autorizacion)
    if token:
        print("Login exitoso, obteniendo información de usuario...")
        obtener_informacion_usuario(token)
    else:
        print("Error en el proceso de login.")

# Ejecutar login
if __name__ == "__main__":
    login()
