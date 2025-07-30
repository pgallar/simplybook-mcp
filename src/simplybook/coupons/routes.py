from typing import Dict, Any, Optional, List
from ..base_routes import BaseRoutes
from .client import CouponsClient
from pydantic import Field
from typing import Annotated

class CouponsRoutes(BaseRoutes):
    def register_tools(self, mcp):
        @mcp.tool(
            description="Obtener lista de promociones",
            tags={"promotions", "list"}
        )
        async def get_promotions(
            service_id: Optional[Annotated[str, Field(description="ID del servicio para filtrar")]] = None,
            visible_only: Optional[Annotated[bool, Field(description="Solo promociones visibles")]] = None,
            promotion_type: Optional[Annotated[str, Field(description="Tipo de promoción ('gift_card' o 'discount')")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de promociones"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = CouponsClient(self.get_auth_headers())
                result = await self.client.get_promotions(
                    service_id=service_id,
                    visible_only=visible_only,
                    promotion_type=promotion_type
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo promociones: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de tarjetas de regalo",
            tags={"promotions", "gift-cards"}
        )
        async def get_gift_cards(
            purchased_by_client_id: Optional[Annotated[str, Field(description="ID del cliente que compró")]] = None,
            used_by_client_id: Optional[Annotated[str, Field(description="ID del cliente que usó")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None,
            user_id: Optional[Annotated[str, Field(description="ID del usuario que emitió")]] = None,
            duration: Optional[Annotated[int, Field(description="Duración")]] = None,
            duration_type: Optional[Annotated[str, Field(description="Tipo de duración")]] = None,
            price_from: Optional[Annotated[float, Field(description="Precio desde")]] = None,
            price_to: Optional[Annotated[float, Field(description="Precio hasta")]] = None,
            status: Optional[Annotated[str, Field(description="Estado (outdated, used, disabled, valid)")]] = None,
            expired_date_from: Optional[Annotated[str, Field(description="Fecha de expiración desde (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            expired_date_to: Optional[Annotated[str, Field(description="Fecha de expiración hasta (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            start_date_from: Optional[Annotated[str, Field(description="Fecha de inicio desde (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            start_date_to: Optional[Annotated[str, Field(description="Fecha de inicio hasta (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            discount_from: Optional[Annotated[float, Field(description="Descuento desde")]] = None,
            discount_to: Optional[Annotated[float, Field(description="Descuento hasta")]] = None,
            used_amount_from: Optional[Annotated[float, Field(description="Monto usado desde")]] = None,
            used_amount_to: Optional[Annotated[float, Field(description="Monto usado hasta")]] = None,
            code: Optional[Annotated[str, Field(description="Código")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de tarjetas de regalo"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = CouponsClient(self.get_auth_headers())
                result = await self.client.get_gift_cards(
                    purchased_by_client_id=purchased_by_client_id,
                    used_by_client_id=used_by_client_id,
                    service_id=service_id,
                    user_id=user_id,
                    duration=duration,
                    duration_type=duration_type,
                    price_from=price_from,
                    price_to=price_to,
                    status=status,
                    expired_date_from=expired_date_from,
                    expired_date_to=expired_date_to,
                    start_date_from=start_date_from,
                    start_date_to=start_date_to,
                    discount_from=discount_from,
                    discount_to=discount_to,
                    used_amount_from=used_amount_from,
                    used_amount_to=used_amount_to,
                    code=code
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo tarjetas de regalo: {str(e)}"}

        @mcp.tool(
            description="Obtener lista de cupones",
            tags={"promotions", "coupons"}
        )
        async def get_coupons(
            used_by_client_id: Optional[Annotated[str, Field(description="ID del cliente que usó")]] = None,
            service_id: Optional[Annotated[str, Field(description="ID del servicio")]] = None,
            user_id: Optional[Annotated[str, Field(description="ID del usuario que emitió")]] = None,
            duration: Optional[Annotated[int, Field(description="Duración")]] = None,
            duration_type: Optional[Annotated[str, Field(description="Tipo de duración")]] = None,
            status: Optional[Annotated[str, Field(description="Estado (outdated, used, disabled, valid)")]] = None,
            expired_date_from: Optional[Annotated[str, Field(description="Fecha de expiración desde (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            expired_date_to: Optional[Annotated[str, Field(description="Fecha de expiración hasta (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            start_date_from: Optional[Annotated[str, Field(description="Fecha de inicio desde (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            start_date_to: Optional[Annotated[str, Field(description="Fecha de inicio hasta (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")]] = None,
            discount_from: Optional[Annotated[float, Field(description="Descuento desde")]] = None,
            discount_to: Optional[Annotated[float, Field(description="Descuento hasta")]] = None,
            code: Optional[Annotated[str, Field(description="Código")]] = None
        ) -> Dict[str, Any]:
            """Obtener lista de cupones"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = CouponsClient(self.get_auth_headers())
                result = await self.client.get_coupons(
                    used_by_client_id=used_by_client_id,
                    service_id=service_id,
                    user_id=user_id,
                    duration=duration,
                    duration_type=duration_type,
                    status=status,
                    expired_date_from=expired_date_from,
                    expired_date_to=expired_date_to,
                    start_date_from=start_date_from,
                    start_date_to=start_date_to,
                    discount_from=discount_from,
                    discount_to=discount_to,
                    code=code
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo cupones: {str(e)}"}

        @mcp.tool(
            description="Emitir tarjetas de regalo",
            tags={"promotions", "gift-cards", "issue"}
        )
        async def issue_gift_card(
            promotion_id: Annotated[int, Field(description="ID de la promoción")],
            start_date: Annotated[str, Field(description="Fecha de inicio (YYYY-MM-DD)", pattern="^\\d{4}-\\d{2}-\\d{2}$")],
            personalized: Annotated[bool, Field(description="Si es personalizada")],
            send_email: Optional[Annotated[bool, Field(description="Enviar por email")]] = None,
            send_sms: Optional[Annotated[bool, Field(description="Enviar por SMS")]] = None,
            email_subject: Optional[Annotated[str, Field(description="Asunto del email")]] = None,
            email_body: Optional[Annotated[str, Field(description="Cuerpo del email")]] = None,
            sms_body: Optional[Annotated[str, Field(description="Cuerpo del SMS")]] = None,
            clients: Optional[Annotated[List[int], Field(description="Lista de IDs de clientes")]] = None,
            count: Optional[Annotated[int, Field(description="Cantidad de tarjetas no personalizadas")]] = None
        ) -> Dict[str, Any]:
            """Emitir tarjetas de regalo"""
            try:
                if not await self.ensure_authenticated():
                    return {"error": "No se pudo autenticar"}
                    
                self.client = CouponsClient(self.get_auth_headers())
                result = await self.client.issue_gift_card(
                    promotion_id=promotion_id,
                    start_date=start_date,
                    personalized=personalized,
                    send_email=send_email,
                    send_sms=send_sms,
                    email_subject=email_subject,
                    email_body=email_body,
                    sms_body=sms_body,
                    clients=clients,
                    count=count
                )
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error emitiendo tarjetas de regalo: {str(e)}"}