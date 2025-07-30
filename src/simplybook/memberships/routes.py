from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import MembershipsClient
from pydantic import Field
from typing import Annotated

class MembershipsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Crear una instancia de membresía",
            tags={"memberships", "create"}
        )
        async def make_membership_instance(
            membership_id: Annotated[str, Field(description="ID de la membresía")],
            period_start: Annotated[str, Field(description="Fecha de inicio (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")],
            is_invoice_needed: Optional[Annotated[bool, Field(description="Si se necesita factura")]] = True,
            payment_processor: Optional[Annotated[str, Field(description="Procesador de pago")]] = "cash",
            auto_confirm_prolonging: Optional[Annotated[bool, Field(description="Confirmar automáticamente la prolongación")]] = True,
            repeat_count: Optional[Annotated[int, Field(description="Cantidad de repeticiones")]] = None,
            clients: Optional[Annotated[List[str], Field(description="Lista de IDs de clientes")]] = None
        ) -> Dict[str, Any]:
            """Crear una instancia de membresía"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = MembershipsClient(self.get_auth_headers())
                result = await self.client.make_membership_instance(
                    membership_id=membership_id,
                    period_start=period_start,
                    is_invoice_needed=is_invoice_needed,
                    payment_processor=payment_processor,
                    auto_confirm_prolonging=auto_confirm_prolonging,
                    repeat_count=repeat_count,
                    clients=clients
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error creando instancia de membresía: {str(e)}"}

        @mcp.tool(
            description="Cancelar una membresía",
            tags={"memberships", "cancel"}
        )
        async def cancel_membership(
            membership_id: Annotated[str, Field(description="ID de la membresía del cliente")]
        ) -> Dict[str, Any]:
            """Cancelar una membresía"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = MembershipsClient(self.get_auth_headers())
                await self.client.cancel_membership(membership_id)
                return {
                    "success": True,
                    "message": "Membresía cancelada correctamente"
                }
            except Exception as e:
                return {"error": f"Error cancelando membresía: {str(e)}"}