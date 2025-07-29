from typing import Dict, Any
from ..base_routes import BaseRoutes
from .client import AuthClient

class AuthRoutes(BaseRoutes):
    def __init__(self):
        # AuthRoutes no necesita credenciales iniciales
        self.auth_client = AuthClient()
    def register_tools(self, mcp):
        @mcp.tool()
        async def authenticate(company: str, login: str, password: str) -> Dict[str, Any]:
            """Autenticar usuario con SimplyBook.me"""
            try:
                result = await self.auth_client.authenticate(company, login, password)
                return result
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }

        @mcp.tool()
        async def validate_token(company: str) -> Dict[str, Any]:
            """Validar si el token actual es válido"""
            try:
                result = await self.auth_client.validate_token(company)
                return result
            except Exception as e:
                return {
                    "valid": False,
                    "error": str(e)
                }

        @mcp.tool()
        async def clear_token(company: str) -> Dict[str, Any]:
            """Eliminar el token almacenado"""
            try:
                success = self.auth_client.clear_token(company)
                return {
                    "success": success,
                    "message": "Token eliminado" if success else "Error eliminando token"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }

        @mcp.tool()
        async def get_auth_status(company: str) -> Dict[str, Any]:
            """Obtener el estado de autenticación"""
            try:
                validation = await self.auth_client.validate_token(company)
                
                if validation.get("valid", False):
                    return {
                        "authenticated": True,
                        "message": "Usuario autenticado",
                        "token_file": self.auth_client._get_token_file_path(company)
                    }
                else:
                    return {
                        "authenticated": False,
                        "message": "Usuario no autenticado",
                        "error": validation.get("message", "Error desconocido")
                    }
            except Exception as e:
                return {
                    "authenticated": False,
                    "error": str(e)
                }