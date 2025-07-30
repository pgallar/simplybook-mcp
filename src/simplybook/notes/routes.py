from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import NotesClient
from pydantic import Field
from typing import Annotated

class NotesRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de notas",
            tags={"notes", "list"}
        )
        async def get_notes(
            page: Optional[Annotated[int, Field(description="Número de página", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None,
            providers: Optional[Annotated[List[str], Field(description="Lista de IDs de proveedores")]] = None,
            services: Optional[Annotated[List[str], Field(description="Lista de IDs de servicios")]] = None,
            types: Optional[Annotated[List[str], Field(description="Lista de IDs de tipos de notas")]] = None,
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None,
            date_from: Optional[Annotated[str, Field(description="Fecha desde (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            date_to: Optional[Annotated[str, Field(description="Fecha hasta (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de notas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = NotesClient(self.get_auth_headers())
                result = await self.client.get_notes(
                    page=page,
                    on_page=on_page,
                    providers=providers,
                    services=services,
                    types=types,
                    search=search,
                    date_from=date_from,
                    date_to=date_to
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo notas: {str(e)}"}

        @mcp.tool(
            description="Crear una nueva nota",
            tags={"notes", "create"}
        )
        async def create_note(
            start_date_time: Annotated[str, Field(description="Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)")],
            end_date_time: Annotated[str, Field(description="Fecha y hora de fin (YYYY-MM-DD HH:mm:ss)")],
            note_type_id: Annotated[str, Field(description="ID del tipo de nota")],
            note: Annotated[str, Field(description="Texto de la nota")],
            mode: Annotated[str, Field(description="Modo de la nota ('service', 'provider' o 'all')")],
            time_blocked: Annotated[bool, Field(description="Si el tiempo está bloqueado")],
            provider_id: Optional[Annotated[str, Field(description="ID del proveedor")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None
        ) -> Dict[str, Any]:
            """Crear una nueva nota"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                note_data = {
                    "start_date_time": start_date_time,
                    "end_date_time": end_date_time,
                    "note_type_id": note_type_id,
                    "note": note,
                    "mode": mode,
                    "time_blocked": time_blocked
                }
                
                if provider_id is not None:
                    note_data["provider_id"] = provider_id
                if service_id is not None:
                    note_data["service_id"] = service_id
                
                self.client = NotesClient(self.get_auth_headers())
                result = await self.client.create_note(note_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando nota: {str(e)}"}

        @mcp.tool(
            description="Editar una nota existente",
            tags={"notes", "edit"}
        )
        async def edit_note(
            note_id: Annotated[str, Field(description="ID de la nota")],
            provider_id: Optional[Annotated[str, Field(description="ID del proveedor")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None,
            start_date_time: Optional[Annotated[str, Field(description="Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)")]] = None,
            end_date_time: Optional[Annotated[str, Field(description="Fecha y hora de fin (YYYY-MM-DD HH:mm:ss)")]] = None,
            note_type_id: Optional[Annotated[str, Field(description="ID del tipo de nota")]] = None,
            note: Optional[Annotated[str, Field(description="Texto de la nota")]] = None,
            mode: Optional[Annotated[str, Field(description="Modo de la nota ('service', 'provider' o 'all')")]] = None,
            time_blocked: Optional[Annotated[bool, Field(description="Si el tiempo está bloqueado")]] = None
        ) -> Dict[str, Any]:
            """Editar una nota existente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                note_data = {}
                if provider_id is not None:
                    note_data["provider_id"] = provider_id
                if service_id is not None:
                    note_data["service_id"] = service_id
                if start_date_time is not None:
                    note_data["start_date_time"] = start_date_time
                if end_date_time is not None:
                    note_data["end_date_time"] = end_date_time
                if note_type_id is not None:
                    note_data["note_type_id"] = note_type_id
                if note is not None:
                    note_data["note"] = note
                if mode is not None:
                    note_data["mode"] = mode
                if time_blocked is not None:
                    note_data["time_blocked"] = time_blocked
                
                self.client = NotesClient(self.get_auth_headers())
                result = await self.client.edit_note(note_id, note_data)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error editando nota: {str(e)}"}

        @mcp.tool(
            description="Eliminar una nota",
            tags={"notes", "delete"}
        )
        async def delete_note(
            note_id: Annotated[str, Field(description="ID de la nota a eliminar")]
        ) -> Dict[str, Any]:
            """Eliminar una nota"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = NotesClient(self.get_auth_headers())
                await self.client.delete_note(note_id)
                return {
                    "success": True,
                    "message": "Nota eliminada correctamente"
                }
            except Exception as e:
                return {"error": f"Error eliminando nota: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de tipos de notas",
            tags={"notes", "types"}
        )
        async def get_note_types() -> Dict[str, Any]:
            """Obtener lista de tipos de notas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = NotesClient(self.get_auth_headers())
                result = await self.client.get_note_types()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo tipos de notas: {str(e)}"}

        @mcp.tool(
            description="Obtener tipo de nota predeterminado",
            tags={"notes", "types", "default"}
        )
        async def get_default_note_type() -> Dict[str, Any]:
            """Obtener tipo de nota predeterminado"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = NotesClient(self.get_auth_headers())
                result = await self.client.get_default_note_type()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo tipo de nota predeterminado: {str(e)}"}