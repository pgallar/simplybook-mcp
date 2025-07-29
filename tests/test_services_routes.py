import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.simplybook.services.routes import ServicesRoutes


class TestServicesRoutes:
    @pytest.fixture
    def services_routes(self):
        return ServicesRoutes("test_company", "test_login", "test_password")

    @pytest.fixture
    def mock_mcp(self):
        mcp = MagicMock()
        mcp.tool = MagicMock(return_value=MagicMock())
        return mcp

    def test_init(self, services_routes):
        """Test de inicialización de las rutas"""
        assert services_routes.company == "test_company"
        assert services_routes.login == "test_login"
        assert services_routes.password == "test_password"
        assert services_routes.auth_client is not None

    def test_register_tools(self, services_routes, mock_mcp):
        """Test de registro de herramientas"""
        services_routes.register_tools(mock_mcp)
        
        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.asyncio
    async def test_get_services_list_success(self, services_routes, mock_mcp):
        """Test de obtención de lista de servicios exitosa"""
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_services_list = AsyncMock(return_value=[
                        {"id": "1", "name": "Servicio 1"},
                        {"id": "2", "name": "Servicio 2"}
                    ])
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    services = await services_routes.client.get_services_list()
                    
                    assert len(services) == 2
                    assert services[0]["id"] == "1"
                    assert services[1]["id"] == "2"

    @pytest.mark.asyncio
    async def test_get_services_list_auth_failure(self, services_routes, mock_mcp):
        """Test de fallo de autenticación al obtener servicios"""
        # Mock de autenticación fallida
        with patch.object(services_routes, 'ensure_authenticated', return_value=False):
            result = services_routes.ensure_authenticated()
            assert result is False

    @pytest.mark.asyncio
    async def test_get_services_list_exception(self, services_routes, mock_mcp):
        """Test de excepción al obtener servicios"""
        # Mock de autenticación exitosa pero excepción en cliente
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_services_list = AsyncMock(side_effect=Exception("API Error"))
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    try:
                        await services_routes.client.get_services_list()
                        assert False, "Debería haber lanzado una excepción"
                    except Exception as e:
                        assert "API Error" in str(e)

    @pytest.mark.asyncio
    async def test_get_service_success(self, services_routes, mock_mcp):
        """Test de obtención de servicio específico exitosa"""
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_service = AsyncMock(return_value={"id": "1", "name": "Servicio 1"})
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    service = await services_routes.client.get_service("1")
                    
                    assert service["id"] == "1"
                    assert service["name"] == "Servicio 1"

    @pytest.mark.asyncio
    async def test_get_performers_list_success(self, services_routes, mock_mcp):
        """Test de obtención de lista de performers exitosa"""
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_performers_list = AsyncMock(return_value=[
                        {"id": "1", "name": "Performer 1"},
                        {"id": "2", "name": "Performer 2"}
                    ])
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    performers = await services_routes.client.get_performers_list()
                    
                    assert len(performers) == 2
                    assert performers[0]["id"] == "1"
                    assert performers[1]["id"] == "2"

    @pytest.mark.asyncio
    async def test_get_first_working_day_success(self, services_routes, mock_mcp):
        """Test de obtención del primer día laboral exitosa"""
        # Registrar las herramientas
        services_routes.register_tools(mock_mcp)
        
        # Obtener la función de primer día laboral
        working_day_tool = mock_mcp.tool.call_args_list[3][0][0]
        
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_first_working_day.return_value = {"date": "2025-07-30"}
                    mock_client_class.return_value = mock_client
                    
                    result = await working_day_tool("1")
                    
                    assert result["success"] is True
                    assert result["date"] == "2025-07-30"

    @pytest.mark.asyncio
    async def test_get_work_calendar_success(self, services_routes, mock_mcp):
        """Test de obtención de calendario de trabajo exitosa"""
        # Registrar las herramientas
        services_routes.register_tools(mock_mcp)
        
        # Obtener la función de calendario
        calendar_tool = mock_mcp.tool.call_args_list[4][0][0]
        
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_work_calendar.return_value = {
                        "2025-07-29": {"is_day_off": 0},
                        "2025-07-30": {"is_day_off": 1}
                    }
                    mock_client_class.return_value = mock_client
                    
                    result = await calendar_tool(2025, 7, "1")
                    
                    assert result["success"] is True
                    assert "2025-07-29" in result["calendar"]
                    assert "2025-07-30" in result["calendar"]

    @pytest.mark.asyncio
    async def test_get_time_slots_success(self, services_routes, mock_mcp):
        """Test de obtención de slots de tiempo exitosa"""
        # Registrar las herramientas
        services_routes.register_tools(mock_mcp)
        
        # Obtener la función de slots de tiempo
        slots_tool = mock_mcp.tool.call_args_list[5][0][0]
        
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_time_slots.return_value = [
                        {"time": "09:00", "available": True},
                        {"time": "10:00", "available": True}
                    ]
                    mock_client_class.return_value = mock_client
                    
                    result = await slots_tool("2025-07-29", "1", "1")
                    
                    assert result["success"] is True
                    assert len(result["time_slots"]) == 2
                    assert result["count"] == 2

    @pytest.mark.asyncio
    async def test_create_booking_success(self, services_routes, mock_mcp):
        """Test de creación de reserva exitosa"""
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.create_booking = AsyncMock(return_value={
                        "booking_id": "12345",
                        "status": "confirmed"
                    })
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    booking_data = {
                        "event_id": "1",
                        "unit_id": "1",
                        "date": "2025-07-29",
                        "time": "09:00",
                        "client_name": "Test Client",
                        "client_email": "test@example.com"
                    }
                    result = await services_routes.client.create_booking(booking_data)
                    
                    assert result["booking_id"] == "12345"
                    assert result["status"] == "confirmed"

    @pytest.mark.asyncio
    async def test_get_bookings_success(self, services_routes, mock_mcp):
        """Test de obtención de reservas exitosa"""
        # Registrar las herramientas
        services_routes.register_tools(mock_mcp)
        
        # Obtener la función de reservas
        bookings_tool = mock_mcp.tool.call_args_list[7][0][0]
        
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.get_bookings.return_value = [
                        {
                            "id": "1",
                            "event_name": "Servicio 1",
                            "unit_name": "Performer 1",
                            "date": "2025-07-29",
                            "time": "09:00"
                        }
                    ]
                    mock_client_class.return_value = mock_client
                    
                    result = await bookings_tool("2025-07-29", "2025-07-29")
                    
                    assert result["success"] is True
                    assert len(result["bookings"]) == 1
                    assert result["count"] == 1

    @pytest.mark.asyncio
    async def test_cancel_booking_success(self, services_routes, mock_mcp):
        """Test de cancelación de reserva exitosa"""
        # Mock de autenticación exitosa
        with patch.object(services_routes, 'ensure_authenticated', return_value=True):
            with patch.object(services_routes, 'get_auth_headers', return_value={"X-Token": "test"}):
                with patch('src.simplybook.services.routes.ServicesClient') as mock_client_class:
                    mock_client = MagicMock()
                    mock_client.cancel_booking = AsyncMock(return_value={
                        "success": True,
                        "message": "Booking cancelled"
                    })
                    mock_client_class.return_value = mock_client
                    
                    services_routes.client = mock_client
                    result = await services_routes.client.cancel_booking("12345")
                    
                    assert result["success"] is True
                    assert result["message"] == "Booking cancelled" 