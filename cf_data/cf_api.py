from abc import ABC

import requests

from settings import BASE_URL


class APIClient:
    @staticmethod
    def get():
        #theo = {}
        items = []
        response = requests.get(BASE_URL)
        response.raise_for_status()
        '''for keys, _ in response.json()['result'].items():
            items.append(keys)
        return items
        '''
        return response.json()['result']
        #return response.json()['result']['problems']
        #return response.json()['result']['problemStatistics']

