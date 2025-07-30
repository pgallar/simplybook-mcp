import httpx
from typing import Optional, Dict, Any, List
from ..http_client import LoggingHTTPClient

class BookingsClient:
    def __init__(self, auth_headers: Dict[str, str]):
        self.base_url = "https://user-api-v2.simplybook.me/admin"
        self.headers = {
            **auth_headers,
            "Content-Type": "application/json"
        }

    async def get_all_bookings_simple(self) -> List[Dict[str, Any]]:
        """Obtener lista básica de reservas sin filtros"""
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/bookings")
            response.raise_for_status()
            return response.json()

    async def get_booking_list(self, 
                              page: Optional[int] = None,
                              on_page: Optional[int] = None,
                              upcoming_only: Optional[bool] = None,
                              status: Optional[str] = None,
                              services: Optional[List[str]] = None,
                              providers: Optional[List[str]] = None,
                              client_id: Optional[str] = None,
                              date_from: Optional[str] = None,
                              date_to: Optional[str] = None,
                              search: Optional[str] = None,
                              additional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Obtener lista de reservas con filtros avanzados
        
        Args:
            page: Número de página
            on_page: Elementos por página
            upcoming_only: Solo reservas futuras
            status: Estado de la reserva (confirmed/confirmed_pending/pending/canceled)
            services: Lista de IDs de servicios para filtrar
            providers: Lista de IDs de proveedores para filtrar
            client_id: ID del cliente para filtrar
            date_from: Fecha desde (YYYY-MM-DD)
            date_to: Fecha hasta (YYYY-MM-DD)
            search: String de búsqueda (por código, datos del cliente)
            additional_fields: Campos adicionales para filtrar (&filter[additional_fields][field] = value)
            
        Returns:
            Dict con la respuesta paginada de reservas (AdminReportBookingEntity[])
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso al reporte de reservas
        """
        # Construir parámetros de query
        params = {}
        
        # Parámetros de paginación
        if page is not None:
            params["page"] = page
        if on_page is not None:
            params["on_page"] = on_page
            
        # Aplicar filtros en el formato correcto filter[key]=value
        if upcoming_only is not None:
            params["filter[upcoming_only]"] = 1 if upcoming_only else 0
            
        if status:
            params["filter[status]"] = status
            
        if services:
            # Si services es una lista, convertir a formato filter[services][]=value
            for i, service_id in enumerate(services):
                params[f"filter[services][{i}]"] = service_id
            
        if providers:
            # Si providers es una lista, convertir a formato filter[providers][]=value
            for i, provider_id in enumerate(providers):
                params[f"filter[providers][{i}]"] = provider_id
            
        if client_id:
            params["filter[client_id]"] = client_id
            
        if date_from:
            params["filter[date_from]"] = date_from
            
        if date_to:
            params["filter[date_to]"] = date_to
            
        if search:
            params["filter[search]"] = search
            
        if additional_fields:
            for field, value in additional_fields.items():
                params[f"filter[additional_fields][{field}]"] = value
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/bookings", params=params)
            response.raise_for_status()
            return response.json()

    async def create_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear una nueva reserva y retornar el resultado (BookingResultEntity)
        
        Args:
            booking_data: AdminBookingBuildEntity con los datos de la reserva:
                - start_datetime: Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)
                - end_datetime: Fecha y hora de fin (YYYY-MM-DD HH:mm:ss)
                - location_id: ID de la ubicación
                - category_id: ID de la categoría
                - service_id: ID del servicio
                - provider_id: ID del proveedor
                - client_id: ID del cliente
                - count: Cantidad para reserva grupal (opcional)
                - recurring_settings: Configuración de recurrencia (opcional)
                - additional_fields: Lista de valores de campos adicionales (opcional)
                - products: Lista de productos/addons (opcional)
                - client_membership_id: ID de membresía del cliente (opcional)
                - batch_id: ID de lote para reservas múltiples/grupales (opcional)
                - skip_membership: No usar membresía para esta reserva (opcional)
                - user_status_id: ID del estado del usuario (opcional)
                - accept_payment: Generar orden de pago para la reserva (opcional)
                - payment_processor: Procesador de pago aceptado (opcional)
            
        Returns:
            BookingResultEntity con el resultado de la reserva
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso a la reserva
            BadRequest: Si los datos proporcionados son inválidos
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post(
                "/bookings", 
                json=booking_data
            )
            response.raise_for_status()
            return response.json()

    async def edit_booking(self, booking_id: str, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modificar una reserva existente y retornar el resultado (BookingResultEntity)
        
        Args:
            booking_id: ID de la reserva a modificar
            booking_data: AdminBookingBuildEntity con los datos de la reserva:
                - start_datetime: Fecha y hora de inicio (YYYY-MM-DD HH:mm:ss)
                - end_datetime: Fecha y hora de fin (YYYY-MM-DD HH:mm:ss)
                - location_id: ID de la ubicación
                - category_id: ID de la categoría
                - service_id: ID del servicio
                - provider_id: ID del proveedor
                - client_id: ID del cliente
                - count: Cantidad para reserva grupal (opcional)
                - recurring_settings: Configuración de recurrencia (opcional)
                - additional_fields: Lista de valores de campos adicionales (opcional)
                - products: Lista de productos/addons (opcional)
                - client_membership_id: ID de membresía del cliente (opcional)
                - batch_id: ID de lote para reservas múltiples/grupales (opcional)
                - skip_membership: No usar membresía para esta reserva (opcional)
                - user_status_id: ID del estado del usuario (opcional)
                - accept_payment: Generar orden de pago para la reserva (opcional)
                - payment_processor: Procesador de pago aceptado (opcional)
            
        Returns:
            BookingResultEntity con el resultado de la reserva
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso a la reserva
            BadRequest: Si los datos proporcionados son inválidos
            NotFound: Si la reserva no existe
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/bookings/{booking_id}",
                json=booking_data
            )
            response.raise_for_status()
            return response.json()

    async def get_booking_details(self, booking_id: str) -> Dict[str, Any]:
        """
        Obtener detalles de una reserva específica
        
        Args:
            booking_id: ID de la reserva
            
        Returns:
            Dict con los detalles de la reserva
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/bookings/{booking_id}")
            response.raise_for_status()
            return response.json()

    async def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """Cancelar una reserva"""
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.delete(
                f"/bookings/{booking_id}"
            )
            response.raise_for_status()
            return response.json()

    async def approve_booking(self, booking_id: str) -> Dict[str, Any]:
        """
        Aprobar una reserva
        
        Args:
            booking_id: ID de la reserva
            
        Returns:
            Dict con los detalles de la reserva actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/bookings/{booking_id}/approve"
            )
            response.raise_for_status()
            return response.json()

    async def set_booking_status(self, booking_id: str, status_id: int) -> Dict[str, Any]:
        """
        Aplicar un estado a una reserva
        
        Args:
            booking_id: ID de la reserva
            status_id: ID del estado a aplicar
            
        Returns:
            Dict con los detalles de la reserva actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/bookings/{booking_id}/status",
                json={"status_id": status_id}
            )
            response.raise_for_status()
            return response.json()

    async def get_booking_links(self, booking_id: str) -> Dict[str, Any]:
        """
        Obtener enlaces relacionados con una reserva
        
        Args:
            booking_id: ID de la reserva
            
        Returns:
            Dict con los enlaces de la reserva
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/bookings/{booking_id}/links")
            response.raise_for_status()
            return response.json()

    async def set_booking_comment(self, booking_id: str, comment: str) -> Dict[str, Any]:
        """
        Establecer un comentario para una reserva
        
        Args:
            booking_id: ID de la reserva
            comment: Texto del comentario
            
        Returns:
            Dict con los detalles de la reserva actualizada
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/bookings/{booking_id}/comment",
                json={"comment": comment}
            )
            response.raise_for_status()
            return response.json()

    async def get_schedule(self, 
                         service_id: int,
                         provider_id: int,
                         date_from: str,
                         date_to: str) -> List[Dict[str, Any]]:
        """
        Obtener horario para un servicio y proveedor
        
        Args:
            service_id: ID del servicio
            provider_id: ID del proveedor
            date_from: Fecha inicial (YYYY-MM-DD)
            date_to: Fecha final (YYYY-MM-DD)
            
        Returns:
            Lista de objetos WorkDayEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(
                "/schedule",
                params={
                    "service_id": service_id,
                    "provider_id": provider_id,
                    "date_from": date_from,
                    "date_to": date_to
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_slots(self,
                       service_id: int,
                       provider_id: int,
                       date: str) -> List[Dict[str, Any]]:
        """
        Obtener slots disponibles para un día específico
        
        Args:
            service_id: ID del servicio
            provider_id: ID del proveedor
            date: Fecha (YYYY-MM-DD)
            
        Returns:
            Lista de objetos TimeSlotEntity
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(
                "/schedule/slots",
                params={
                    "service_id": service_id,
                    "provider_id": provider_id,
                    "date": date
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_available_slots(self,
                                service_id: int,
                                provider_id: int,
                                date: str,
                                count: Optional[int] = None,
                                products: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """
        Obtener slots disponibles para reservar
        
        Args:
            service_id: ID del servicio
            provider_id: ID del proveedor
            date: Fecha (YYYY-MM-DD)
            count: Cantidad para reserva grupal
            products: Lista de IDs de productos adicionales
            
        Returns:
            Lista de objetos TimeSlotEntity
        """
        params = {
            "service_id": service_id,
            "provider_id": provider_id,
            "date": date
        }
        
        if count is not None:
            params["count"] = count
            
        if products:
            params["products"] = products
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/schedule/available-slots", params=params)
            response.raise_for_status()
            return response.json()

    async def get_first_available_slot(self,
                                     service_id: int,
                                     provider_id: int,
                                     date: str,
                                     count: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtener el primer slot disponible
        
        Args:
            service_id: ID del servicio
            provider_id: ID del proveedor
            date: Fecha (YYYY-MM-DD)
            count: Cantidad para reserva grupal
            
        Returns:
            Objeto TimeSlotEntity
        """
        params = {
            "service_id": service_id,
            "provider_id": provider_id,
            "date": date
        }
        
        if count is not None:
            params["count"] = count
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/schedule/first-available-slot", params=params)
            response.raise_for_status()
            return response.json()

    async def get_slots_timeline(self,
                               service_id: int,
                               provider_id: int,
                               date_from: str,
                               date_to: str,
                               count: Optional[int] = None,
                               with_available_slots: bool = False,
                               booking_id: Optional[int] = None,
                               product_ids: Optional[List[int]] = None,
                               skip_min_max_restriction: bool = False) -> List[Dict[str, Any]]:
        """
        Obtener timeline de slots por fecha
        
        Args:
            service_id: ID del servicio
            provider_id: ID del proveedor
            date_from: Fecha inicial (YYYY-MM-DD)
            date_to: Fecha final (YYYY-MM-DD)
            count: Cantidad de reservas
            with_available_slots: Calcular slots disponibles
            booking_id: ID de reserva para edición
            product_ids: Lista de IDs de productos adicionales
            skip_min_max_restriction: Omitir restricciones min/max
            
        Returns:
            Lista de objetos Timeline_SlotsDateEntity
        """
        params = {
            "service_id": service_id,
            "provider_id": provider_id,
            "date_from": date_from,
            "date_to": date_to,
            "with_available_slots": 1 if with_available_slots else 0,
            "skip_min_max_restriction": 1 if skip_min_max_restriction else 0
        }
        
        if count is not None:
            params["count"] = count
            
        if booking_id is not None:
            params["booking_id"] = booking_id
            
        if product_ids:
            params["product_ids"] = product_ids
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/timeline/slots", params=params)
            response.raise_for_status()
            return response.json()

    async def get_calendar_data(self,
                              mode: str,
                              upcoming_only: Optional[bool] = None,
                              status: Optional[str] = None,
                              services: Optional[List[str]] = None,
                              providers: Optional[List[str]] = None,
                              client_id: Optional[str] = None,
                              date_from: Optional[str] = None,
                              date_to: Optional[str] = None,
                              search: Optional[str] = None,
                              additional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Obtener datos del calendario con reservas, notas y tiempos de descanso
        
        Args:
            mode: Modo de visualización ('day', 'week', 'provider' o 'service')
            upcoming_only: Solo reservas futuras
            status: Estado de las reservas (confirmed/confirmed_pending/pending/canceled)
            services: Lista de IDs de servicios para filtrar
            providers: Lista de IDs de proveedores para filtrar
            client_id: ID del cliente para filtrar
            date_from: Fecha desde (YYYY-MM-DD)
            date_to: Fecha hasta (YYYY-MM-DD)
            search: Texto de búsqueda (por código, datos del cliente)
            additional_fields: Campos adicionales para filtrar (&filter[additional_fields][field] = value)
            
        Returns:
            Calendar_DataEntity con los datos del calendario
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso al reporte de reservas
        """
        params = {
            "mode": mode
        }
        
        # Aplicar filtros en el formato correcto filter[key]=value
        if upcoming_only is not None:
            params["filter[upcoming_only]"] = 1 if upcoming_only else 0
            
        if status:
            params["filter[status]"] = status
            
        if services:
            # Si services es una lista, convertir a formato filter[services][]=value
            for i, service_id in enumerate(services):
                params[f"filter[services][{i}]"] = service_id
            
        if providers:
            # Si providers es una lista, convertir a formato filter[providers][]=value
            for i, provider_id in enumerate(providers):
                params[f"filter[providers][{i}]"] = provider_id
            
        if client_id:
            params["filter[client_id]"] = client_id
            
        if date_from:
            params["filter[date_from]"] = date_from
            
        if date_to:
            params["filter[date_to]"] = date_to
            
        if search:
            params["filter[search]"] = search
            
        if additional_fields:
            for field, value in additional_fields.items():
                params[f"filter[additional_fields][{field}]"] = value
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get("/calendar", params=params)
            response.raise_for_status()
            return response.json()

    async def generate_detailed_report(self,
                                    created_date_from: Optional[str] = None,
                                    created_date_to: Optional[str] = None,
                                    date_from: Optional[str] = None,
                                    date_to: Optional[str] = None,
                                    event_id: Optional[str] = None,
                                    unit_group_id: Optional[str] = None,
                                    client_id: Optional[str] = None,
                                    booking_type: Optional[str] = None,
                                    export_columns: Optional[List[str]] = None,
                                    order_direction: str = "asc",
                                    order_field: str = "record_date") -> Dict[str, Any]:
        """
        Generar reporte detallado
        
        Args:
            created_date_from: Fecha de creación desde (YYYY-MM-DD)
            created_date_to: Fecha de creación hasta (YYYY-MM-DD)
            date_from: Fecha desde (YYYY-MM-DD)
            date_to: Fecha hasta (YYYY-MM-DD)
            event_id: ID del servicio
            unit_group_id: ID del proveedor
            client_id: ID del cliente
            booking_type: Tipo de reserva ('cancelled' o 'non_cancelled')
            export_columns: Lista de columnas a exportar
            order_direction: Dirección de ordenamiento ('asc' o 'desc')
            order_field: Campo de ordenamiento
            
        Returns:
            Dict con el resultado de la generación del reporte
            
        Throws:
            AccessDenied: Si el usuario no tiene acceso
            BadRequest: Si los datos proporcionados son inválidos
        """
        data = {
            "filter": {},
            "export_columns": export_columns or [],
            "order_direction": order_direction,
            "order_field": order_field
        }
        
        if created_date_from:
            data["filter"]["created_date_from"] = created_date_from
            
        if created_date_to:
            data["filter"]["created_date_to"] = created_date_to
            
        if date_from:
            data["filter"]["date_from"] = date_from
            
        if date_to:
            data["filter"]["date_to"] = date_to
            
        if event_id:
            data["filter"]["event_id"] = event_id
            
        if unit_group_id:
            data["filter"]["unit_group_id"] = unit_group_id
            
        if client_id:
            data["filter"]["client_id"] = client_id
            
        if booking_type:
            data["filter"]["booking_type"] = booking_type
            
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.post("/detailed-report", json=data)
            response.raise_for_status()
            return response.json()

    async def get_detailed_report(self, report_id: str) -> Dict[str, Any]:
        """
        Obtener reporte detallado por ID
        
        Args:
            report_id: ID del reporte
            
        Returns:
            Dict con los datos del reporte
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.get(f"/detailed-report/{report_id}")
            response.raise_for_status()
            return response.json()

    async def set_medical_test_status(self, booking_id: str, status: str) -> None:
        """
        Establecer estado de prueba médica para una reserva
        
        Args:
            booking_id: ID de la reserva
            status: Estado ('negative', 'positive', etc.)
        """
        async with LoggingHTTPClient(self.base_url, self.headers) as client:
            response = await client.put(
                f"/medical-test/status/{booking_id}",
                json={"status": status}
            )
            response.raise_for_status()