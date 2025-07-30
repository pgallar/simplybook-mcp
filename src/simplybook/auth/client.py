import httpx
import json
import os
import tempfile
import time
import asyncio
from typing import Dict, Any, Optional
from ..http_client import LoggingHTTPClient

class AuthClient:
    def __init__(self):
        self.base_url = "https://user-api-v2.simplybook.me"
        self.auth_url = "https://user-api-v2.simplybook.me/admin/auth"
        self.token_file = None
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 segundo entre solicitudes
        self.max_retries = 3
        self.retry_delay = 5.0  # 5 segundos entre reintentos

    async def authenticate(self, company: str, login: str, password: str) -> Dict[str, Any]:
        """
        Autenticación inicial. Retorna información del token (TokenEntity)
        
        Args:
            company: Company login
            login: User login
            password: User password
            
        Returns:
            TokenEntity con el resultado de la autenticación
            
        Throws:
            AccessDenied: Si el acceso es denegado
            BadRequest: Si los datos proporcionados son inválidos
        """
        for attempt in range(self.max_retries):
            try:
                await self._rate_limit()
                
                async with LoggingHTTPClient(self.base_url, {
                    "Content-Type": "application/json",
                    "User-Agent": "SimplyBook-MCP/1.0"
                }) as client:
                    response = await client.post(
                        "/admin/auth",
                        json={
                            "company": company,
                            "login": login,
                            "password": password
                        }
                    )
                    
                    if response.status_code == 403:
                        if attempt < self.max_retries - 1:
                            print(f"⚠️  Error 403 en intento {attempt + 1}, reintentando en {self.retry_delay} segundos...")
                            await asyncio.sleep(self.retry_delay)
                            self.clear_token(company)
                            continue
                        else:
                            return {
                                "success": False,
                                "message": "Error HTTP: 403 - Acceso denegado después de múltiples intentos",
                                "error": "Posible rate limiting o credenciales bloqueadas temporalmente"
                            }
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    if "token" in result:
                        token = result["token"]
                        self._save_token(company, token)
                        
                        return {
                            "success": True,
                            "token": token,
                            "message": "Autenticación exitosa",
                            "token_file": self._get_token_file_path(company)
                        }
                    else:
                        return {
                            "success": False,
                            "message": "Autenticación fallida",
                            "error": result.get("error", "No se recibió token en la respuesta")
                        }
                        
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️  Error de conexión en intento {attempt + 1}, reintentando en {self.retry_delay} segundos...")
                    await asyncio.sleep(self.retry_delay)
                    continue
                else:
                    return {
                        "success": False,
                        "message": "Error de conexión",
                        "error": str(e)
                    }

    async def authenticate_2fa(self, company: str, session_id: str, code: str, type_2fa: str) -> Dict[str, Any]:
        """
        Autenticación de segundo factor. Retorna información del token (TokenEntity)
        
        Args:
            company: Company login
            session_id: ID de sesión obtenido en el primer paso de autenticación
            code: Código 2FA
            type_2fa: Tipo de 2FA ('ga' o 'sms')
            
        Returns:
            TokenEntity con el resultado de la autenticación
            
        Throws:
            AccessDenied: Si el acceso es denegado
            BadRequest: Si los datos proporcionados son inválidos
        """
        await self._rate_limit()
        
        async with LoggingHTTPClient(self.base_url, {
            "Content-Type": "application/json",
            "User-Agent": "SimplyBook-MCP/1.0"
        }) as client:
            response = await client.post(
                "/admin/auth/2fa",
                json={
                    "company": company,
                    "session_id": session_id,
                    "code": code,
                    "type": type_2fa
                }
            )
            response.raise_for_status()
            return response.json()

    async def request_sms_code(self, company: str, session_id: str) -> None:
        """
        Solicita el código SMS para 2FA
        
        Args:
            company: Company login
            session_id: ID de sesión obtenido en el primer paso de autenticación
            
        Throws:
            AccessDenied: Si el acceso es denegado
            BadRequest: Si los datos proporcionados son inválidos
        """
        await self._rate_limit()
        
        async with LoggingHTTPClient(self.base_url, {
            "Content-Type": "application/json",
            "User-Agent": "SimplyBook-MCP/1.0"
        }) as client:
            response = await client.get(
                "/admin/auth/sms",
                params={
                    "company": company,
                    "session_id": session_id
                }
            )
            response.raise_for_status()

    async def refresh_token(self, company: str, refresh_token: str) -> Dict[str, Any]:
        """
        Renueva el token usando el refresh token
        
        Args:
            company: Company login
            refresh_token: Refresh token obtenido en la autenticación
            
        Returns:
            TokenEntity con el nuevo token
            
        Throws:
            AccessDenied: Si el acceso es denegado
            BadRequest: Si los datos proporcionados son inválidos
        """
        await self._rate_limit()
        
        async with LoggingHTTPClient(self.base_url, {
            "Content-Type": "application/json",
            "User-Agent": "SimplyBook-MCP/1.0"
        }) as client:
            response = await client.post(
                "/admin/auth/refresh-token",
                json={
                    "company": company,
                    "refresh_token": refresh_token
                }
            )
            response.raise_for_status()
            result = response.json()
            
            if "token" in result:
                self._save_token(company, result["token"])
            
            return result

    async def logout(self, company: str, auth_token: str) -> None:
        """
        Cierra la sesión y revoca el token
        
        Args:
            company: Company login
            auth_token: Token a revocar
            
        Throws:
            AccessDenied: Si el acceso es denegado
            BadRequest: Si los datos proporcionados son inválidos
        """
        await self._rate_limit()
        
        headers = self.get_auth_headers(company)
        async with LoggingHTTPClient(self.base_url, headers) as client:
            response = await client.post(
                "/admin/auth/logout",
                json={
                    "auth_token": auth_token
                }
            )
            response.raise_for_status()
            self.clear_token(company)

    def _get_token_file_path(self, company: str) -> str:
        """Obtiene la ruta del archivo temporal para almacenar el token"""
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, f"simplybook_token_{company}.json")
        
    def _save_token(self, company: str, token: str) -> None:
        """Guarda el token en un archivo temporal"""
        token_data = {
            "company": company,
            "token": token,
            "timestamp": str(int(time.time())),
            "created_at": time.time()
        }
        token_file_path = self._get_token_file_path(company)
        
        with open(token_file_path, 'w') as f:
            json.dump(token_data, f)
            
    def _load_token(self, company: str) -> Optional[str]:
        """Carga el token desde el archivo temporal"""
        token_file_path = self._get_token_file_path(company)
        
        if os.path.exists(token_file_path):
            try:
                with open(token_file_path, 'r') as f:
                    token_data = json.load(f)
                    # Verificar si el token no es muy antiguo (máximo 1 hora)
                    created_at = token_data.get("created_at", 0)
                    if time.time() - created_at < 3600:  # 1 hora
                        return token_data.get("token")
                    else:
                        # Token muy antiguo, eliminarlo
                        self.clear_token(company)
            except (json.JSONDecodeError, KeyError):
                pass
        return None
        
    async def _rate_limit(self):
        """Implementa rate limiting para evitar errores 403"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last)
            
        self.last_request_time = time.time()
        
    def get_auth_headers(self, company: str) -> Dict[str, str]:
        """
        Obtiene los headers de autenticación según la documentación de SimplyBook.me
        
        Args:
            company: Company login
            
        Returns:
            Dict con los headers X-Company-Login y X-Token
        """
        token = self._load_token(company)
        if not token:
            raise ValueError(f"No se encontró token para la empresa {company}. Ejecuta authenticate() primero.")
            
        return {
            "X-Company-Login": company,
            "X-Token": token,
            "User-Agent": "SimplyBook-MCP/1.0"
        }
        
    def clear_token(self, company: str) -> bool:
        """
        Elimina el token almacenado
        
        Args:
            company: Company login
            
        Returns:
            True si se eliminó correctamente
        """
        token_file_path = self._get_token_file_path(company)
        if os.path.exists(token_file_path):
            try:
                os.remove(token_file_path)
                return True
            except OSError:
                return False
        return True