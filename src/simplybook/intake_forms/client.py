from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class IntakeFormsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_additional_fields(self, service_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de campos adicionales
        
        Args:
            service_id: ID del servicio para filtrar campos
            
        Returns:
            Dict con la lista paginada de campos adicionales
        """
        params = {}
        if service_id:
            params["filter"] = {"service_id": service_id}
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/additional-fields", params=params)
            response.raise_for_status()
            return response.json() 