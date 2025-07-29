from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import BookingsClient

class BookingsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool()
        async def get_bookings_list() -> Dict[str, Any]:
            """Obtener lista de reservas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                bookings = await self.client.get_bookings_list()
                return {
                    "success": True,
                    "bookings": bookings,
                    "count": len(bookings)
                }
            except Exception as e:
                return {"error": f"Error obteniendo reservas: {str(e)}"}

        @mcp.tool()
        async def create_booking(booking_data: Dict[str, Any]) -> Dict[str, Any]:
            """Crear una nueva reserva"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                result = await self.client.create_booking(booking_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando reserva: {str(e)}"}

        @mcp.tool()
        async def edit_booking(booking_id: str, booking_data: Dict[str, Any]) -> Dict[str, Any]:
            """Editar una reserva existente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                result = await self.client.edit_booking(booking_id, booking_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error editando reserva: {str(e)}"}

        @mcp.tool()
        async def get_booking_details(booking_id: str) -> Dict[str, Any]:
            """Obtener detalles de una reserva específica"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                booking = await self.client.get_booking_details(booking_id)
                return {
                    "success": True,
                    "booking": booking
                }
            except Exception as e:
                return {"error": f"Error obteniendo detalles de reserva: {str(e)}"}

        @mcp.tool()
        async def cancel_booking(booking_id: str) -> Dict[str, Any]:
            """Cancelar una reserva"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                result = await self.client.cancel_booking(booking_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error cancelando reserva: {str(e)}"}

        @mcp.tool()
        async def approve_booking(booking_id: str) -> Dict[str, Any]:
            """Aprobar una reserva"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                result = await self.client.approve_booking(booking_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error aprobando reserva: {str(e)}"}

        @mcp.tool()
        async def get_available_slots(service_id: str, date: str) -> Dict[str, Any]:
            """Obtener horarios disponibles para un servicio en una fecha"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                slots = await self.client.get_available_slots(service_id, date)
                return {
                    "success": True,
                    "slots": slots
                }
            except Exception as e:
                return {"error": f"Error obteniendo horarios: {str(e)}"}

        @mcp.tool()
        async def get_calendar_data(start_date: str, end_date: str) -> Dict[str, Any]:
            """Obtener datos del calendario para un período"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                calendar_data = await self.client.get_calendar_data(start_date, end_date)
                return {
                    "success": True,
                    "calendar_data": calendar_data
                }
            except Exception as e:
                return {"error": f"Error obteniendo datos del calendario: {str(e)}"}