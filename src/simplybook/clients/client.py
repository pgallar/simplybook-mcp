from typing import Dict, Any, Optional, List
import httpx

class ClientsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_clients_list(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/clients",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        # Obtener todos los clientes y filtrar por ID
        clients = await self.get_clients_list()
        for client in clients:
            if str(client.get('id')) == str(client_id):
                return client
        raise ValueError(f"Cliente con ID {client_id} no encontrado")

    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/clients",
                json=client_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def edit_client(self, client_id: str, client_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/clients/{client_id}",
                json=client_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def delete_client(self, client_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/clients/{client_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()