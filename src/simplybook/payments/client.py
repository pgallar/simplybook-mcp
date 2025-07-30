from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class PaymentsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_invoices(self,
                          page: Optional[int] = None,
                          on_page: Optional[int] = None,
                          client_id: Optional[str] = None,
                          datetime_from: Optional[str] = None,
                          datetime_to: Optional[str] = None,
                          status: Optional[str] = None,
                          booking_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de órdenes/facturas
        
        Args:
            page: Número de página
            on_page: Elementos por página
            client_id: Filtrar por ID de cliente
            datetime_from: Fecha y hora desde
            datetime_to: Fecha y hora hasta
            status: Estado de la orden/factura
            booking_code: Código de reserva
            
        Returns:
            Dict con la lista paginada de órdenes/facturas
        """
        params = {}
        filters = {}
        
        if page is not None:
            params["page"] = page
            
        if on_page is not None:
            params["on_page"] = on_page
            
        if client_id:
            filters["client_id"] = client_id
            
        if datetime_from:
            filters["datetime_from"] = datetime_from
            
        if datetime_to:
            filters["datetime_to"] = datetime_to
            
        if status:
            filters["status"] = status
            
        if booking_code:
            filters["booking_code"] = booking_code
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/invoices", params=params)
            response.raise_for_status()
            return response.json()

    async def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de una orden/factura
        
        Args:
            invoice_id: ID de la orden/factura
            
        Returns:
            Dict con los detalles de la orden/factura
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/invoices/{invoice_id}")
            response.raise_for_status()
            return response.json()

    async def get_invoice_link(self, invoice_id: str) -> str:
        """
        Obtener URL de la página de la orden/factura
        
        Args:
            invoice_id: ID de la orden/factura
            
        Returns:
            URL de la página de la orden/factura
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/invoices/{invoice_id}/link")
            response.raise_for_status()
            return response.json()

    async def accept_payment(self, invoice_id: str, payment_processor: str) -> Dict[str, Any]:
        """
        Aceptar pago manualmente
        
        Args:
            invoice_id: ID de la orden/factura
            payment_processor: Procesador de pago
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/invoices/{invoice_id}/accept-payment",
                json={"payment_processor": payment_processor}
            )
            response.raise_for_status()
            return response.json()

    async def accept_saved_payment(self, invoice_id: str, payment_method_id: int) -> Dict[str, Any]:
        """
        Aceptar pago con método guardado
        
        Args:
            invoice_id: ID de la orden/factura
            payment_method_id: ID del método de pago guardado
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/invoices/{invoice_id}/rebill",
                json={"payment_method_id": payment_method_id}
            )
            response.raise_for_status()
            return response.json()

    async def get_payment_link(self, invoice_id: str) -> str:
        """
        Generar enlace de pago
        
        Args:
            invoice_id: ID de la orden/factura
            
        Returns:
            URL del enlace de pago
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/invoices/{invoice_id}/payment-link")
            response.raise_for_status()
            return response.json()

    async def send_payment_link(self, invoice_id: str, message_type: str) -> None:
        """
        Enviar enlace de pago al cliente
        
        Args:
            invoice_id: ID de la orden/factura
            message_type: Tipo de mensaje ('email' o 'sms')
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/invoices/{invoice_id}/send-payment-link",
                json={"type": message_type}
            )
            response.raise_for_status()

    async def apply_promo_code(self, invoice_id: str, code: str) -> Dict[str, Any]:
        """
        Aplicar código promocional
        
        Args:
            invoice_id: ID de la orden/factura
            code: Código promocional
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/invoices/{invoice_id}/apply-promo-code",
                json={"code": code}
            )
            response.raise_for_status()
            return response.json()

    async def remove_promo_code(self, invoice_id: str, instance_id: int) -> Dict[str, Any]:
        """
        Eliminar código promocional aplicado
        
        Args:
            invoice_id: ID de la orden/factura
            instance_id: ID de la instancia del código promocional
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/invoices/{invoice_id}/promo-code/{instance_id}")
            response.raise_for_status()
            return response.json()

    async def apply_tip(self, invoice_id: str, percent: Optional[int] = None, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Aplicar propina
        
        Args:
            invoice_id: ID de la orden/factura
            percent: Porcentaje de propina
            amount: Monto fijo de propina
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        data = {}
        if percent is not None:
            data["percent"] = percent
        if amount is not None:
            data["amount"] = amount
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(f"/invoices/{invoice_id}/tip", json=data)
            response.raise_for_status()
            return response.json()

    async def remove_tip(self, invoice_id: str) -> Dict[str, Any]:
        """
        Eliminar propina aplicada
        
        Args:
            invoice_id: ID de la orden/factura
            
        Returns:
            Dict con los detalles de la orden/factura actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(f"/invoices/{invoice_id}/tip")
            response.raise_for_status()
            return response.json()

    async def make_terminal_payment(self, invoice_id: str, payment_system: str, reader_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Realizar pago con terminal
        
        Args:
            invoice_id: ID de la orden/factura
            payment_system: Sistema de pago
            reader_id: ID del lector de terminal
            
        Returns:
            Dict con el resultado del pago
        """
        data = {
            "paymentSystem": payment_system
        }
        if reader_id:
            data["readerId"] = reader_id
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post(f"/invoices/{invoice_id}/make-terminal-payment", json=data)
            response.raise_for_status()
            return response.json()

    async def get_terminal_readers(self) -> List[Dict[str, Any]]:
        """
        Obtener lista de lectores de terminal
        
        Returns:
            Lista de lectores de terminal disponibles
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/invoices/terminal/reader/list")
            response.raise_for_status()
            return response.json()

    async def get_stripe_connection_token(self) -> Dict[str, Any]:
        """
        Obtener token de conexión de Stripe
        
        Returns:
            Dict con el token de conexión
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/invoices/terminal/stripe-connection-token")
            response.raise_for_status()
            return response.json()

    async def get_stripe_config_location(self) -> Dict[str, Any]:
        """
        Obtener ubicación de configuración de Stripe
        
        Returns:
            Dict con la configuración de ubicación
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/invoices/terminal/stripe-config-location")
            response.raise_for_status()
            return response.json()

    async def get_client_payment_methods(self, client_id: str) -> List[Dict[str, Any]]:
        """
        Obtener métodos de pago guardados de un cliente
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Lista de métodos de pago guardados
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/payment-methods/{client_id}")
            response.raise_for_status()
            return response.json()