import hmac
import hashlib
import time
import requests
from typing import Dict, Any, Optional

class OmnibookExchange:
    """
    Custom Exchange Adapter for connecting OctoBot to Omnibook.
    Handles HMAC-SHA256 signature generation, REST requests, 
    account balances, and 60-second BTC prediction orders.
    """

    BASE_URL = "https://www.omnibook.xyz/api/v1"  # Replace with exact target API route if needed

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def _generate_signature(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """
        Generates HMAC SHA256 signature required by API headers.
        """
        message = f"{timestamp}{method.upper()}{path}{body}"
        return hmac.new(
            self.api_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _get_headers(self, method: str, path: str, body: str = "") -> Dict[str, str]:
        """
        Constructs standard authentication headers for requests.
        """
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp, method, path, body)

        return {
            "Content-Type": "application/json",
            "OMNIBOOK-API-KEY": self.api_key,
            "OMNIBOOK-SIGNATURE": signature,
            "OMNIBOOK-TIMESTAMP": timestamp,
        }

    def request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Executes an authenticated HTTP request to Omnibook.
        """
        url = f"{self.BASE_URL}{endpoint}"
        body_str = json.dumps(data) if data else ""
        headers = self._get_headers(method, endpoint, body_str)

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data if data else None,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    # --- Exchange Methods ---

    def get_account_balance(self) -> Dict[str, Any]:
        """
        Retrieves user testnet balance and active positions.
        """
        return self.request("GET", "/user/balance")

    def get_market_data(self, symbol: str = "BTC") -> Dict[str, Any]:
        """
        Fetches current market price and active round status.
        """
        return self.request("GET", f"/markets/{symbol}/current")

    def place_prediction(self, direction: str, amount: float, symbol: str = "BTC") -> Dict[str, Any]:
        """
        Places a 60-second binary prediction order ('UP' or 'DOWN').
        """
        payload = {
            "symbol": symbol,
            "direction": direction.upper(),
            "amount": amount
        }
        return self.request("POST", "/orders/prediction", data=payload)
