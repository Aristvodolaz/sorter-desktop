import requests


class APIClient:
    BASE_URL = "http://31.128.44.48:3000/api"

    @staticmethod
    def fetch_full_info():
        response = requests.get(f"{APIClient.BASE_URL}/tm/getFullInfo")
        response.raise_for_status()
        return response.json()
