from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class NotesClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_notes(self,
                       page: Optional[int] = None,
                       on_page: Optional[int] = None,
                       providers: Optional[List[str]] = None,
                       services: Optional[List[str]] = None,
                       types: Optional[List[str]] = None,
                       search: Optional[str] = None,
                       date_from: Optional[str] = None,
                       date_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de notas
        
        Args:
            page: Número de página
            on_page: Elementos por página
            providers: Lista de IDs de proveedores
            services: Lista de IDs de servicios
            types: Lista de IDs de tipos de notas
            search: Texto de búsqueda
            date_from: Fecha desde
            date_to: Fecha hasta
            
        Returns:
            Dict con la lista paginada de notas
        """
        params = {}
        filters = {}
        
        if page is not None:
            params["page"] = page
            
        if on_page is not None:
            params["on_page"] = on_page
            
        if providers:
            filters["providers"] = providers
            
        if services:
            filters["services"] = services
            
        if types:
            filters["types"] = types
            
        if search:
            filters["search"] = search
            
        if date_from:
            filters["date_from"] = date_from
            
        if date_to:
            filters["date_to"] = date_to
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/calendar-notes", params=params)
            response.raise_for_status()
            return response.json()

    async def get_note(self, note_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de una nota
        
        Args:
            note_id: ID de la nota
            
        Returns:
            Dict con los detalles de la nota
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/calendar-notes/{note_id}")
            response.raise_for_status()
            return response.json()

    async def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear una nueva nota
        
        Args:
            note_data: Datos de la nota (provider_id, service_id, start_date_time, etc.)
            
        Returns:
            Dict con los detalles de la nota creada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/calendar-notes", json=note_data)
            response.raise_for_status()
            return response.json()

    async def edit_note(self, note_id: str, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Editar una nota existente
        
        Args:
            note_id: ID de la nota
            note_data: Datos actualizados de la nota
            
        Returns:
            Dict con los detalles de la nota actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/calendar-notes/{note_id}", json=note_data)
            response.raise_for_status()
            return response.json()

    async def delete_note(self, note_id: str) -> None:
        """
        Eliminar una nota
        
        Args:
            note_id: ID de la nota
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/calendar-notes/{note_id}")
            response.raise_for_status()

    async def get_note_types(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de tipos de notas
        
        Returns:
            Lista de objetos CalendarNoteTypeEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/calendar-notes/types")
            response.raise_for_status()
            return response.json()

    async def get_default_note_type(self) -> Dict[str, Any]:
        """
        Obtener tipo de nota predeterminado
        
        Returns:
            Dict con el tipo de nota predeterminado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/calendar-notes/types/default")
            response.raise_for_status()
            return response.json()