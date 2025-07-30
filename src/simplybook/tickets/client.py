from typing import Dict, Any
from ..http_client import LoggingHTTPClient

class TicketsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_ticket(self, code: str) -> Dict[str, Any]:
        """
        Obtener información de un ticket por código
        
        Args:
            code: Código del ticket
            
        Returns:
            Dict con los detalles del ticket (AdminTicketEntity)
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/tickets/{code}")
            response.raise_for_status()
            return response.json()

    async def check_in_ticket(self, code: str) -> Dict[str, Any]:
        """
        Validar un ticket
        
        Args:
            code: Código del ticket
            
        Returns:
            Dict con los detalles del ticket actualizado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/tickets/{code}/check-in")
            response.raise_for_status()
            return response.json()