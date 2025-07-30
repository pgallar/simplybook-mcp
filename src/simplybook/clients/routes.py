from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import ClientsClient
from pydantic import Field
from typing import Annotated

class ClientsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de clientes",
            tags={"clients", "list"}
        )
        async def get_clients_list(
            page: Optional[Annotated[int, Field(description="Número de página", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None,
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de clientes"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.get_clients_list(
                    page=page,
                    on_page=on_page,
                    search=search
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo clientes: {str(e)}"}

        @mcp.tool(
            description="Obtener detalles de un cliente",
            tags={"clients", "details"}
        )
        async def get_client(
            client_id: Annotated[str, Field(description="ID del cliente")]
        ) -> Dict[str, Any]:
            """Obtener detalles de un cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.get_client(client_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo cliente: {str(e)}"}

        @mcp.tool(
            description="Crear un nuevo cliente",
            tags={"clients", "create"}
        )
        async def create_client(
            name: Annotated[str, Field(description="Nombre del cliente")],
            email: Optional[Annotated[str, Field(description="Email del cliente")]] = None,
            phone: Optional[Annotated[str, Field(description="Teléfono del cliente")]] = None
        ) -> Dict[str, Any]:
            """Crear un nuevo cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                client_data = {
                    "name": name
                }
                if email:
                    client_data["email"] = email
                if phone:
                    client_data["phone"] = phone
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.create_client(client_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando cliente: {str(e)}"}

        @mcp.tool(
            description="Editar un cliente existente",
            tags={"clients", "edit"}
        )
        async def edit_client(
            client_id: Annotated[str, Field(description="ID del cliente")],
            name: Optional[Annotated[str, Field(description="Nombre del cliente")]] = None,
            email: Optional[Annotated[str, Field(description="Email del cliente")]] = None,
            phone: Optional[Annotated[str, Field(description="Teléfono del cliente")]] = None
        ) -> Dict[str, Any]:
            """Editar un cliente existente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                client_data = {}
                if name:
                    client_data["name"] = name
                if email:
                    client_data["email"] = email
                if phone:
                    client_data["phone"] = phone
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.edit_client(client_id, client_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error editando cliente: {str(e)}"}

        @mcp.tool(
            description="Eliminar un cliente",
            tags={"clients", "delete"}
        )
        async def delete_client(
            client_id: Annotated[str, Field(description="ID del cliente a eliminar")]
        ) -> Dict[str, Any]:
            """Eliminar un cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                await self.client.delete_client(client_id)
                return {
                    "success": True,
                    "message": "Cliente eliminado correctamente"
                }
            except Exception as e:
                return {"error": f"Error eliminando cliente: {str(e)}"}

        @mcp.tool(
            description="Obtener membresías de un cliente",
            tags={"clients", "memberships"}
        )
        async def get_client_memberships(
            client_id: Optional[Annotated[str, Field(description="ID del cliente")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None,
            service_start_date: Optional[Annotated[str, Field(description="Fecha de inicio del servicio (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            count: Optional[Annotated[int, Field(description="Cantidad de reservas grupales")]] = None,
            active_only: Optional[Annotated[bool, Field(description="Solo membresías activas")]] = None,
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None,
            page: Optional[Annotated[int, Field(description="Número de página", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de membresías de clientes"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.get_client_memberships(
                    page=page,
                    on_page=on_page,
                    client_id=client_id,
                    service_id=service_id,
                    service_start_date=service_start_date,
                    count=count,
                    active_only=active_only,
                    search=search
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo membresías: {str(e)}"}

        @mcp.tool(
            description="Obtener campos de cliente",
            tags={"clients", "fields"}
        )
        async def get_client_fields() -> Dict[str, Any]:
            """Obtener lista de campos de cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.get_client_fields()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo campos de cliente: {str(e)}"}

        @mcp.tool(
            description="Obtener valores de campos de un cliente",
            tags={"clients", "fields", "values"}
        )
        async def get_client_field_values(
            client_id: Annotated[str, Field(description="ID del cliente")]
        ) -> Dict[str, Any]:
            """Obtener valores de campos de un cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.get_client_field_values(client_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo valores de campos: {str(e)}"}

        @mcp.tool(
            description="Editar campos de un cliente",
            tags={"clients", "fields", "edit"}
        )
        async def edit_client_fields(
            client_id: Annotated[str, Field(description="ID del cliente")],
            field_values: Annotated[List[Dict[str, Any]], Field(description="Lista de valores de campos")]
        ) -> Dict[str, Any]:
            """Editar valores de campos de un cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.edit_client_fields(client_id, field_values)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error editando campos: {str(e)}"}

        @mcp.tool(
            description="Crear cliente con campos personalizados",
            tags={"clients", "fields", "create"}
        )
        async def create_client_with_fields(
            field_values: Annotated[List[Dict[str, Any]], Field(description="Lista de valores de campos")]
        ) -> Dict[str, Any]:
            """Crear un cliente con valores de campos personalizados"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ClientsClient(self.get_auth_headers())
                result = await self.client.create_client_with_fields(field_values)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando cliente: {str(e)}"}