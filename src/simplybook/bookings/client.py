import httpx
from typing import Optional, Dict, Any, List

class BookingsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_bookings_list(self) -> List[Dict[str, Any]]:
        """Obtener lista de reservas"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/bookings",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def create_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear una nueva reserva"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/bookings", 
                json=booking_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def edit_booking(self, booking_id: str, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Editar una reserva existente"""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/bookings/{booking_id}",
                json=booking_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_booking_details(self, booking_id: str) -> Dict[str, Any]:
        """Obtener detalles de una reserva específica"""
        # Obtener todas las reservas y filtrar por ID
        bookings = await self.get_bookings_list()
        for booking in bookings:
            if str(booking.get('id')) == str(booking_id):
                return booking
        raise ValueError(f"Reserva con ID {booking_id} no encontrada")

    async def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """Cancelar una reserva"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/bookings/{booking_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def approve_booking(self, booking_id: str) -> Dict[str, Any]:
        """Aprobar una reserva"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/bookings/{booking_id}/approve",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_available_slots(self, service_id: str, date: str) -> Dict[str, Any]:
        """Obtener horarios disponibles para un servicio en una fecha"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/time-slots",
                params={
                    "event_id": service_id,
                    "date": date
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_calendar_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Obtener datos del calendario para un período"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/bookings",
                params={
                    "date_from": start_date,
                    "date_to": end_date
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()