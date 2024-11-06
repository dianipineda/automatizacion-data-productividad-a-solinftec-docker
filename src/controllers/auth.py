import requests
import json


def auth_token():
    auth_data = {
        "cliente": "carmelita",
        "password": "pz12dQthFdD*UTsjtH5b"
    }
    json_auth_data = json.dumps(auth_data, ensure_ascii=False)

    # configuracion de headers
    cabeceras = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    try:
        res = requests.post('https://scdi.saas-solinftec.com/auth/token', data = json_auth_data, headers= cabeceras)
        token = res.json()['token']
        return token
    except requests.exceptions.HTTPError as err:
        print(err)
