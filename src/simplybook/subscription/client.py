from typing import Dict, Any
from ..http_client import LoggingHTTPClient

class SubscriptionClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_current_subscription(self) -> Dict[str, Any]:
        """
        Obtener información de la suscripción actual
        
        Returns:
            Dict con los detalles de la suscripción actual (CompanyTariffEntity)
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/tariff/current")
            response.raise_for_status()
            return response.json()