'''
Auth:
    1. Generate "X-Device-ID" header:
        It is random string of 16 symbols length. It can contain only lowercase english symbols and digits.

    2. Get city list:
        GET /api/v1/catalog/cities?modified=1602174362 HTTP/1.1 
        X-Device-ID: cb6b9ee38d65b0a2 
        X-Device-Model: LLD-L31 
        X-Platform: Android 
        X-OS-Version: 28 
        X-Language: en_US 
        X-App-Version: 7.5.1 
        X-Build-Number: 3357 
        X-Cellular-Name: MegaFon 
        X-Timezone: GMT+03:00 
        X-Appsflyer-ID: 1606427792425-5386367759305992358 
        Host: mobile-api.mcdonalds.ru 
        Connection: Keep-Alive 
        Accept-Encoding: gzip 
        User-Agent: okhttp/3.12.1

        It returns us an object of cities list in JSON format. We must take city ID from it.

    3. Get Session token:
        POST /api/v1/device/city HTTP/1.1 
        X-Device-ID: cb6b9ee38d65b0a2 
        X-Device-Model: LLD-L31 
        X-Platform: Android 
        X-OS-Version: 28 
        X-Language: en_US 
        X-App-Version: 7.5.1 
        X-Build-Number: 3357 
        X-Cellular-Name: MegaFon 
        X-City-ID: 5dfc9fd451f0dc92455bee95 
        X-Timezone: GMT+03:00 
        X-Appsflyer-ID: 1606427792425-5386367759305992358 
        Content-Type: application/json; charset=UTF-8 
        Content-Length: 33 
        Host: mobile-api.mcdonalds.ru 
        Connection: Keep-Alive 
        Accept-Encoding: gzip 
        User-Agent: okhttp/3.12.1 
         
        {"id":"5dfc9fd451f0dc92455bee95"}


        It returns us 

'''


import requests
import string
import random
import json

from loguru import logger

app_versions = [
    '7.5.1',
    '7.5.4',
    '7.4.0',
    '7.3.1',
    '7.2.1'
]




class McDonaldsSession:
    def __init__(self):
        self.api_host = 'https://mobile-api.mcdonalds.ru'
        self.sess = requests.session()
        self.headers = {
            # Generate random device ID.
            'X-Device-ID': ''.join([random.choice(string.digits+string.ascii_lowercase) for _ in range(16)]),
            # Generate random device model.
            'X-Device-Model': ''.join([random.choice(string.digits) for _ in range(8)]),
            'X-Platform': 'Android',
            'X-OS-Version': '28',
            'X-Language': 'en_US',
            'X-App-Version': '7.5.1',
            'X-Build-Number': '3357',
            'X-Cellular-Name': 'Megafon',
            'X-Timezone': 'GMT+03:00',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'

         }
        self.is_logged_in = False

    def get_cities_list(self):
        api_method = '/api/v1/catalog/cities'
        answer = self.sess.get(url=self.api_host+api_method, headers=self.headers)
        return answer.json()

    def get_bearer_sess_token(self):
        cities_id = [city['id'] for city in self.get_cities_list()['items']]
        random_city_id = random.choice(cities_id)

        self.headers['X-City-ID'] = random_city_id
        api_method = '/api/v1/device/city'

        _headers = self.headers.copy()
        _headers['Content-Type'] = 'application/json; charset=UTF-8'
        answer = self.sess.post(
            url=self.api_host+api_method,
            headers=_headers,
            data=json.dumps({'id': random_city_id})
        )

        token = answer.json()['token']
        self.headers['Authorization'] = 'Bearer ' + token

    def get_login_code(self, phone):
        # phone in format +70000000000
        api_method = '/api/v1/user/login/phone'
        _headers = self.headers.copy()
        _headers['Content-Type'] = 'application/json; charset=UTF-8'
        data = json.dumps({'phone': phone})
        answer = self.sess.post(
            url=self.api_host+api_method,
            headers=_headers,
            data=data
        )
        return answer.json()

    def verify_code(self, ticket, code):
        api_method = '/api/v1/user/login/phone/confirm'
        _headers = self.headers.copy()
        _headers['Content-Type'] = 'application/json; charset=UTF-8'
        data = json.dumps({'code': code, 'ticket': ticket})
        answer = self.sess.post(
            url=self.api_host+api_method,
            headers=_headers,
            data=data
        )
        self.headers['Authorization'] = 'Bearer ' + answer.json()['token']
        self.is_logged_in = True
        return True


if __name__ == '__main__':
    mc = McDonaldsSession()






