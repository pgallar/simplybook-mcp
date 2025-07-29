from typing import Dict, Any
import httpx

class SubscriptionClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_subscription_info(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}subscription",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_subscription_limits(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}subscription/limits",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()