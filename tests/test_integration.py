import pytest
import os
import asyncio
from src.simplybook.auth.client import AuthClient
from src.simplybook.services.client import ServicesClient


class TestIntegration:
    """Tests de integración con la API real de SimplyBook.me"""
    
    @pytest.fixture
    def auth_client(self):
        return AuthClient()
    
    @pytest.fixture
    def test_credentials(self):
        """Obtener credenciales de prueba desde variables de entorno"""
        company = os.getenv('SIMPLYBOOK_COMPANY')
        login = os.getenv('SIMPLYBOOK_LOGIN')
        password = os.getenv('SIMPLYBOOK_PASSWORD')
        
        if not all([company, login, password]):
            pytest.skip("Credenciales de prueba no configuradas")
        
        return company, login, password
    
    @pytest.mark.asyncio
    async def test_real_authentication(self, auth_client, test_credentials):
        """Test de autenticación real con SimplyBook.me"""
        company, login, password = test_credentials
        
        result = await auth_client.authenticate(company, login, password)
        
        print(f"Resultado de autenticación: {result}")
        
        # Verificar que la autenticación fue exitosa
        assert result["success"] is True, f"Autenticación fallida: {result}"
        assert "token" in result, "No se recibió token en la respuesta"
        assert result["token"], "Token está vacío"
    
    @pytest.mark.asyncio
    async def test_real_services_list(self, auth_client, test_credentials):
        """Test de obtención de servicios reales"""
        company, login, password = test_credentials
        
        # Autenticar primero
        auth_result = await auth_client.authenticate(company, login, password)
        assert auth_result["success"] is True, "Autenticación fallida"
        
        # Obtener headers de autenticación
        headers = auth_client.get_auth_headers(company)
        
        # Crear cliente de servicios
        services_client = ServicesClient(headers)
        
        try:
            services = await services_client.get_services_list()
            print(f"Servicios obtenidos: {len(services)}")
            
            # Verificar que se obtuvieron servicios
            assert isinstance(services, list), "La respuesta no es una lista"
            
        except Exception as e:
            print(f"Error obteniendo servicios: {e}")
            pytest.fail(f"Error obteniendo servicios: {e}")
    
    @pytest.mark.asyncio
    async def test_real_bookings_list(self, auth_client, test_credentials):
        """Test de obtención de reservas reales"""
        company, login, password = test_credentials
        
        # Autenticar primero
        auth_result = await auth_client.authenticate(company, login, password)
        assert auth_result["success"] is True, "Autenticación fallida"
        
        # Obtener headers de autenticación
        headers = auth_client.get_auth_headers(company)
        
        # Crear cliente de servicios
        services_client = ServicesClient(headers)
        
        try:
            bookings = await services_client.get_bookings()
            print(f"Reservas obtenidas: {len(bookings)}")
            
            # Verificar que se obtuvieron reservas (puede estar vacío)
            assert isinstance(bookings, list), "La respuesta no es una lista"
            
        except Exception as e:
            print(f"Error obteniendo reservas: {e}")
            pytest.fail(f"Error obteniendo reservas: {e}")
    
    @pytest.mark.asyncio
    async def test_real_performers_list(self, auth_client, test_credentials):
        """Test de obtención de performers reales"""
        company, login, password = test_credentials
        
        # Autenticar primero
        auth_result = await auth_client.authenticate(company, login, password)
        assert auth_result["success"] is True, "Autenticación fallida"
        
        # Obtener headers de autenticación
        headers = auth_client.get_auth_headers(company)
        
        # Crear cliente de servicios
        services_client = ServicesClient(headers)
        
        try:
            performers = await services_client.get_performers_list()
            print(f"Performers obtenidos: {len(performers)}")
            
            # Verificar que se obtuvieron performers
            assert isinstance(performers, list), "La respuesta no es una lista"
            
        except Exception as e:
            print(f"Error obteniendo performers: {e}")
            pytest.fail(f"Error obteniendo performers: {e}")
    
    @pytest.mark.asyncio
    async def test_token_validation(self, auth_client, test_credentials):
        """Test de validación de token"""
        company, login, password = test_credentials
        
        # Autenticar primero
        auth_result = await auth_client.authenticate(company, login, password)
        assert auth_result["success"] is True, "Autenticación fallida"
        
        # Validar token
        validation_result = await auth_client.validate_token(company)
        print(f"Resultado de validación: {validation_result}")
        
        # Verificar que el token es válido
        assert validation_result["valid"] is True, f"Token inválido: {validation_result}" 