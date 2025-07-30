from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class ProvidersClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_providers(self,
                          search: Optional[str] = None,
                          service_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de proveedores
        
        Args:
            search: Texto de búsqueda
            service_id: Filtrar por servicio (solo proveedores que pueden dar este servicio)
            
        Returns:
            Dict con la lista paginada de proveedores
        """
        params = {}
        filters = {}
        
        if search:
            filters["search"] = search
            
        if service_id:
            filters["service_id"] = service_id
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/providers", params=params)
            response.raise_for_status()
            return response.json()

    async def get_provider(self, provider_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de un proveedor
        
        Args:
            provider_id: ID del proveedor
            
        Returns:
            Dict con los detalles del proveedor
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/providers/{provider_id}")
            response.raise_for_status()
            return response.json()

    async def create_provider(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo proveedor
        
        Args:
            provider_data: Datos del proveedor (name, qty, email, etc.)
            
        Returns:
            Dict con los detalles del proveedor creado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/providers", json=provider_data)
            response.raise_for_status()
            return response.json()

    async def update_provider(self, provider_id: str, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar un proveedor existente
        
        Args:
            provider_id: ID del proveedor
            provider_data: Datos actualizados del proveedor
            
        Returns:
            Dict con los detalles del proveedor actualizado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/providers/{provider_id}", json=provider_data)
            response.raise_for_status()
            return response.json()

    async def delete_provider(self, provider_id: str) -> None:
        """
        Eliminar un proveedor
        
        Args:
            provider_id: ID del proveedor
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/providers/{provider_id}")
            response.raise_for_status()

    async def get_locations(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de ubicaciones
        
        Returns:
            Lista de objetos LocationEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/locations")
            response.raise_for_status()
            return response.json()