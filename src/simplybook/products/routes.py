from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import ProductsClient
from pydantic import Field
from typing import Annotated

class ProductsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de productos/atributos",
            tags={"products", "list"}
        )
        async def get_products(
            page: Optional[Annotated[int, Field(description="Número de página", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None,
            product_type: Optional[Annotated[str, Field(description="Tipo de producto ('product' o 'attribute')")]] = None,
            search: Optional[Annotated[str, Field(description="Texto de búsqueda")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de productos/atributos"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProductsClient(self.get_auth_headers())
                result = await self.client.get_products(
                    page=page,
                    on_page=on_page,
                    service_id=service_id,
                    product_type=product_type,
                    search=search
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo productos: {str(e)}"}

        @mcp.tool(
            description="Obtener detalles de un producto/atributo",
            tags={"products", "details"}
        )
        async def get_product(
            product_id: Annotated[str, Field(description="ID del producto/atributo")]
        ) -> Dict[str, Any]:
            """Obtener detalles de un producto/atributo"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = ProductsClient(self.get_auth_headers())
                result = await self.client.get_product(product_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo producto: {str(e)}"}