import pytest
import httpx
import json
import tempfile
import os
from unittest.mock import AsyncMock, patch, MagicMock
from src.simplybook.auth.client import AuthClient


class TestAuthClient:
    @pytest.fixture
    def auth_client(self):
        return AuthClient()

    @pytest.fixture
    def mock_token_response(self):
        return {
            "token": "test_token_12345",
            "expires_in": 3600
        }

    @pytest.fixture
    def mock_error_response(self):
        return {
            "error": "Invalid credentials",
            "code": 401
        }

    def test_init(self, auth_client):
        """Test de inicialización del cliente"""
        assert auth_client.base_url == "https://user-api-v2.simplybook.me"
        assert auth_client.auth_url == "https://user-api-v2.simplybook.me/admin/auth"
        assert auth_client.token_file is None

    def test_get_token_file_path(self, auth_client):
        """Test de generación de ruta de archivo de token"""
        company = "test_company"
        token_path = auth_client._get_token_file_path(company)
        
        assert "simplybook_token_test_company.json" in token_path
        assert tempfile.gettempdir() in token_path

    def test_save_and_load_token(self, auth_client):
        """Test de guardado y carga de token"""
        company = "test_company"
        token = "test_token_12345"
        
        # Guardar token
        auth_client._save_token(company, token)
        
        # Verificar que se guardó
        token_path = auth_client._get_token_file_path(company)
        assert os.path.exists(token_path)
        
        # Cargar token
        loaded_token = auth_client._load_token(company)
        assert loaded_token == token
        
        # Limpiar archivo de prueba
        os.remove(token_path)

    def test_load_token_nonexistent(self, auth_client):
        """Test de carga de token inexistente"""
        company = "nonexistent_company"
        token = auth_client._load_token(company)
        assert token is None

    @pytest.mark.asyncio
    async def test_authenticate_success(self, auth_client, mock_token_response):
        """Test de autenticación exitosa"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_token_response)
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await auth_client.authenticate("test_company", "test_login", "test_password")

            assert result["success"] is True
            assert result["token"] == "test_token_12345"
            assert "Autenticación exitosa" in result["message"]

    @pytest.mark.asyncio
    async def test_authenticate_failure(self, auth_client, mock_error_response):
        """Test de autenticación fallida"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_error_response
            mock_response.raise_for_status = AsyncMock()
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await auth_client.authenticate("test_company", "test_login", "wrong_password")

            assert result["success"] is False
            assert "Autenticación fallida" in result["message"]

    @pytest.mark.asyncio
    async def test_authenticate_http_error(self, auth_client):
        """Test de error HTTP en autenticación"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.post.side_effect = httpx.HTTPStatusError(
                "403 Forbidden", 
                request=MagicMock(), 
                response=MagicMock(status_code=403)
            )
            mock_client.return_value = mock_client_instance

            result = await auth_client.authenticate("test_company", "test_login", "test_password")

            assert result["success"] is False
            assert "Error HTTP: 403" in result["message"]

    def test_get_auth_headers_success(self, auth_client):
        """Test de obtención de headers de autenticación exitosa"""
        company = "test_company"
        token = "test_token_12345"
        
        # Guardar token primero
        auth_client._save_token(company, token)
        
        headers = auth_client.get_auth_headers(company)
        
        assert headers["X-Company-Login"] == company
        assert headers["X-Token"] == token
        
        # Limpiar archivo de prueba
        os.remove(auth_client._get_token_file_path(company))

    def test_get_auth_headers_no_token(self, auth_client):
        """Test de obtención de headers sin token"""
        company = "test_company"
        
        with pytest.raises(ValueError, match=f"No se encontró token para la empresa {company}"):
            auth_client.get_auth_headers(company)

    @pytest.mark.asyncio
    async def test_validate_token_success(self, auth_client):
        """Test de validación de token exitosa"""
        company = "test_company"
        token = "test_token_12345"
        
        # Guardar token
        auth_client._save_token(company, token)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await auth_client.validate_token(company)

            assert result["valid"] is True
            assert "Token válido" in result["message"]
        
        # Limpiar archivo de prueba
        os.remove(auth_client._get_token_file_path(company))

    @pytest.mark.asyncio
    async def test_validate_token_invalid(self, auth_client):
        """Test de validación de token inválido"""
        company = "test_company"
        token = "invalid_token"
        
        # Guardar token
        auth_client._save_token(company, token)
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 404
            
            mock_client_instance = AsyncMock()
            mock_client_instance.__aenter__.return_value = mock_client_instance
            mock_client_instance.__aexit__.return_value = None
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value = mock_client_instance

            result = await auth_client.validate_token(company)

            assert result["valid"] is False
            assert "Token inválido: 404" in result["message"]
        
        # Limpiar archivo de prueba
        os.remove(auth_client._get_token_file_path(company))

    def test_clear_token(self, auth_client):
        """Test de eliminación de token"""
        company = "test_company"
        token = "test_token_12345"
        
        # Guardar token
        auth_client._save_token(company, token)
        token_path = auth_client._get_token_file_path(company)
        
        # Verificar que existe
        assert os.path.exists(token_path)
        
        # Eliminar token
        result = auth_client.clear_token(company)
        
        assert result is True
        assert not os.path.exists(token_path)

    def test_clear_token_nonexistent(self, auth_client):
        """Test de eliminación de token inexistente"""
        company = "nonexistent_company"
        result = auth_client.clear_token(company)
        assert result is True 