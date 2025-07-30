from typing import Dict, Any, Optional, List
from ..http_client import LoggingHTTPClient

class PromotionsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_promotions(self,
                           service_id: Optional[str] = None,
                           visible_only: Optional[bool] = None,
                           promotion_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de promociones
        
        Args:
            service_id: ID del servicio para filtrar
            visible_only: Solo promociones visibles
            promotion_type: Tipo de promoción ('gift_card' o 'discount')
            
        Returns:
            Dict con la lista paginada de promociones
        """
        params = {}
        filters = {}
        
        if service_id:
            filters["service_id"] = service_id
            
        if visible_only is not None:
            filters["visible_only"] = 1 if visible_only else 0
            
        if promotion_type:
            filters["promotion_type"] = promotion_type
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/promotions", params=params)
            response.raise_for_status()
            return response.json()

    async def get_gift_cards(self,
                           purchased_by_client_id: Optional[str] = None,
                           used_by_client_id: Optional[str] = None,
                           service_id: Optional[str] = None,
                           user_id: Optional[str] = None,
                           duration: Optional[int] = None,
                           duration_type: Optional[str] = None,
                           price_from: Optional[float] = None,
                           price_to: Optional[float] = None,
                           status: Optional[str] = None,
                           expired_date_from: Optional[str] = None,
                           expired_date_to: Optional[str] = None,
                           start_date_from: Optional[str] = None,
                           start_date_to: Optional[str] = None,
                           discount_from: Optional[float] = None,
                           discount_to: Optional[float] = None,
                           used_amount_from: Optional[float] = None,
                           used_amount_to: Optional[float] = None,
                           code: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de tarjetas de regalo
        
        Args:
            purchased_by_client_id: ID del cliente que compró
            used_by_client_id: ID del cliente que usó
            service_id: ID del servicio
            user_id: ID del usuario que emitió
            duration: Duración
            duration_type: Tipo de duración
            price_from: Precio desde
            price_to: Precio hasta
            status: Estado (outdated, used, disabled, valid)
            expired_date_from: Fecha de expiración desde
            expired_date_to: Fecha de expiración hasta
            start_date_from: Fecha de inicio desde
            start_date_to: Fecha de inicio hasta
            discount_from: Descuento desde
            discount_to: Descuento hasta
            used_amount_from: Monto usado desde
            used_amount_to: Monto usado hasta
            code: Código
            
        Returns:
            Dict con la lista paginada de tarjetas de regalo
        """
        params = {}
        filters = {}
        
        if purchased_by_client_id:
            filters["purchased_by_client_id"] = purchased_by_client_id
            
        if used_by_client_id:
            filters["used_by_client_id"] = used_by_client_id
            
        if service_id:
            filters["service_id"] = service_id
            
        if user_id:
            filters["user_id"] = user_id
            
        if duration:
            filters["duration"] = duration
            
        if duration_type:
            filters["duration_type"] = duration_type
            
        if price_from:
            filters["price_from"] = price_from
            
        if price_to:
            filters["price_to"] = price_to
            
        if status:
            filters["status"] = status
            
        if expired_date_from:
            filters["expired_date_from"] = expired_date_from
            
        if expired_date_to:
            filters["expired_date_to"] = expired_date_to
            
        if start_date_from:
            filters["start_date_from"] = start_date_from
            
        if start_date_to:
            filters["start_date_to"] = start_date_to
            
        if discount_from:
            filters["discount_from"] = discount_from
            
        if discount_to:
            filters["discount_to"] = discount_to
            
        if used_amount_from:
            filters["used_amount_from"] = used_amount_from
            
        if used_amount_to:
            filters["used_amount_to"] = used_amount_to
            
        if code:
            filters["code"] = code
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/promotions/gift-cards", params=params)
            response.raise_for_status()
            return response.json()

    async def get_coupons(self,
                        used_by_client_id: Optional[str] = None,
                        service_id: Optional[str] = None,
                        user_id: Optional[str] = None,
                        duration: Optional[int] = None,
                        duration_type: Optional[str] = None,
                        status: Optional[str] = None,
                        expired_date_from: Optional[str] = None,
                        expired_date_to: Optional[str] = None,
                        start_date_from: Optional[str] = None,
                        start_date_to: Optional[str] = None,
                        discount_from: Optional[float] = None,
                        discount_to: Optional[float] = None,
                        code: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener lista de cupones
        
        Args:
            used_by_client_id: ID del cliente que usó
            service_id: ID del servicio
            user_id: ID del usuario que emitió
            duration: Duración
            duration_type: Tipo de duración
            status: Estado (outdated, used, disabled, valid)
            expired_date_from: Fecha de expiración desde
            expired_date_to: Fecha de expiración hasta
            start_date_from: Fecha de inicio desde
            start_date_to: Fecha de inicio hasta
            discount_from: Descuento desde
            discount_to: Descuento hasta
            code: Código
            
        Returns:
            Dict con la lista paginada de cupones
        """
        params = {}
        filters = {}
        
        if used_by_client_id:
            filters["used_by_client_id"] = used_by_client_id
            
        if service_id:
            filters["service_id"] = service_id
            
        if user_id:
            filters["user_id"] = user_id
            
        if duration:
            filters["duration"] = duration
            
        if duration_type:
            filters["duration_type"] = duration_type
            
        if status:
            filters["status"] = status
            
        if expired_date_from:
            filters["expired_date_from"] = expired_date_from
            
        if expired_date_to:
            filters["expired_date_to"] = expired_date_to
            
        if start_date_from:
            filters["start_date_from"] = start_date_from
            
        if start_date_to:
            filters["start_date_to"] = start_date_to
            
        if discount_from:
            filters["discount_from"] = discount_from
            
        if discount_to:
            filters["discount_to"] = discount_to
            
        if code:
            filters["code"] = code
            
        if filters:
            params["filter"] = filters
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/promotions/coupons", params=params)
            response.raise_for_status()
            return response.json()

    async def issue_gift_card(self,
                            promotion_id: int,
                            start_date: str,
                            personalized: bool,
                            send_email: Optional[bool] = None,
                            send_sms: Optional[bool] = None,
                            email_subject: Optional[str] = None,
                            email_body: Optional[str] = None,
                            sms_body: Optional[str] = None,
                            clients: Optional[List[int]] = None,
                            count: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Emitir tarjetas de regalo
        
        Args:
            promotion_id: ID de la promoción
            start_date: Fecha de inicio
            personalized: Si es personalizada
            send_email: Enviar por email
            send_sms: Enviar por SMS
            email_subject: Asunto del email
            email_body: Cuerpo del email
            sms_body: Cuerpo del SMS
            clients: Lista de IDs de clientes
            count: Cantidad de tarjetas no personalizadas
            
        Returns:
            Lista de instancias de tarjetas de regalo creadas
        """
        data = {
            "promotion_id": promotion_id,
            "start_date": start_date,
            "personalized": personalized
        }
        
        if personalized:
            if send_email is not None:
                data["send_email"] = send_email
            if send_sms is not None:
                data["send_sms"] = send_sms
            if email_subject:
                data["email_subject"] = email_subject
            if email_body:
                data["email_body"] = email_body
            if sms_body:
                data["sms_body"] = sms_body
            if clients:
                data["clients"] = clients
        else:
            if count:
                data["count"] = count
                
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/promotions/issue-gift-card", json=data)
            response.raise_for_status()
            return response.json() 