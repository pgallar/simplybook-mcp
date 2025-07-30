from typing import Dict, Any, List
import httpx

class ProvidersClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_providers_list(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de proveedores según la documentación de SimplyBook.me
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/providers",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_provider(self, provider_id: str) -> Dict[str, Any]:
        """
        Obtener información de un proveedor específico
        """
        # Primero obtener la lista completa y filtrar
        providers = await self.get_providers_list()
        for provider in providers:
            if str(provider.get('id')) == str(provider_id):
                return provider
        raise ValueError(f"Proveedor con ID {provider_id} no encontrado")

    async def create_provider(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo proveedor
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/units",
                json=provider_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def update_provider(self, provider_id: str, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar un proveedor existente
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/units/{provider_id}",
                json=provider_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def delete_provider(self, provider_id: str) -> Dict[str, Any]:
        """
        Eliminar un proveedor
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/units/{provider_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_provider_locations(self, provider_id: str) -> List[Dict[str, Any]]:
        """
        Obtener ubicaciones de un proveedor
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/units/{provider_id}/locations",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()