from src.controllers.auth import auth_token
from src.utils.database import establish_connection
import requests
import json

def ins_productividad():
    cabeceras = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Auth-Token': auth_token()
    }
    try:
        res =  requests.post('https://scdi.saas-solinftec.com/push', data = establish_connection(), headers=cabeceras)
        print(f"el estado es: {res.status_code}")
        # print(f"el envio es: {res.json()}")
        return res.json()
    except requests.exceptions.HTTPError as err:
        print(err)