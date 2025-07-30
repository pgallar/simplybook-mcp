#!/usr/bin/env python3
"""
Script para verificar y analizar los logs de la API de SimplyBook.me
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


def read_api_logs(log_file: str = "logs/simplybook_api.log") -> List[Dict[str, Any]]:
    """Leer y parsear los logs de la API"""
    logs = []
    
    if not os.path.exists(log_file):
        print(f"❌ Archivo de log no encontrado: {log_file}")
        return logs
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Dividir por líneas de log (timestamp al inicio)
        lines = content.split('\n')
        current_log = ""
        in_json = False
        
        for line in lines:
            # Verificar si es una nueva línea de log (empieza con timestamp)
            if line.startswith('2025-') and ('API REQUEST' in line or 'API RESPONSE' in line or 'API ERROR' in line):
                # Procesar el log anterior si existe
                if current_log and in_json:
                    try:
                        # Extraer el JSON del log
                        start_idx = current_log.find('{')
                        if start_idx != -1:
                            json_str = current_log[start_idx:]
                            log_entry = json.loads(json_str)
                            logs.append(log_entry)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Error parseando JSON: {e}")
                        print(f"   Log: {current_log[:100]}...")
                
                # Iniciar nuevo log
                current_log = line
                in_json = '{' in line
            elif in_json and line.strip():
                # Continuar acumulando el JSON
                current_log += '\n' + line
            elif in_json and not line.strip():
                # Línea vacía, seguir acumulando
                current_log += '\n'
        
        # Procesar el último log
        if current_log and in_json:
            try:
                start_idx = current_log.find('{')
                if start_idx != -1:
                    json_str = current_log[start_idx:]
                    log_entry = json.loads(json_str)
                    logs.append(log_entry)
            except json.JSONDecodeError as e:
                print(f"⚠️  Error parseando último JSON: {e}")
    
    except Exception as e:
        print(f"❌ Error leyendo logs: {e}")
    
    return logs


def analyze_logs(logs: List[Dict[str, Any]]) -> None:
    """Analizar los logs y mostrar estadísticas"""
    if not logs:
        print("📭 No se encontraron logs de API")
        return
    
    print(f"📊 Análisis de {len(logs)} entradas de log")
    print("=" * 60)
    
    # Estadísticas generales
    requests = [log for log in logs if "request_id" in log and "method" in log]
    responses = [log for log in logs if "request_id" in log and "status_code" in log]
    errors = [log for log in logs if "error" in log]
    
    print(f"📤 Requests: {len(requests)}")
    print(f"📥 Responses: {len(responses)}")
    print(f"❌ Errors: {len(errors)}")
    
    # Análisis por método HTTP
    methods = {}
    for req in requests:
        method = req.get("method", "UNKNOWN")
        methods[method] = methods.get(method, 0) + 1
    
    print(f"\n🔗 Métodos HTTP:")
    for method, count in methods.items():
        print(f"   {method}: {count}")
    
    # Análisis por endpoint
    endpoints = {}
    for req in requests:
        url = req.get("url", "")
        if "simplybook.me" in url:
            endpoint = url.split("simplybook.me")[-1]
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
    
    print(f"\n🎯 Endpoints más usados:")
    for endpoint, count in sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {endpoint}: {count}")
    
    # Análisis de códigos de estado
    status_codes = {}
    for resp in responses:
        status = resp.get("status_code", 0)
        status_codes[status] = status_codes.get(status, 0) + 1
    
    print(f"\n📊 Códigos de estado:")
    for status, count in sorted(status_codes.items()):
        print(f"   {status}: {count}")
    
    # Análisis de duración
    durations = [resp.get("duration_ms", 0) for resp in responses if resp.get("duration_ms")]
    if durations:
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)
        
        print(f"\n⏱️  Duración de requests:")
        print(f"   Promedio: {avg_duration:.2f}ms")
        print(f"   Máximo: {max_duration:.2f}ms")
        print(f"   Mínimo: {min_duration:.2f}ms")
    
    # Mostrar errores recientes
    if errors:
        print(f"\n❌ Errores recientes:")
        for error in errors[-5:]:  # Últimos 5 errores
            print(f"   {error.get('timestamp', 'N/A')}: {error.get('error', 'N/A')}")


def show_recent_requests(logs: List[Dict[str, Any]], limit: int = 10) -> None:
    """Mostrar los requests más recientes"""
    requests = [log for log in logs if "request_id" in log and "method" in log]
    
    if not requests:
        print("📭 No se encontraron requests")
        return
    
    # Ordenar por timestamp
    requests.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    print(f"\n🕒 Últimos {min(limit, len(requests))} requests:")
    print("=" * 60)
    
    for req in requests[:limit]:
        request_id = req.get("request_id", "N/A")
        timestamp = req.get("timestamp", "N/A")
        method = req.get("method", "N/A")
        url = req.get("url", "N/A")
        
        # Buscar la respuesta correspondiente
        response = None
        for resp in logs:
            if resp.get("request_id") == request_id and "status_code" in resp:
                response = resp
                break
        
        status_code = response.get("status_code", "N/A") if response else "N/A"
        duration = response.get("duration_ms", "N/A") if response else "N/A"
        
        print(f"📤 {timestamp}")
        print(f"   ID: {request_id}")
        print(f"   {method} {url}")
        print(f"   Status: {status_code} | Duration: {duration}ms")
        print()


def main():
    """Función principal"""
    print("🔍 Analizador de logs de API SimplyBook.me")
    print("=" * 60)
    
    # Leer logs
    logs = read_api_logs()
    
    if not logs:
        print("❌ No se encontraron logs para analizar")
        return
    
    # Analizar logs
    analyze_logs(logs)
    
    # Mostrar requests recientes
    show_recent_requests(logs, limit=5)
    
    # Mostrar archivo de log
    log_file = "logs/simplybook_api.log"
    if os.path.exists(log_file):
        file_size = os.path.getsize(log_file)
        print(f"📁 Archivo de log: {log_file}")
        print(f"📏 Tamaño: {file_size} bytes")
        print(f"📅 Última modificación: {datetime.fromtimestamp(os.path.getmtime(log_file))}")


if __name__ == "__main__":
    main() 