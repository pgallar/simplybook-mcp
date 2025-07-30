from typing import Dict, Any
from ..http_client import LoggingHTTPClient

class StatisticsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas generales
        
        Returns:
            Dict con las estadísticas:
            - Proveedor más popular y número de reservas (últimos 30 días)
            - Servicio más popular y número de reservas (últimos 30 días)
            - Número de reservas hoy
            - Número de reservas esta semana (Lunes-Domingo)
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/statistics")
            response.raise_for_status()
            return response.json()

    async def get_detailed_report(self, report_id: str) -> Dict[str, Any]:
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(
                f"{self.base_url}statistics/reports/{report_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def generate_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post(
                f"{self.base_url}statistics/reports",
                json=report_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()