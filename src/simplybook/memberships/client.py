from typing import Dict, Any, List
import httpx

class MembershipsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://user-api-v2.simplybook.me/admin/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def make_membership_instance(self, membership_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}memberships/instances",
                json=membership_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def cancel_membership(self, instance_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}memberships/instances/{instance_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_memberships_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}memberships",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()