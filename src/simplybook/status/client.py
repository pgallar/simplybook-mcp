from typing import Dict, Any, List
from ..http_client import LoggingHTTPClient

class StatusClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_statuses(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de estados
        
        Returns:
            Lista de objetos StatusEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/statuses")
            response.raise_for_status()
            return response.json() 