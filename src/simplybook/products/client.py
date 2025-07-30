from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class ProductsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_products(self,
                          service_id: Optional[str] = None,
                          search: Optional[str] = None,
                          product_type: Optional[str] = None,
                          visible_only: Optional[bool] = None) -> Dict[str, Any]:
        """
        Obtener lista de productos/atributos
        
        Args:
            service_id: ID del servicio para filtrar
            search: Texto de búsqueda
            product_type: Tipo de producto ('product' o 'attribute')
            visible_only: Solo productos visibles
            
        Returns:
            Dict con la lista paginada de productos
        """
        params = {}
        filters = {}
        
        if service_id:
            filters["service_id"] = service_id
            
        if search:
            filters["search"] = search
            
        if product_type:
            filters["type"] = product_type
            
        if visible_only is not None:
            filters["visible_only"] = 1 if visible_only else 0
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/products", params=params)
            response.raise_for_status()
            return response.json()

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de un producto/atributo
        
        Args:
            product_id: ID del producto
            
        Returns:
            Dict con los detalles del producto
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/products/{product_id}")
            response.raise_for_status()
            return response.json()