from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import SubscriptionClient
from pydantic import Field
from typing import Annotated

class SubscriptionRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener información de la suscripción actual",
            tags={"subscription", "current"}
        )
        async def get_current_subscription() -> Dict[str, Any]:
            """Obtener información de la suscripción actual"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = SubscriptionClient(self.get_auth_headers())
                result = await self.client.get_current_subscription()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo suscripción: {str(e)}"}