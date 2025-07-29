from typing import Dict, Any
from fastmcp import FastMCP
from .auth.client import AuthClient

class BaseRoutes:
    def __init__(self, company: str, login: str, password: str):
        self.company = company
        self.login = login
        self.password = password
        self.auth_client = AuthClient()
        self.client = None

    def register_tools(self, mcp: FastMCP) -> None:
        """Registra las herramientas de este router en la instancia de FastMCP"""
        pass
        
    async def ensure_authenticated(self) -> bool:
        """
        Asegura que el usuario esté autenticado antes de hacer llamadas a la API
        
        Returns:
            True si la autenticación es exitosa
        """
        try:
            # Verificar si ya tenemos un token válido
            validation = await self.auth_client.validate_token(self.company)
            if validation["valid"]:
                return True
                
            # Si no hay token válido, autenticar
            auth_result = await self.auth_client.authenticate(
                self.company, 
                self.login, 
                self.password
            )
            
            return auth_result["success"]
            
        except Exception as e:
            print(f"Error en autenticación: {str(e)}")
            return False
            
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Obtiene los headers de autenticación para las llamadas a la API
        
        Returns:
            Dict con los headers X-Company-Login y X-Token
        """
        return self.auth_client.get_auth_headers(self.company)