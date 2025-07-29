from typing import Dict, Any, List, Optional
import httpx

class PaymentsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://user-api-v2.simplybook.me/admin/"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_orders_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}orders",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}orders/{order_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_payment_link(self, order_id: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}orders/{order_id}/payment-link",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()["payment_link"]

    async def accept_payment(self, order_id: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}orders/{order_id}/accept-payment",
                json=payment_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def apply_promo_code(self, order_id: str, promo_code: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}orders/{order_id}/promo-code",
                json={"code": promo_code},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_saved_payment_methods(self, client_id: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}clients/{client_id}/payment-methods",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()