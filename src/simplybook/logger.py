import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import os


def is_logging_enabled() -> bool:
    """Verificar si el logging de API está habilitado"""
    return os.getenv('ENABLE_API_LOGGING', 'true').lower() in ('true', '1', 'yes', 'on')


class SimplyBookLogger:
    """Logger centralizado para todas las llamadas a la API de SimplyBook.me"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configurar el logger"""
        logger = logging.getLogger('simplybook_api')
        logger.setLevel(logging.INFO)
        
        # Evitar duplicar handlers
        if not logger.handlers:
            # Handler para archivo
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            file_handler = logging.FileHandler(f"{log_dir}/simplybook_api.log")
            file_handler.setLevel(logging.INFO)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    def log_request(self, method: str, url: str, headers: Dict[str, str], 
                   data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Loggear un request a la API
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL del endpoint
            headers: Headers del request
            data: Datos del body (para POST/PUT)
            params: Parámetros de query (para GET)
            
        Returns:
            ID único del request para correlacionar con la respuesta
        """
        # Verificar si el logging está habilitado
        if not is_logging_enabled():
            return f"req_{int(time.time() * 1000)}"
        
        request_id = f"req_{int(time.time() * 1000)}"
        
        # Ocultar información sensible en los logs
        safe_headers = self._sanitize_headers(headers)
        safe_data = self._sanitize_data(data) if data else None
        
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "url": url,
            "headers": safe_headers,
            "data": safe_data,
            "params": params
        }
        
        self.logger.info(f"API REQUEST [{request_id}]: {json.dumps(log_entry, indent=2)}")
        return request_id
    
    def log_response(self, request_id: str, status_code: int, 
                    response_data: Optional[Dict[str, Any]] = None,
                    error: Optional[str] = None, duration_ms: Optional[float] = None) -> None:
        """
        Loggear una respuesta de la API
        
        Args:
            request_id: ID del request correspondiente
            status_code: Código de estado HTTP
            response_data: Datos de la respuesta
            error: Mensaje de error si existe
            duration_ms: Duración del request en milisegundos
        """
        # Verificar si el logging está habilitado
        if not is_logging_enabled():
            return
        
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "status_code": status_code,
            "duration_ms": duration_ms,
            "success": status_code < 400
        }
        
        if response_data:
            log_entry["response_data"] = self._sanitize_data(response_data)
        
        if error:
            log_entry["error"] = error
            
        self.logger.info(f"API RESPONSE [{request_id}]: {json.dumps(log_entry, indent=2)}")
    
    def log_error(self, request_id: str, error: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Loggear un error específico
        
        Args:
            request_id: ID del request correspondiente
            error: Mensaje de error
            context: Contexto adicional del error
        """
        # Verificar si el logging está habilitado
        if not is_logging_enabled():
            return
        
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "context": context
        }
        
        self.logger.error(f"API ERROR [{request_id}]: {json.dumps(log_entry, indent=2)}")
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Ocultar información sensible en los headers"""
        safe_headers = headers.copy()
        
        # Ocultar tokens y credenciales
        sensitive_keys = ['x-token', 'authorization', 'x-company-login']
        for key in sensitive_keys:
            if key.lower() in safe_headers:
                safe_headers[key] = '***HIDDEN***'
        
        return safe_headers
    
    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ocultar información sensible en los datos"""
        if not data:
            return data
            
        safe_data = data.copy()
        
        # Ocultar campos sensibles
        sensitive_fields = ['password', 'token', 'api_key', 'secret']
        for field in sensitive_fields:
            if field in safe_data:
                safe_data[field] = '***HIDDEN***'
        
        return safe_data


# Instancia global del logger
api_logger = SimplyBookLogger() 