#!/usr/bin/env python3
"""
Script para probar el control de logging mediante la variable ENABLE_API_LOGGING
"""

import asyncio
import os
import subprocess
from fastmcp import Client


async def test_logging_control():
    """Probar el control de logging"""
    
    print("🔧 Probando control de logging de API")
    print("=" * 50)
    
    # Verificar el estado actual del logging
    current_logging = os.getenv('ENABLE_API_LOGGING', 'true')
    print(f"📊 Estado actual de ENABLE_API_LOGGING: {current_logging}")
    
    # Probar con logging habilitado
    print(f"\n✅ Probando con logging HABILITADO...")
    await test_api_calls("Logging habilitado")
    
    # Deshabilitar logging
    print(f"\n❌ Deshabilitando logging...")
    os.environ['ENABLE_API_LOGGING'] = 'false'
    
    # Probar con logging deshabilitado
    print(f"✅ Probando con logging DESHABILITADO...")
    await test_api_calls("Logging deshabilitado")
    
    # Rehabilitar logging
    print(f"\n✅ Rehabilitando logging...")
    os.environ['ENABLE_API_LOGGING'] = 'true'
    
    # Probar con logging rehabilitado
    print(f"✅ Probando con logging REHABILITADO...")
    await test_api_calls("Logging rehabilitado")
    
    print(f"\n🎯 Prueba completada. Verifica los logs para confirmar el comportamiento.")


async def test_api_calls(test_name: str):
    """Realizar llamadas de prueba a la API"""
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print(f"   🔗 Conectado al servidor MCP SSE")
            
            # Esperar inicialización
            await asyncio.sleep(3)
            
            # La autenticación ahora es interna y automática
            print(f"   🔐 Autenticación interna automática")
            print(f"   ✅ Usando credenciales del archivo .env")
            
            # Esperar para que la autenticación interna se complete
            await asyncio.sleep(2)
            
            # Hacer algunas llamadas de prueba
            print(f"   📋 Obteniendo servicios...")
            services_result = await client.call_tool("get_services_list", {})
            if services_result.data.get("success"):
                print(f"   ✅ Servicios obtenidos")
            
            await asyncio.sleep(1)
            
            print(f"   📅 Obteniendo reservas...")
            bookings_result = await client.call_tool("get_bookings_list", {})
            if bookings_result.data.get("success"):
                print(f"   ✅ Reservas obtenidas")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")


def check_log_file():
    """Verificar el archivo de log"""
    log_file = "logs/simplybook_api.log"
    
    if os.path.exists(log_file):
        # Obtener el tamaño del archivo
        file_size = os.path.getsize(log_file)
        
        # Contar líneas de log de API
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                api_request_lines = content.count('API REQUEST')
                api_response_lines = content.count('API RESPONSE')
                api_error_lines = content.count('API ERROR')
                
            print(f"\n📁 Archivo de log: {log_file}")
            print(f"📏 Tamaño: {file_size} bytes")
            print(f"📤 API REQUEST lines: {api_request_lines}")
            print(f"📥 API RESPONSE lines: {api_response_lines}")
            print(f"❌ API ERROR lines: {api_error_lines}")
            
        except Exception as e:
            print(f"❌ Error leyendo archivo de log: {e}")
    else:
        print(f"❌ Archivo de log no encontrado: {log_file}")


def main():
    """Función principal"""
    print("🔧 Control de Logging de API SimplyBook.me")
    print("=" * 50)
    
    # Verificar estado inicial
    check_log_file()
    
    # Ejecutar pruebas
    asyncio.run(test_logging_control())
    
    # Verificar estado final
    print(f"\n📊 Estado final:")
    check_log_file()
    
    print(f"\n💡 Para cambiar el logging:")
    print(f"   - Habilitar: ENABLE_API_LOGGING=true")
    print(f"   - Deshabilitar: ENABLE_API_LOGGING=false")
    print(f"   - En .env: ENABLE_API_LOGGING=true/false")


if __name__ == "__main__":
    main() 