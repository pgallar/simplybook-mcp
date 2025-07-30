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

        @mcp.tool(
            description="Crear un nuevo servicio",
            tags={"services", "create"}
        )
        async def create_service(
            name: Annotated[str, Field(description="Nombre del servicio")],
            description: Annotated[str, Field(description="Descripción del servicio")],
            price: Annotated[float, Field(description="Precio del servicio", ge=0)],
            deposit_price: Annotated[float, Field(description="Precio del depósito", ge=0)],
            duration: Annotated[int, Field(description="Duración en minutos", gt=0)],
            tax_id: Optional[Annotated[int, Field(description="ID del impuesto")]] = None,
            is_visible: Annotated[bool, Field(description="Si el servicio es visible")] = True
        ) -> Dict[str, Any]:
            """Crear un nuevo servicio"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                service_data = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "deposit_price": deposit_price,
                    "duration": duration,
                    "tax_id": tax_id,
                    "is_visible": is_visible
                }
                result = await self.client.create_service(service_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando servicio: {str(e)}"}

        @mcp.tool(
            description="Actualizar un servicio existente",
            tags={"services", "update"}
        )
        async def update_service(
            service_id: Annotated[str, Field(description="ID del servicio a actualizar")],
            name: Optional[Annotated[str, Field(description="Nombre del servicio")]] = None,
            description: Optional[Annotated[str, Field(description="Descripción del servicio")]] = None,
            price: Optional[Annotated[float, Field(description="Precio del servicio", ge=0)]] = None,
            deposit_price: Optional[Annotated[float, Field(description="Precio del depósito", ge=0)]] = None,
            tax_id: Optional[Annotated[int, Field(description="ID del impuesto")]] = None,
            duration: Optional[Annotated[int, Field(description="Duración en minutos", gt=0)]] = None,
            is_visible: Optional[Annotated[bool, Field(description="Si el servicio es visible")]] = None
        ) -> Dict[str, Any]:
            """Actualizar un servicio existente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                service_data = {}
                
                if name is not None:
                    service_data["name"] = name
                if description is not None:
                    service_data["description"] = description
                if price is not None:
                    service_data["price"] = price
                if deposit_price is not None:
                    service_data["deposit_price"] = deposit_price
                if tax_id is not None:
                    service_data["tax_id"] = tax_id
                if duration is not None:
                    service_data["duration"] = duration
                if is_visible is not None:
                    service_data["is_visible"] = is_visible
                    
                result = await self.client.update_service(service_id, service_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error actualizando servicio: {str(e)}"}

        @mcp.tool(
            description="Eliminar un servicio",
            tags={"services", "delete"}
        )
        async def delete_service(
            service_id: Annotated[str, Field(description="ID del servicio a eliminar")]
        ) -> Dict[str, Any]:
            """Eliminar un servicio"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                await self.client.delete_service(service_id)
                return {
                    "success": True,
                    "message": "Servicio eliminado correctamente"
                }
            except Exception as e:
                return {"error": f"Error eliminando servicio: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de categorías",
            tags={"services", "categories"}
        )
        async def get_categories() -> Dict[str, Any]:
            """Obtener lista de categorías"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ServicesClient(self.get_auth_headers())
                result = await self.client.get_categories()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo categorías: {str(e)}"}