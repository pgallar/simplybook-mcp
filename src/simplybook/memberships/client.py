from typing import Dict, Any, List, Optional
from ..http_client import LoggingHTTPClient

class MembershipsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def make_membership_instance(self,
                                     membership_id: str,
                                     period_start: str,
                                     is_invoice_needed: bool = True,
                                     payment_processor: str = "cash",
                                     auto_confirm_prolonging: bool = True,
                                     repeat_count: Optional[int] = None,
                                     clients: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Crear una instancia de membresía
        
        Args:
            membership_id: ID de la membresía
            period_start: Fecha de inicio
            is_invoice_needed: Si se necesita factura
            payment_processor: Procesador de pago
            auto_confirm_prolonging: Confirmar automáticamente la prolongación
            repeat_count: Cantidad de repeticiones
            clients: Lista de IDs de clientes
            
        Returns:
            Dict con los detalles de la instancia creada
        """
        data = {
            "membership_id": membership_id,
            "period_start": period_start,
            "is_invoice_needed": 1 if is_invoice_needed else 0,
            "payment_processor": payment_processor,
            "auto_confirm_prolonging": 1 if auto_confirm_prolonging else 0
        }
        
        if repeat_count is not None:
            data["repeat_count"] = repeat_count
            
        if clients:
            data["clients"] = clients
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/memberships/make-membership-instance", json=data)
            response.raise_for_status()
            return response.json()

    async def cancel_membership(self, membership_id: str) -> None:
        """
        Cancelar una membresía
        
        Args:
            membership_id: ID de la membresía del cliente
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/memberships/cancel-client-membership/{membership_id}")
            response.raise_for_status()