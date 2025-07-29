from typing import Dict, Any
import httpx

class TicketsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_ticket_info(self, ticket_code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}tickets/{ticket_code}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def check_in_ticket(self, ticket_code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}tickets/{ticket_code}/check-in",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()