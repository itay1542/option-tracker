import datetime
import logging
import os
from typing import Tuple, Iterator

import requests
from requests import HTTPError
from retry import retry

from database.models import OptionData, OptionExpirations

logger = logging.getLogger(__name__)


class TemporaryError(Exception):
    pass


class TradestationAPI:
    def __init__(self):
        self.api_key = os.getenv("TS_API_KEY")
        self.api_secret = os.getenv("TS_API_SECRET")
        self.base_url = "https://signin.tradestation.com"
        self.api_url = "https://api.tradestation.com/v3"
        self.access_token = None
        self.refresh_token = os.getenv("TS_REFRESH_TOKEN")  # Get refresh token from environment

    @retry(TemporaryError, tries=3, delay=2, backoff=2)
    def _refresh_access_token(self):
        token_url = f"{self.base_url}/oauth/token"
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'refresh_token': self.refresh_token,
        }
        response = requests.post(token_url, headers=headers, data=data)
        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.error(f"Error while refreshing access token: {err}")
            if response.status_code >= 500:
                raise TemporaryError(response.text)
            else:
                raise err

        response = response.json()
        self.access_token = response['access_token']

    @retry(TemporaryError, tries=3, delay=2, backoff=2)
    def _request_endpoint(self, endpoint, params=None):
        if not self.access_token:  # If access token is not available
            self._refresh_access_token()  # Refresh it

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(endpoint, headers=headers, params=params)
        try:
            response.raise_for_status()
        except HTTPError as err:
            logger.error(f"Error while requesting endpoint: {err}")
            if response.status_code >= 500:
                raise TemporaryError(response.text)
            elif response.status_code in (401, 403):
                self._refresh_access_token()
                self._request_endpoint(endpoint)
            else:
                raise err

        return response.json()

    async def stream_option_chain(self, symbol, expiration: datetime) -> Iterator[OptionData]:
        endpoint = f"https://api.tradestation.com/v3/marketdata/stream/options/chains/{symbol}"
        endpoint += f"?expiration={expiration.strftime('%Y-%m-%d')}"
        # todo: use aiohttp to handle the json stream
        pass

    def get_symbol_strikes(self, symbol):
        endpoint = f"{self.api_url}/marketdata/options/strikes/{symbol}"
        return self._request_endpoint(endpoint)

    def get_option_expirations(self, symbol):
        endpoint = f"{self.api_url}/marketdata/options/expirations/{symbol}"
        expirations = self._request_endpoint(endpoint)["Expirations"]
        return [
            OptionExpirations(
                datetime=datetime.datetime.fromisoformat(expiration["Date"]), type=expiration["Type"]
            ) for expiration in expirations
        ]
