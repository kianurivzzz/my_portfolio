import requests
from config import TOKEN



def call_tg(text):
    url =  f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'text' : text,
        'chat_id': 5353106736
    }

    headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json'
    }

    return requests.post(url, json=payload, headers=headers)
