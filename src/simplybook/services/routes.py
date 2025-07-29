from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import ServicesClient

class ServicesRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool()
        async def get_services_list() -> Dict[str, Any]:
            """Obtener lista de servicios disponibles"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                services = await self.client.get_services_list()
                return {
                    "success": True,
                    "services": services,
                    "count": len(services)
                }
            except Exception as e:
                return {"error": f"Error obteniendo servicios: {str(e)}"}

        @mcp.tool()
        async def get_service(service_id: str) -> Dict[str, Any]:
            """Obtener información de un servicio específico"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                service = await self.client.get_service(service_id)
                return {
                    "success": True,
                    "service": service
                }
            except Exception as e:
                return {"error": f"Error obteniendo servicio: {str(e)}"}

        @mcp.tool()
        async def get_performers_list() -> Dict[str, Any]:
            """Obtener lista de performers/proveedores"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                performers = await self.client.get_performers_list()
                return {
                    "success": True,
                    "performers": performers,
                    "count": len(performers)
                }
            except Exception as e:
                return {"error": f"Error obteniendo performers: {str(e)}"}

        @mcp.tool()
        async def get_first_working_day(performer_id: str) -> Dict[str, Any]:
            """Obtener el primer día laboral para un performer"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                working_day = await self.client.get_first_working_day(performer_id)
                return {
                    "success": True,
                    "first_working_day": working_day
                }
            except Exception as e:
                return {"error": f"Error obteniendo día laboral: {str(e)}"}

        @mcp.tool()
        async def get_work_calendar(year: int, month: int, performer_id: str) -> Dict[str, Any]:
            """Obtener calendario de trabajo para un performer"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                calendar = await self.client.get_work_calendar(year, month, performer_id)
                return {
                    "success": True,
                    "work_calendar": calendar
                }
            except Exception as e:
                return {"error": f"Error obteniendo calendario: {str(e)}"}

        @mcp.tool()
        async def get_time_slots(date: str, service_id: str, performer_id: str) -> Dict[str, Any]:
            """Obtener slots de tiempo disponibles"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                time_slots = await self.client.get_time_slots(date, service_id, performer_id)
                return {
                    "success": True,
                    "time_slots": time_slots,
                    "count": len(time_slots)
                }
            except Exception as e:
                return {"error": f"Error obteniendo slots de tiempo: {str(e)}"}

        @mcp.tool()
        async def get_bookings(date_from: str = None, date_to: str = None) -> Dict[str, Any]:
            """Obtener reservas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                bookings = await self.client.get_bookings(date_from, date_to)
                return {
                    "success": True,
                    "bookings": bookings,
                    "count": len(bookings)
                }
            except Exception as e:
                return {"error": f"Error obteniendo reservas: {str(e)}"}