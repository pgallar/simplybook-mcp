from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import ProvidersClient
from ..schemas import (
    PROVIDERS_LIST_SCHEMA,
    PROVIDER_DETAILS_SCHEMA
)

class ProvidersRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(schema=PROVIDERS_LIST_SCHEMA)
        async def get_providers_list() -> Dict[str, Any]:
            """Obtener lista de proveedores"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                providers = await self.client.get_providers_list()
                return {
                    "success": True,
                    "providers": providers,
                    "count": len(providers)
                }
            except Exception as e:
                return {"error": f"Error obteniendo proveedores: {str(e)}"}

        @mcp.tool(schema=PROVIDER_DETAILS_SCHEMA)
        async def get_provider(provider_id: str) -> Dict[str, Any]:
            """Obtener información de un proveedor específico"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                provider = await self.client.get_provider(provider_id)
                return {
                    "success": True,
                    "provider": provider
                }
            except Exception as e:
                return {"error": f"Error obteniendo proveedor: {str(e)}"}

        @mcp.tool(schema={
            "type": "object",
            "required": ["provider_data"],
            "properties": {
                "provider_data": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nombre del proveedor"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email del proveedor",
                            "format": "email"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Teléfono del proveedor"
                        },
                        "services": {
                            "type": "array",
                            "description": "Lista de IDs de servicios que ofrece",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        })
        async def create_provider(provider_data: Dict[str, Any]) -> Dict[str, Any]:
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

        @mcp.tool(schema={
            "type": "object",
            "required": ["provider_id", "provider_data"],
            "properties": {
                "provider_id": {
                    "type": "string",
                    "description": "ID del proveedor a actualizar"
                },
                "provider_data": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nombre del proveedor"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email del proveedor",
                            "format": "email"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Teléfono del proveedor"
                        },
                        "services": {
                            "type": "array",
                            "description": "Lista de IDs de servicios que ofrece",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        })
        async def update_provider(provider_id: str, provider_data: Dict[str, Any]) -> Dict[str, Any]:
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

        @mcp.tool(schema={
            "type": "object",
            "required": ["provider_id"],
            "properties": {
                "provider_id": {
                    "type": "string",
                    "description": "ID del proveedor a eliminar"
                }
            }
        })
        async def delete_provider(provider_id: str) -> Dict[str, Any]:
            """Eliminar un proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                result = await self.client.delete_provider(provider_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error eliminando proveedor: {str(e)}"}

        @mcp.tool(schema={
            "type": "object",
            "required": ["provider_id"],
            "properties": {
                "provider_id": {
                    "type": "string",
                    "description": "ID del proveedor"
                }
            }
        })
        async def get_provider_locations(provider_id: str) -> Dict[str, Any]:
            """Obtener ubicaciones de un proveedor"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProvidersClient(self.get_auth_headers())
                locations = await self.client.get_provider_locations(provider_id)
                return {
                    "success": True,
                    "locations": locations,
                    "count": len(locations)
                }
            except Exception as e:
                return {"error": f"Error obteniendo ubicaciones: {str(e)}"}