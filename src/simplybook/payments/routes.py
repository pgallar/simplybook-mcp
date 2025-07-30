from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import PaymentsClient
from pydantic import Field
from typing import Annotated

class PaymentsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de órdenes/facturas",
            tags={"payments", "invoices", "list"}
        )
        async def get_invoices(
            page: Optional[Annotated[int, Field(description="Número de página", ge=1)]] = None,
            on_page: Optional[Annotated[int, Field(description="Elementos por página", ge=1)]] = None,
            client_id: Optional[Annotated[str, Field(description="ID del cliente")]] = None,
            datetime_from: Optional[Annotated[str, Field(description="Fecha y hora desde (YYYY-MM-DD HH:mm:ss)")]] = None,
            datetime_to: Optional[Annotated[str, Field(description="Fecha y hora hasta (YYYY-MM-DD HH:mm:ss)")]] = None,
            status: Optional[Annotated[str, Field(description="Estado de la orden/factura")]] = None,
            booking_code: Optional[Annotated[str, Field(description="Código de reserva")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de órdenes/facturas"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_invoices(
                    page=page,
                    on_page=on_page,
                    client_id=client_id,
                    datetime_from=datetime_from,
                    datetime_to=datetime_to,
                    status=status,
                    booking_code=booking_code
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo órdenes/facturas: {str(e)}"}

        @mcp.tool(
            description="Obtener detalles de una orden/factura",
            tags={"payments", "invoices", "details"}
        )
        async def get_invoice(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")]
        ) -> Dict[str, Any]:
            """Obtener detalles de una orden/factura"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_invoice(invoice_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo orden/factura: {str(e)}"}

        @mcp.tool(
            description="Obtener URL de la página de una orden/factura",
            tags={"payments", "invoices", "link"}
        )
        async def get_invoice_link(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")]
        ) -> Dict[str, Any]:
            """Obtener URL de la página de una orden/factura"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_invoice_link(invoice_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo enlace: {str(e)}"}

        @mcp.tool(
            description="Aceptar pago manualmente",
            tags={"payments", "invoices", "accept"}
        )
        async def accept_payment(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            payment_processor: Annotated[str, Field(description="Procesador de pago")]
        ) -> Dict[str, Any]:
            """Aceptar pago manualmente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.accept_payment(invoice_id, payment_processor)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error aceptando pago: {str(e)}"}

        @mcp.tool(
            description="Aceptar pago con método guardado",
            tags={"payments", "invoices", "rebill"}
        )
        async def accept_saved_payment(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            payment_method_id: Annotated[int, Field(description="ID del método de pago guardado")]
        ) -> Dict[str, Any]:
            """Aceptar pago con método guardado"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.accept_saved_payment(invoice_id, payment_method_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error aceptando pago: {str(e)}"}

        @mcp.tool(
            description="Generar enlace de pago",
            tags={"payments", "invoices", "payment-link"}
        )
        async def get_payment_link(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")]
        ) -> Dict[str, Any]:
            """Generar enlace de pago"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_payment_link(invoice_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error generando enlace de pago: {str(e)}"}

        @mcp.tool(
            description="Enviar enlace de pago al cliente",
            tags={"payments", "invoices", "send-link"}
        )
        async def send_payment_link(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            message_type: Annotated[str, Field(description="Tipo de mensaje ('email' o 'sms')")]
        ) -> Dict[str, Any]:
            """Enviar enlace de pago al cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                await self.client.send_payment_link(invoice_id, message_type)
                return {
                    "success": True,
                    "message": "Enlace de pago enviado correctamente"
                }
            except Exception as e:
                return {"error": f"Error enviando enlace de pago: {str(e)}"}

        @mcp.tool(
            description="Aplicar código promocional",
            tags={"payments", "invoices", "promo-code"}
        )
        async def apply_promo_code(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            code: Annotated[str, Field(description="Código promocional")]
        ) -> Dict[str, Any]:
            """Aplicar código promocional"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.apply_promo_code(invoice_id, code)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error aplicando código promocional: {str(e)}"}

        @mcp.tool(
            description="Eliminar código promocional aplicado",
            tags={"payments", "invoices", "promo-code", "remove"}
        )
        async def remove_promo_code(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            instance_id: Annotated[int, Field(description="ID de la instancia del código promocional")]
        ) -> Dict[str, Any]:
            """Eliminar código promocional aplicado"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.remove_promo_code(invoice_id, instance_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error eliminando código promocional: {str(e)}"}

        @mcp.tool(
            description="Aplicar propina",
            tags={"payments", "invoices", "tip"}
        )
        async def apply_tip(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            percent: Optional[Annotated[int, Field(description="Porcentaje de propina")]] = None,
            amount: Optional[Annotated[float, Field(description="Monto fijo de propina")]] = None
        ) -> Dict[str, Any]:
            """Aplicar propina"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.apply_tip(invoice_id, percent=percent, amount=amount)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error aplicando propina: {str(e)}"}

        @mcp.tool(
            description="Eliminar propina aplicada",
            tags={"payments", "invoices", "tip", "remove"}
        )
        async def remove_tip(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")]
        ) -> Dict[str, Any]:
            """Eliminar propina aplicada"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.remove_tip(invoice_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error eliminando propina: {str(e)}"}

        @mcp.tool(
            description="Realizar pago con terminal",
            tags={"payments", "invoices", "terminal"}
        )
        async def make_terminal_payment(
            invoice_id: Annotated[str, Field(description="ID de la orden/factura")],
            payment_system: Annotated[str, Field(description="Sistema de pago")],
            reader_id: Optional[Annotated[str, Field(description="ID del lector de terminal")]] = None
        ) -> Dict[str, Any]:
            """Realizar pago con terminal"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.make_terminal_payment(
                    invoice_id,
                    payment_system=payment_system,
                    reader_id=reader_id
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error realizando pago con terminal: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de lectores de terminal",
            tags={"payments", "terminal", "readers"}
        )
        async def get_terminal_readers() -> Dict[str, Any]:
            """Obtener lista de lectores de terminal"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_terminal_readers()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo lectores de terminal: {str(e)}"}

        @mcp.tool(
            description="Obtener token de conexión de Stripe",
            tags={"payments", "terminal", "stripe"}
        )
        async def get_stripe_connection_token() -> Dict[str, Any]:
            """Obtener token de conexión de Stripe"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_stripe_connection_token()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo token de conexión: {str(e)}"}

        @mcp.tool(
            description="Obtener ubicación de configuración de Stripe",
            tags={"payments", "terminal", "stripe"}
        )
        async def get_stripe_config_location() -> Dict[str, Any]:
            """Obtener ubicación de configuración de Stripe"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_stripe_config_location()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo configuración: {str(e)}"}

        @mcp.tool(
            description="Obtener métodos de pago guardados de un cliente",
            tags={"payments", "methods"}
        )
        async def get_client_payment_methods(
            client_id: Annotated[str, Field(description="ID del cliente")]
        ) -> Dict[str, Any]:
            """Obtener métodos de pago guardados de un cliente"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = PaymentsClient(self.get_auth_headers())
                result = await self.client.get_client_payment_methods(client_id)
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo métodos de pago: {str(e)}"}