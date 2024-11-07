from src.controllers.auth import auth_token
from src.utils.database import establish_connection
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

def ins_productividad():
    cabeceras = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Auth-Token': auth_token()
    }
    try:
        res =  requests.post('https://scdi.saas-solinftec.com/push', data = establish_connection(), headers=cabeceras, verify=False)
        print(f"el estado es: {res.status_code}")
        # print(f"el envio es: {res.json()}")
        return res.json()
    except requests.exceptions.HTTPError as err:
        print(err)