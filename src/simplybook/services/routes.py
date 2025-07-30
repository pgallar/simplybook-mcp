from typing import Dict, Any, Optional
from ..base_routes import BaseRoutes
from .client import ServicesClient
from pydantic import Field
from typing import Annotated

class ServicesRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de servicios disponibles",
            tags={"services", "list"}
        )
        async def get_services(
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de servicios disponibles"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_services(search=search)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo servicios: {str(e)}"}

        @mcp.tool(
            description="Obtener información de un servicio específico",
            tags={"services", "details"}
        )
        async def get_service(
            service_id: Annotated[str, Field(description="ID del servicio")]
        ) -> Dict[str, Any]:
            """Obtener información de un servicio específico"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_service(service_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo servicio: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de proveedores",
            tags={"providers", "list"}
        )
        async def get_performers(
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de proveedores"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_performers()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo proveedores: {str(e)}"}

        @mcp.tool(
            description="Obtener el primer día laboral para un proveedor",
            tags={"providers", "schedule"}
        )
        async def get_first_working_day(
            provider_id: Annotated[str, Field(description="ID del proveedor")]
        ) -> Dict[str, Any]:
            """Obtener el primer día laboral para un proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_first_working_day(provider_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo día laboral: {str(e)}"}

        @mcp.tool(
            description="Obtener calendario de trabajo para un proveedor",
            tags={"providers", "calendar"}
        )
        async def get_work_calendar(
            year: Annotated[int, Field(description="Año", ge=2000, le=2100)],
            month: Annotated[int, Field(description="Mes (1-12)", ge=1, le=12)],
            provider_id: Annotated[str, Field(description="ID del proveedor")]
        ) -> Dict[str, Any]:
            """Obtener calendario de trabajo para un proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_work_calendar(year, month, provider_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo calendario: {str(e)}"}

        @mcp.tool(
            description="Obtener slots de tiempo disponibles",
            tags={"services", "slots"}
        )
        async def get_time_slots(
            date: Annotated[str, Field(description="Fecha (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")],
            service_id: Annotated[str, Field(description="ID del servicio")],
            provider_id: Annotated[str, Field(description="ID del proveedor")]
        ) -> Dict[str, Any]:
            """Obtener slots de tiempo disponibles"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_time_slots(date, service_id, provider_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo slots de tiempo: {str(e)}"}

        @mcp.tool(
            description="Obtener reservas",
            tags={"bookings", "list"}
        )
        async def get_bookings(
            date_from: Optional[Annotated[str, Field(description="Fecha inicial (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            date_to: Optional[Annotated[str, Field(description="Fecha final (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None
        ) -> Dict[str, Any]:
            """Obtener reservas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_bookings(date_from, date_to)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo reservas: {str(e)}"}

        @mcp.tool(
            description="Obtener productos asociados a un servicio",
            tags={"services", "products"}
        )
        async def get_service_products(
            service_id: Annotated[str, Field(description="ID del servicio")],
            product_type: Optional[Annotated[str, Field(description="Tipo de producto ('product' o 'attribute')")]] = None
        ) -> Dict[str, Any]:
            """
            Obtener productos asociados a un servicio
            
            Args:
                service_id: ID del servicio
                product_type: Tipo de producto ('product' o 'attribute')
            
            Returns:
                Dict con la lista de productos y sus cantidades por defecto
            """
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_service_products(
                    service_id=service_id,
                    product_type=product_type
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo productos del servicio: {str(e)}"}