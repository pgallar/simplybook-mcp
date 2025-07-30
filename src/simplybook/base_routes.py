from typing import Dict, Any
from fastmcp import FastMCP
from .auth.client import AuthClient
import os

class BaseRoutes:
    def __init__(self, company: str = None, login: str = None, password: str = None):
        # Usar variables de entorno si no se proporcionan credenciales
        self.company = company or os.getenv('SIMPLYBOOK_COMPANY')
        self.login = login or os.getenv('SIMPLYBOOK_LOGIN')
        self.password = password or os.getenv('SIMPLYBOOK_PASSWORD')
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
            try:
                self.auth_client.get_auth_headers(self.company)
                return True
            except ValueError:
                pass
                
            # Si no hay token válido, autenticar
            auth_result = await self.auth_client.authenticate(
                self.company, 
                self.login, 
                self.password
            )
            
            if auth_result["success"]:
                # Esperar un momento después de la autenticación exitosa
                import asyncio
                await asyncio.sleep(1)
                return True
            
            return False
            
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