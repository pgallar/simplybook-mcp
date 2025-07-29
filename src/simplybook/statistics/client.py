from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx

class StatisticsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://user-api-v2.simplybook.me/admin/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_statistics(self, 
                           start_date: str, 
                           end_date: str, 
                           provider_id: Optional[str] = None,
                           service_id: Optional[str] = None) -> Dict[str, Any]:
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        if provider_id:
            params["provider_id"] = provider_id
        if service_id:
            params["service_id"] = service_id

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}statistics",
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_detailed_report(self, report_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}statistics/reports/{report_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def generate_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}statistics/reports",
                json=report_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()