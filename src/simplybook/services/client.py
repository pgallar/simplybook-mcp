from typing import Dict, Any, Optional, List
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
            Dict con la lista paginada de servicios (ServiceEntity[])
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso al servicio
            NotFound: Si el servicio no existe
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
            ServiceEntity con los detalles del servicio
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso al servicio
            NotFound: Si el servicio no existe
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
            Service_ProductEntity con la lista de productos y sus cantidades por defecto
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
            service_data: ServiceWriteableEntity con los datos del servicio:
                - name: Nombre del servicio
                - description: Descripción del servicio
                - price: Precio del servicio
                - deposit_price: Precio del depósito
                - tax_id: ID del impuesto
                - duration: Duración en minutos
                - is_visible: Si el servicio es visible
            
        Returns:
            ServiceEntity con los detalles del servicio creado
            
        Throws:
            BadRequest: Si los datos proporcionados son inválidos
            AccessDenied: Si el usuario no tiene acceso para crear servicios
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/services", json=service_data)
            response.raise_for_status()
            return response.json()

    async def update_service(self, service_id: str, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar un servicio existente
        
        Args:
            service_id: ID del servicio a actualizar
            service_data: ServiceWriteableEntity con los datos del servicio:
                - name: Nombre del servicio
                - description: Descripción del servicio
                - price: Precio del servicio
                - deposit_price: Precio del depósito
                - tax_id: ID del impuesto
                - duration: Duración en minutos
                - is_visible: Si el servicio es visible
            
        Returns:
            ServiceEntity con los detalles del servicio actualizado
            
        Throws:
            BadRequest: Si los datos proporcionados son inválidos
            NotFound: Si el servicio no existe
            AccessDenied: Si el usuario no tiene acceso para actualizar el servicio
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/services/{service_id}", json=service_data)
            response.raise_for_status()
            return response.json()

    async def delete_service(self, service_id: str) -> None:
        """
        Eliminar un servicio
        
        Args:
            service_id: ID del servicio a eliminar
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso para eliminar el servicio
            NotFound: Si el servicio no existe
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

    async def get_performers(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de proveedores según la documentación
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
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
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
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
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
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
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
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
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
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(
                f"{self.base_url}/bookings/{booking_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()