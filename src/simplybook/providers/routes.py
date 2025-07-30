from typing import Dict, Any, Optional
from ..base_routes import BaseRoutes
from .client import ProvidersClient
from pydantic import Field
from typing import Annotated

class ProvidersRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de proveedores",
            tags={"providers", "list"}
        )
        async def get_providers(
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio para filtrar")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de proveedores"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.get_providers(
                    search=search,
                    service_id=service_id
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo proveedores: {str(e)}"}

        @mcp.tool(
            description="Obtener información de un proveedor específico",
            tags={"providers", "details"}
        )
        async def get_provider(
            provider_id: Annotated[str, Field(description="ID del proveedor")]
        ) -> Dict[str, Any]:
            """Obtener información de un proveedor específico"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.get_provider(provider_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo proveedor: {str(e)}"}

        @mcp.tool(
            description="Crear un nuevo proveedor",
            tags={"providers", "create"}
        )
        async def create_provider(
            provider_data: Annotated[Dict[str, Any], Field(
                description="Datos del proveedor",
                example={
                    "name": "Nombre del Proveedor",
                    "email": "proveedor@email.com",
                    "phone": "+1234567890",
                    "services": ["123", "456"]
                }
            )]
        ) -> Dict[str, Any]:
            """Crear un nuevo proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.create_provider(provider_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando proveedor: {str(e)}"}

        @mcp.tool(
            description="Actualizar un proveedor existente",
            tags={"providers", "update"}
        )
        async def update_provider(
            provider_id: Annotated[str, Field(description="ID del proveedor a actualizar")],
            provider_data: Annotated[Dict[str, Any], Field(
                description="Datos actualizados del proveedor",
                example={
                    "name": "Nombre Actualizado",
                    "email": "nuevo@email.com",
                    "phone": "+0987654321",
                    "services": ["789", "012"]
                }
            )]
        ) -> Dict[str, Any]:
            """Actualizar un proveedor existente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.update_provider(provider_id, provider_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error actualizando proveedor: {str(e)}"}

        @mcp.tool(
            description="Eliminar un proveedor",
            tags={"providers", "delete"}
        )
        async def delete_provider(
            provider_id: Annotated[str, Field(description="ID del proveedor a eliminar")]
        ) -> Dict[str, Any]:
            """Eliminar un proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                await self.client.delete_provider(provider_id)
                return {
                    "success": True,
                    "message": "Proveedor eliminado correctamente"
                }
            except Exception as e:
                return {"error": f"Error eliminando proveedor: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de ubicaciones",
            tags={"providers", "locations"}
        )
        async def get_locations() -> Dict[str, Any]:
            """Obtener lista de ubicaciones"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.get_locations()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo ubicaciones: {str(e)}"}