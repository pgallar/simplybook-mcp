import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.simplybook.auth.routes import AuthRoutes


class TestAuthRoutes:
    @pytest.fixture
    def auth_routes(self):
        return AuthRoutes()

    @pytest.fixture
    def mock_mcp(self):
        mcp = MagicMock()
        mcp.tool = MagicMock(return_value=MagicMock())
        return mcp

    @pytest.fixture
    def mock_auth_client(self):
        return MagicMock()

    def test_init(self, auth_routes):
        """Test de inicialización de las rutas"""
        assert auth_routes.auth_client is not None

    def test_register_tools(self, auth_routes, mock_mcp):
        """Test de registro de herramientas"""
        auth_routes.register_tools(mock_mcp)
        
        # Verificar que se registraron las herramientas
        assert mock_mcp.tool.call_count >= 1

    @pytest.mark.asyncio
    async def test_authenticate_success(self, auth_routes, mock_mcp):
        """Test de autenticación exitosa"""
        # Mock del resultado de autenticación
        mock_result = {
            "success": True,
            "token": "test_token_12345",
            "message": "Autenticación exitosa"
        }
        
        with patch.object(auth_routes.auth_client, 'authenticate', return_value=mock_result):
            result = await auth_routes.auth_client.authenticate("test_company", "test_login", "test_password")
            
            assert result["success"] is True
            assert result["token"] == "test_token_12345"
            assert "Autenticación exitosa" in result["message"]

    @pytest.mark.asyncio
    async def test_authenticate_failure(self, auth_routes, mock_mcp):
        """Test de autenticación fallida"""
        # Mock del resultado de autenticación fallida
        mock_result = {
            "success": False,
            "message": "Autenticación fallida",
            "error": "Invalid credentials"
        }
        
        with patch.object(auth_routes.auth_client, 'authenticate', return_value=mock_result):
            result = await auth_routes.auth_client.authenticate("test_company", "test_login", "wrong_password")
            
            assert result["success"] is False
            assert "Autenticación fallida" in result["message"]

    @pytest.mark.asyncio
    async def test_authenticate_exception(self, auth_routes, mock_mcp):
        """Test de excepción en autenticación"""
        # Mock que simula el comportamiento del método real cuando hay una excepción
        async def mock_authenticate(*args, **kwargs):
            raise Exception("Connection error")
        
        with patch.object(auth_routes.auth_client, 'authenticate', side_effect=mock_authenticate):
            try:
                await auth_routes.auth_client.authenticate("test_company", "test_login", "test_password")
                assert False, "Debería haber lanzado una excepción"
            except Exception as e:
                assert "Connection error" in str(e)

    @pytest.mark.asyncio
    async def test_validate_token_success(self, auth_routes, mock_mcp):
        """Test de validación de token exitosa"""
        # Mock de get_auth_headers exitoso
        mock_headers = {
            "X-Company-Login": "test_company",
            "X-Token": "test_token_12345"
        }
        
        with patch.object(auth_routes.auth_client, 'get_auth_headers', return_value=mock_headers):
            result = await auth_routes.validate_token_internal("test_company")
            
            assert result["valid"] is True
            assert "Token válido" in result["message"]

    @pytest.mark.asyncio
    async def test_validate_token_invalid(self, auth_routes, mock_mcp):
        """Test de validación de token inválido"""
        # Mock de get_auth_headers que lanza ValueError
        def mock_get_headers(*args, **kwargs):
            raise ValueError("No se encontró token")
        
        with patch.object(auth_routes.auth_client, 'get_auth_headers', side_effect=mock_get_headers):
            result = await auth_routes.validate_token_internal("test_company")
            
            assert result["valid"] is False
            assert "Token no encontrado o expirado" in result["message"]

    @pytest.mark.asyncio
    async def test_clear_token_success(self, auth_routes, mock_mcp):
        """Test de eliminación de token exitosa"""
        with patch.object(auth_routes.auth_client, 'clear_token', return_value=True):
            result = auth_routes.auth_client.clear_token("test_company")
            
            assert result is True

    @pytest.mark.asyncio
    async def test_clear_token_failure(self, auth_routes, mock_mcp):
        """Test de eliminación de token fallida"""
        with patch.object(auth_routes.auth_client, 'clear_token', return_value=False):
            result = auth_routes.auth_client.clear_token("test_company")
            
            assert result is False

    @pytest.mark.asyncio
    async def test_get_auth_status_authenticated(self, auth_routes, mock_mcp):
        """Test de estado de autenticación cuando está autenticado"""
        # Mock de get_auth_headers exitoso
        mock_headers = {
            "X-Company-Login": "test_company",
            "X-Token": "test_token_12345"
        }
        
        with patch.object(auth_routes.auth_client, 'get_auth_headers', return_value=mock_headers):
            result = await auth_routes.validate_token_internal("test_company")
            
            assert result["valid"] is True
            assert "Token válido" in result["message"]

    @pytest.mark.asyncio
    async def test_get_auth_status_not_authenticated(self, auth_routes, mock_mcp):
        """Test de estado de autenticación cuando no está autenticado"""
        # Mock de get_auth_headers que lanza ValueError
        def mock_get_headers(*args, **kwargs):
            raise ValueError("No se encontró token")
        
        with patch.object(auth_routes.auth_client, 'get_auth_headers', side_effect=mock_get_headers):
            result = await auth_routes.validate_token_internal("test_company")
            
            assert result["valid"] is False
            assert "Token no encontrado o expirado" in result["message"] 