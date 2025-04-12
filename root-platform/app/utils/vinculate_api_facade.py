# vinculate_api_facade.py

import requests
import os

class VinculateApiFacade:
    BASE_URL = 'https://api-vinculate.atlas.com.co/prod/back/api'
    HEADERS = {
        'Authorization': f'Bearer {os.getenv("VINCULATE_API_TOKEN")}',
        'Content-Type': 'application/json'
    }

    @staticmethod
    def get(endpoint, params=None):
        url = f"{VinculateApiFacade.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, headers=VinculateApiFacade.HEADERS, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch from Vinculate API: {e}")
