from typing import Dict, Any, List
import httpx

class CouponsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://user-api-v2.simplybook.me/admin/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_promotions_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}promotions",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_gift_cards_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}gift-cards",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_coupons_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}coupons",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def issue_gift_card(self, gift_card_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}gift-cards",
                json=gift_card_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()