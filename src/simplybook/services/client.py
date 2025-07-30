from typing import Dict, Any, List, Optional
import httpx
from ..http_client import LoggingHTTPClient

class ServicesClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_services_list(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de servicios según la documentación de SimplyBook.me
        Usa getEventList() como se muestra en la documentación
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/services")
            response.raise_for_status()
            return response.json()

    async def get_service(self, service_id: str) -> Dict[str, Any]:
        """
        Obtener información de un servicio específico
        """
        # Primero obtener la lista completa y filtrar
        services = await self.get_services_list()
        for service in services:
            if str(service.get('id')) == str(service_id):
                return service
        raise ValueError(f"Servicio con ID {service_id} no encontrado")

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