from typing import Dict, Any, Optional, List
import httpx
from ..http_client import LoggingHTTPClient

class ClientsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_clients(self, 
                       page: Optional[int] = None,
                       on_page: Optional[int] = None,
                       search: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de clientes con paginación y filtros
        
        Args:
            page: Número de página
            on_page: Elementos por página
            search: Texto de búsqueda
            
        Returns:
            Dict con la lista paginada de clientes
        """
        params = {}
        
        if page is not None:
            params["page"] = page
            
        if on_page is not None:
            params["on_page"] = on_page
            
        if search:
            params["filter"] = {"search": search}
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/clients", params=params)
            response.raise_for_status()
            return response.json()

    async def get_client(self, client_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de un cliente específico
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Dict con los detalles del cliente
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/clients/{client_id}")
            response.raise_for_status()
            return response.json()

    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo cliente
        
        Args:
            client_data: Datos del cliente (name, email, phone)
            
        Returns:
            Dict con los datos del cliente creado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/clients", json=client_data)
            response.raise_for_status()
            return response.json()

    async def edit_client(self, client_id: str, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Editar un cliente existente
        
        Args:
            client_id: ID del cliente
            client_data: Datos actualizados del cliente
            
        Returns:
            Dict con los datos del cliente actualizado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/clients/{client_id}", json=client_data)
            response.raise_for_status()
            return response.json()

    async def delete_client(self, client_id: str) -> None:
        """
        Eliminar un cliente
        
        Args:
            client_id: ID del cliente
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/clients/{client_id}")
            response.raise_for_status()

    async def get_client_memberships(self,
                                   page: Optional[int] = None,
                                   on_page: Optional[int] = None,
                                   client_id: Optional[str] = None,
                                   service_id: Optional[str] = None,
                                   service_start_date: Optional[str] = None,
                                   count: Optional[int] = None,
                                   active_only: Optional[bool] = None,
                                   search: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de membresías de clientes
        
        Args:
            page: Número de página
            on_page: Elementos por página
            client_id: Filtrar por ID de cliente
            service_id: Filtrar por ID de servicio
            service_start_date: Filtrar por fecha de inicio
            count: Cantidad de reservas grupales
            active_only: Solo membresías activas
            search: Texto de búsqueda
            
        Returns:
            Dict con la lista paginada de membresías
        """
        params = {}
        filters = {}
        
        if page is not None:
            params["page"] = page
            
        if on_page is not None:
            params["on_page"] = on_page
            
        if client_id:
            filters["client_id"] = client_id
            
        if service_id:
            filters["service_id"] = service_id
            
        if service_start_date:
            filters["service_start_date"] = service_start_date
            
        if count is not None:
            filters["count"] = count
            
        if active_only is not None:
            filters["active_only"] = 1 if active_only else 0
            
        if search:
            filters["search"] = search
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/clients/memberships", params=params)
            response.raise_for_status()
            return response.json()

    async def get_client_fields(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de campos de cliente
        
        Returns:
            Lista de objetos Client_FieldDetailsEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/clients/fields")
            response.raise_for_status()
            return response.json()

    async def get_client_field_values(self, client_id: str) -> Dict[str, Any]:
        """
        Obtener valores de campos de un cliente
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Dict con los valores de los campos del cliente
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/clients/field-values/{client_id}")
            response.raise_for_status()
            return response.json()

    async def edit_client_fields(self, client_id: str, field_values: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Editar valores de campos de un cliente
        
        Args:
            client_id: ID del cliente
            field_values: Lista de valores de campos actualizados
            
        Returns:
            Dict con los valores actualizados de los campos
        """
        data = {
            "id": client_id,
            "fields": field_values
        }
        
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/clients/field-values/{client_id}", json=data)
            response.raise_for_status()
            return response.json()

    async def create_client_with_fields(self, field_values: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Crear un cliente con valores de campos personalizados
        
        Args:
            field_values: Lista de valores de campos
            
        Returns:
            Dict con los datos del cliente creado
        """
        data = {
            "id": None,
            "fields": field_values
        }
        
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/clients/field-values", json=data)
            response.raise_for_status()
            return response.json()