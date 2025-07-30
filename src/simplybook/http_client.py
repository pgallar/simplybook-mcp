import httpx
import time
from typing import Dict, Any, Optional
from .logger import api_logger


class LoggingHTTPClient:
    """Cliente HTTP wrapper que loggee todas las llamadas a la API de SimplyBook.me"""
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Realizar una petición GET con logging"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        request_id = None
        
        try:
            # Loggear el request
            request_id = api_logger.log_request(
                method="GET",
                url=url,
                headers=self.headers,
                params=params
            )
            
            # Realizar la petición
            response = await self.client.get(url, headers=self.headers, params=params)
            
            # Calcular duración
            duration_ms = (time.time() - start_time) * 1000
            
            # Loggear la respuesta
            try:
                response_data = response.json() if response.content else None
            except:
                response_data = None
                
            api_logger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                response_data=response_data,
                duration_ms=duration_ms
            )
            
            return response
            
        except Exception as e:
            # Loggear el error
            if request_id:
                api_logger.log_error(
                    request_id=request_id,
                    error=str(e),
                    context={"method": "GET", "url": url}
                )
            raise
    
    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Realizar una petición POST con logging"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        request_id = None
        
        try:
            # Loggear el request
            request_id = api_logger.log_request(
                method="POST",
                url=url,
                headers=self.headers,
                data=json
            )
            
            # Realizar la petición
            response = await self.client.post(url, headers=self.headers, json=json)
            
            # Calcular duración
            duration_ms = (time.time() - start_time) * 1000
            
            # Loggear la respuesta
            try:
                response_data = response.json() if response.content else None
            except:
                response_data = None
                
            api_logger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                response_data=response_data,
                duration_ms=duration_ms
            )
            
            return response
            
        except Exception as e:
            # Loggear el error
            if request_id:
                api_logger.log_error(
                    request_id=request_id,
                    error=str(e),
                    context={"method": "POST", "url": url}
                )
            raise
    
    async def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Realizar una petición PUT con logging"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        request_id = None
        
        try:
            # Loggear el request
            request_id = api_logger.log_request(
                method="PUT",
                url=url,
                headers=self.headers,
                data=json
            )
            
            # Realizar la petición
            response = await self.client.put(url, headers=self.headers, json=json)
            
            # Calcular duración
            duration_ms = (time.time() - start_time) * 1000
            
            # Loggear la respuesta
            try:
                response_data = response.json() if response.content else None
            except:
                response_data = None
                
            api_logger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                response_data=response_data,
                duration_ms=duration_ms
            )
            
            return response
            
        except Exception as e:
            # Loggear el error
            if request_id:
                api_logger.log_error(
                    request_id=request_id,
                    error=str(e),
                    context={"method": "PUT", "url": url}
                )
            raise
    
    async def delete(self, endpoint: str) -> httpx.Response:
        """Realizar una petición DELETE con logging"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        request_id = None
        
        try:
            # Loggear el request
            request_id = api_logger.log_request(
                method="DELETE",
                url=url,
                headers=self.headers
            )
            
            # Realizar la petición
            response = await self.client.delete(url, headers=self.headers)
            
            # Calcular duración
            duration_ms = (time.time() - start_time) * 1000
            
            # Loggear la respuesta
            try:
                response_data = response.json() if response.content else None
            except:
                response_data = None
                
            api_logger.log_response(
                request_id=request_id,
                status_code=response.status_code,
                response_data=response_data,
                duration_ms=duration_ms
            )
            
            return response
            
        except Exception as e:
            # Loggear el error
            if request_id:
                api_logger.log_error(
                    request_id=request_id,
                    error=str(e),
                    context={"method": "DELETE", "url": url}
                )
            raise
    
    async def close(self):
        """Cerrar el cliente HTTP"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close() 