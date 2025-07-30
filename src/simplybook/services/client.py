from typing import Dict, Any, Optional, List
import httpx
from ..http_client import LoggingHTTPClient

class ServicesClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_services(self, search: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de servicios
        
        Args:
            search: Texto de búsqueda
            
        Returns:
            Dict con la lista paginada de servicios
        """
        params = {}
        if search:
            params["filter"] = {"search": search}
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/services", params=params)
            response.raise_for_status()
            return response.json()

    async def get_service(self, service_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de un servicio
        
        Args:
            service_id: ID del servicio
            
        Returns:
            Dict con los detalles del servicio
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/services/{service_id}")
            response.raise_for_status()
            return response.json()

    async def get_service_products(self,
                                 service_id: str,
                                 product_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener productos asociados a un servicio
        
        Args:
            service_id: ID del servicio
            product_type: Tipo de producto ('product' o 'attribute')
            
        Returns:
            Dict con la lista de productos y sus cantidades por defecto
        """
        params = {
            "filter": {
                "service_id": service_id
            }
        }
        
        if product_type:
            params["filter"]["type"] = product_type
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/services/products", params=params)
            response.raise_for_status()
            return response.json()

    async def create_service(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo servicio
        
        Args:
            service_data: Datos del servicio (name, description, price, etc.)
            
        Returns:
            Dict con los detalles del servicio creado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/services", json=service_data)
            response.raise_for_status()
            return response.json()

    async def update_service(self, service_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar un servicio existente
        
        Args:
            service_id: ID del servicio
            service_data: Datos actualizados del servicio
            
        Returns:
            Dict con los detalles del servicio actualizado
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/services/{service_id}", json=service_data)
            response.raise_for_status()
            return response.json()

    async def delete_service(self, service_id: str) -> None:
        """
        Eliminar un servicio
        
        Args:
            service_id: ID del servicio
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/services/{service_id}")
            response.raise_for_status()

    async def get_categories(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de categorías
        
        Returns:
            Lista de objetos CategoryEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/categories")
            response.raise_for_status()
            return response.json()

    async def get_performers_list(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de performers/proveedores según la documentación
        Usa getUnitList() como se muestra en la documentación
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/providers")
            response.raise_for_status()
            return response.json()

    async def get_first_working_day(self, performer_id: str) -> Dict[str, Any]:
        """
        Obtener el primer día laboral para un performer específico
        Usa getFirstWorkingDay() como se muestra en la documentación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/units/{performer_id}/first-working-day",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_work_calendar(self, year: int, month: int, performer_id: str) -> Dict[str, Any]:
        """
        Obtener calendario de trabajo para un performer
        Usa getWorkCalendar() como se muestra en la documentación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/units/{performer_id}/work-calendar",
                headers=self.headers,
                params={
                    "year": year,
                    "month": month
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_time_slots(self, date: str, service_id: str, performer_id: str) -> List[Dict[str, Any]]:
        """
        Obtener slots de tiempo disponibles
        Usa getTimeSlots() como se muestra en la documentación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/time-slots",
                headers=self.headers,
                params={
                    "date": date,
                    "event_id": service_id,
                    "unit_id": performer_id
                }
            )
            response.raise_for_status()
            return response.json()

    async def create_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear una reserva
        Usa addBooking() como se muestra en la documentación
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/bookings",
                json=booking_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_bookings(self, date_from: str = None, date_to: str = None) -> List[Dict[str, Any]]:
        """
        Obtener reservas
        Usa getBookingList() como se muestra en la documentación
        """
        params = {}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/bookings", params=params)
            response.raise_for_status()
            return response.json()

    async def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """
        Cancelar una reserva
        Usa cancelBooking() como se muestra en la documentación
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/bookings/{booking_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()