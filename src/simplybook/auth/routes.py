from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import AuthClient

class AuthRoutes(BaseRoutes):
    def __init__(self):
        # AuthRoutes no necesita credenciales iniciales
        self.auth_client = AuthClient()
    
    def register_tools(self, mcp):
        # No se registran herramientas públicas de autenticación
        # La autenticación se maneja internamente en base_routes.py
        pass
    
    async def authenticate_internal(self, company: str, login: str, password: str) -> Dict[str, Any]:
        """Método interno para autenticación"""
        try:
            result = await self.auth_client.authenticate(company, login, password)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def validate_token_internal(self, company: str) -> Dict[str, Any]:
        """Método interno para validar token"""
        try:
            # Intentar obtener los headers de autenticación
            # Si no hay error, significa que el token es válido
            self.auth_client.get_auth_headers(company)
            return {
                "valid": True,
                "message": "Token válido"
            }
        except ValueError:
            return {
                "valid": False,
                "message": "Token no encontrado o expirado"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def get_auth_headers_internal(self, company: str) -> Dict[str, str]:
        """Método interno para obtener headers de autenticación"""
        return self.auth_client.get_auth_headers(company)