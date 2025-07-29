from typing import Dict, Any, List
import httpx

class ProductsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_products_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}products",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}products/{product_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_service_addons(self, service_id: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}services/{service_id}/addons",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()