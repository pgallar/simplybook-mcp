from typing import Dict, Any, List
import httpx

class CouponsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
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