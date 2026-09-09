import json

import requests
#It would be better to have a different project to test API
class BettingAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/") + '/api'

    def place_bet(self, payload: dict, header):
        return requests.post(self.base_url + '/place-bet',headers=header, json=payload)


    def get_matches(self, header):
        return requests.get(self.base_url + '/matches',headers=header)

    def get_balance(self, header):
        return requests.get(self.base_url + '/balance',headers=header )

    def reset_balance(self, header):
        return requests.post(self.base_url + '/reset-balance', headers=header)
