from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import TicketsClient
from pydantic import Field
from typing import Annotated

class TicketsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener información de un ticket por código",
            tags={"tickets", "info"}
        )
        async def get_ticket(
            code: Annotated[str, Field(description="Código del ticket")]
        ) -> Dict[str, Any]:
            """Obtener información de un ticket por código"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = TicketsClient(self.get_auth_headers())
                result = await self.client.get_ticket(code)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo ticket: {str(e)}"}

        @mcp.tool(
            description="Validar un ticket",
            tags={"tickets", "check-in"}
        )
        async def check_in_ticket(
            code: Annotated[str, Field(description="Código del ticket")]
        ) -> Dict[str, Any]:
            """Validar un ticket"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = TicketsClient(self.get_auth_headers())
                result = await self.client.check_in_ticket(code)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error validando ticket: {str(e)}"}