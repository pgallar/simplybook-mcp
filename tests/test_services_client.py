import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from src.simplybook.services.client import ServicesClient


class TestServicesClient:
    @pytest.fixture
    def auth_headers(self):
        return {
            "X-Company-Login": "test_company",
            "X-Token": "test_token_12345"
        }

    @pytest.fixture
    def services_client(self, auth_headers):
        return ServicesClient(auth_headers)

    @pytest.fixture
    def mock_services_response(self):
        return [
            {
                "id": "1",
                "name": "Servicio 1",
                "duration": 60,
                "price": 50.0
            },
            {
                "id": "2", 
                "name": "Servicio 2",
                "duration": 30,
                "price": 25.0
            }
        ]

    @pytest.fixture
    def mock_performers_response(self):
        return [
            {
                "id": "1",
                "name": "Performer 1",
                "email": "performer1@test.com"
            },
            {
                "id": "2",
                "name": "Performer 2", 
                "email": "performer2@test.com"
            }
        ]

    def test_init(self, services_client, auth_headers):
        """Test de inicialización del cliente"""
        assert services_client.base_url == "https://user-api-v2.simplybook.me"
        assert services_client.headers["X-Company-Login"] == auth_headers["X-Company-Login"]
        assert services_client.headers["X-Token"] == auth_headers["X-Token"]
        assert services_client.headers["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_get_services_list_success(self, services_client, mock_services_response):
        """Test de obtención de lista de servicios exitosa"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_services_response
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_services_list()

            assert len(result) == 2
            assert result[0]["id"] == "1"
            assert result[0]["name"] == "Servicio 1"
            assert result[1]["id"] == "2"
            assert result[1]["name"] == "Servicio 2"

    @pytest.mark.asyncio
    async def test_get_services_list_error(self, services_client):
        """Test de error al obtener lista de servicios"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.side_effect = httpx.HTTPStatusError(
                "404 Not Found",
                request=MagicMock(),
                response=MagicMock(status_code=404)
            )
            mock_client.return_value = mock_client_instance

            with pytest.raises(httpx.HTTPStatusError):
                await services_client.get_services_list()

    @pytest.mark.asyncio
    async def test_get_service_success(self, services_client, mock_services_response):
        """Test de obtención de servicio específico exitosa"""
        with patch.object(services_client, 'get_services_list', return_value=mock_services_response):
            result = await services_client.get_service("1")

            assert result["id"] == "1"
            assert result["name"] == "Servicio 1"
            assert result["duration"] == 60

    @pytest.mark.asyncio
    async def test_get_service_not_found(self, services_client, mock_services_response):
        """Test de servicio no encontrado"""
        with patch.object(services_client, 'get_services_list', return_value=mock_services_response):
            with pytest.raises(ValueError, match="Servicio con ID 999 no encontrado"):
                await services_client.get_service("999")

    @pytest.mark.asyncio
    async def test_get_performers_list_success(self, services_client, mock_performers_response):
        """Test de obtención de lista de performers exitosa"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_performers_response
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_performers_list()

            assert len(result) == 2
            assert result[0]["id"] == "1"
            assert result[0]["name"] == "Performer 1"
            assert result[1]["id"] == "2"
            assert result[1]["name"] == "Performer 2"

    @pytest.mark.asyncio
    async def test_get_first_working_day_success(self, services_client):
        """Test de obtención del primer día laboral exitosa"""
        mock_response_data = {"date": "2025-07-30"}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_first_working_day("1")

            assert result["date"] == "2025-07-30"

    @pytest.mark.asyncio
    async def test_get_work_calendar_success(self, services_client):
        """Test de obtención de calendario de trabajo exitosa"""
        mock_response_data = {
            "2025-07-29": {"is_day_off": 0},
            "2025-07-30": {"is_day_off": 1}
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_work_calendar(2025, 7, "1")

            assert "2025-07-29" in result
            assert "2025-07-30" in result
            assert result["2025-07-29"]["is_day_off"] == 0
            assert result["2025-07-30"]["is_day_off"] == 1

    @pytest.mark.asyncio
    async def test_get_time_slots_success(self, services_client):
        """Test de obtención de slots de tiempo exitosa"""
        mock_response_data = [
            {"time": "09:00", "available": True},
            {"time": "10:00", "available": True},
            {"time": "11:00", "available": False}
        ]
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_time_slots("2025-07-29", "1", "1")

            assert len(result) == 3
            assert result[0]["time"] == "09:00"
            assert result[0]["available"] is True
            assert result[2]["available"] is False

    @pytest.mark.asyncio
    async def test_create_booking_success(self, services_client):
        """Test de creación de reserva exitosa"""
        booking_data = {
            "event_id": "1",
            "unit_id": "1",
            "date": "2025-07-29",
            "time": "09:00",
            "client_name": "Test Client",
            "client_email": "test@example.com"
        }
        
        mock_response_data = {
            "booking_id": "12345",
            "status": "confirmed"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.create_booking(booking_data)

            assert result["booking_id"] == "12345"
            assert result["status"] == "confirmed"

    @pytest.mark.asyncio
    async def test_get_bookings_success(self, services_client):
        """Test de obtención de reservas exitosa"""
        mock_response_data = [
            {
                "id": "1",
                "event_name": "Servicio 1",
                "unit_name": "Performer 1",
                "date": "2025-07-29",
                "time": "09:00",
                "client_name": "Test Client"
            }
        ]
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.get_bookings("2025-07-29", "2025-07-29")

            assert len(result) == 1
            assert result[0]["id"] == "1"
            assert result[0]["event_name"] == "Servicio 1"

    @pytest.mark.asyncio
    async def test_cancel_booking_success(self, services_client):
        """Test de cancelación de reserva exitosa"""
        mock_response_data = {
            "success": True,
            "message": "Booking cancelled"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await services_client.cancel_booking("12345")

            assert result["success"] is True
            assert result["message"] == "Booking cancelled" 