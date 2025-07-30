from typing import Dict, Any, List, Optional
from ..base_routes import BaseRoutes
from .client import BookingsClient
from pydantic import Field
from typing import Annotated

class BookingsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool()
        async def get_bookings_list() -> Dict[str, Any]:
            """Obtener lista de reservas (método básico)"""
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

        @mcp.tool(
            description="Obtener lista de reservas con filtros avanzados",
            tags={"bookings", "filters"}
        )
        async def get_booking_list(
            page: Optional[Annotated[int, Field(description="Número de página para paginación", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None,
            upcoming_only: Optional[Annotated[bool, Field(description="Solo reservas futuras")]] = None,
            status: Optional[Annotated[str, Field(description="Estado de la reserva", pattern="^(confirmed|confirmed_pending|pending|canceled)$")]] = None,
            services: Optional[Annotated[List[str], Field(description="Lista de IDs de servicios para filtrar")]] = None,
            providers: Optional[Annotated[List[str], Field(description="Lista de IDs de proveedores para filtrar")]] = None,
            client_id: Optional[Annotated[str, Field(description="ID del cliente para filtrar")]] = None,
            date: Optional[Annotated[str, Field(description="Fecha para filtrar (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            search: Optional[Annotated[str, Field(description="String de búsqueda (por código, datos del cliente)")]] = None,
            additional_fields: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            """
            Obtener lista de reservas con filtros avanzados.
            
            Args:
                page: Número de página para paginación
                on_page: Elementos por página
                upcoming_only: Solo reservas futuras
                status: Estado de la reserva (confirmed/confirmed_pending/pending/canceled)
                services: Lista de IDs de servicios para filtrar
                providers: Lista de IDs de proveedores para filtrar
                client_id: ID del cliente para filtrar
                date: Fecha para filtrar (YYYY-MM-DD)
                search: String de búsqueda (por código, datos del cliente)
                additional_fields: Campos adicionales para filtrar
            
            Returns:
                Dict con la respuesta paginada de reservas
            """
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = BookingsClient(self.get_auth_headers())
                result = await self.client.get_booking_list(
                    page=page,
                    on_page=on_page,
                    upcoming_only=upcoming_only,
                    status=status,
                    services=services,
                    providers=providers,
                    client_id=client_id,
                    date=date,
                    search=search,
                    additional_fields=additional_fields
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo reservas filtradas: {str(e)}"}

        @mcp.tool(
            description="Crear una nueva reserva",
            tags={"bookings", "create"}
        )
        async def create_booking(
            booking_data: Annotated[Dict[str, Any], Field(
                description="Datos de la reserva",
                example={
                    "service_id": "123",
                    "start_datetime": "2024-03-20 10:00:00",
                    "client_id": "456",
                    "provider_id": "789",
                    "notes": "Notas adicionales"
                }
            )]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Editar una reserva existente",
            tags={"bookings", "edit"}
        )
        async def edit_booking(
            booking_id: Annotated[str, Field(description="ID de la reserva a editar")],
            booking_data: Annotated[Dict[str, Any], Field(
                description="Datos actualizados de la reserva",
                example={
                    "service_id": "123",
                    "start_datetime": "2024-03-20 10:00:00",
                    "provider_id": "789",
                    "notes": "Notas actualizadas"
                }
            )]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Obtener detalles de una reserva específica",
            tags={"bookings", "details"}
        )
        async def get_booking_details(
            booking_id: Annotated[str, Field(description="ID de la reserva")]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Cancelar una reserva",
            tags={"bookings", "cancel"}
        )
        async def cancel_booking(
            booking_id: Annotated[str, Field(description="ID de la reserva a cancelar")]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Aprobar una reserva",
            tags={"bookings", "approve"}
        )
        async def approve_booking(
            booking_id: Annotated[str, Field(description="ID de la reserva a aprobar")]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Obtener horarios disponibles para un servicio en una fecha",
            tags={"bookings", "slots"}
        )
        async def get_available_slots(
            service_id: Annotated[str, Field(description="ID del servicio")],
            date: Annotated[str, Field(description="Fecha para buscar slots (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]
        ) -> Dict[str, Any]:
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

        @mcp.tool(
            description="Obtener datos del calendario para un período",
            tags={"bookings", "calendar"}
        )
        async def get_calendar_data(
            start_date: Annotated[str, Field(description="Fecha de inicio (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")],
            end_date: Annotated[str, Field(description="Fecha de fin (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]
        ) -> Dict[str, Any]:
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