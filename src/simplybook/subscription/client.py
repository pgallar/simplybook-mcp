from typing import Dict, Any
import httpx

class SubscriptionClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://user-api-v2.simplybook.me/admin/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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