from apps.reports.models import TokenSiigo
from requests.exceptions import ReadTimeout
import os
import json
import requests
from apps.companies.models import Company, Credential
from django.contrib.sessions.models import Session
from dotenv import load_dotenv
load_dotenv()

HEADERS = {
    'Content-Type': 'application/json',
    'Partner-Id': os.getenv('SIGO_APP')
}

def siigo_connection(request):
    user = request.user
        
    company = user.company
    credentials = Credential.objects.get(company=company) 
    
    user_siigo = credentials.user_siigo
    access_key = credentials.secret_key_siigo

    session = requests.Session()
    values = f'''
        {{
            "username": "{user_siigo}",
            "access_key": "{access_key}"
        }}
        '''
    response = session.post('https://api.siigo.com/auth', data=values, headers=HEADERS)
    if response.status_code == 200:
        token = response.json()
        return token['access_token']
    else:
        return False

            
def request_type(type, url, headers, value):
    session = requests.Session()
    timeout = 180

    if type == "get":
        response = session.get(url=url, headers=headers, timeout=timeout)
    elif type == "post":
        response = session.post(url=url, headers=headers, data=value, timeout=timeout)
    elif type == "put":
        response = session.put(url=url, headers=headers, data=value, timeout=timeout)
    elif type == "delete":
        response = session.delete(url=url, headers=headers, data=value, timeout=timeout)

    return response

def execute_request(url, values, type, request):
    token = siigo_connection(request)
    if not token:
        return {"status": False, "error": "No se pudo obtener el token de autenticación"}

    headers = HEADERS.copy()
    headers["Authorization"] = token

    try:
        response = request_type(type, url, headers=headers, value=values)
        response.raise_for_status()
    except ReadTimeout:
        return {"status": False, "error": "SIIGO tardó más de 3 minutos en responder, intente de nuevo más tarde"}
    except requests.exceptions.RequestException as e:
        return {"status": False, "error": str(e)}

    if response.status_code not in [200, 201]:
        errors = response.json().get("Errors", [{"Code": "Error interno", "Message": "Error interno de SIIGO"}])[0]
        return {"status": False, "error": errors["Message"]}

    return {"status": True, "data": response.json()}
