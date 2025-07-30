from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import StatisticsClient
from pydantic import Field
from typing import Annotated

class StatisticsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener estadísticas generales",
            tags={"statistics", "general"}
        )
        async def get_statistics() -> Dict[str, Any]:
            """
            Obtener estadísticas generales:
            - Proveedor más popular y número de reservas (últimos 30 días)
            - Servicio más popular y número de reservas (últimos 30 días)
            - Número de reservas hoy
            - Número de reservas esta semana (Lunes-Domingo)
            """
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = StatisticsClient(self.get_auth_headers())
                result = await self.client.get_statistics()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo estadísticas: {str(e)}"}