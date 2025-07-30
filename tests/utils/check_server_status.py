#!/usr/bin/env python3
"""
Script para verificar el estado del servidor MCP SSE
y detectar problemas de inicialización
"""

import asyncio
import httpx
import json
from datetime import datetime


async def check_server_status():
    """Verificar el estado del servidor MCP SSE"""
    
    print(f"🔍 Verificando estado del servidor MCP SSE - {datetime.now()}")
    print("=" * 60)
    
    # Verificar conectividad básica
    print("1️⃣ Verificando conectividad básica...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Probar endpoint SSE
            response = await client.get("http://localhost:8001/sse/")
            print(f"   ✅ Endpoint SSE: HTTP {response.status_code}")
            
            # Verificar que es un stream de eventos
            if "text/event-stream" in response.headers.get("content-type", ""):
                print("   ✅ Content-Type correcto: text/event-stream")
            else:
                print(f"   ⚠️  Content-Type inesperado: {response.headers.get('content-type')}")
                
    except Exception as e:
        print(f"   ❌ Error de conectividad: {e}")
        return False
    
    # Verificar conexión MCP
    print("\n2️⃣ Verificando conexión MCP...")
    try:
        from fastmcp import Client
        
        client = Client("http://localhost:8001/sse")
        
        async with client:
            # Esperar inicialización
            await asyncio.sleep(2)
            
            # Ping al servidor
            await client.ping()
            print("   ✅ Ping exitoso")
            
            # Listar herramientas
            tools = await client.list_tools()
            print(f"   ✅ Herramientas disponibles: {len(tools)}")
            
            # Verificar herramientas críticas
            critical_tools = ["authenticate", "get_bookings_list", "get_services_list"]
            missing_tools = []
            
            for tool_name in critical_tools:
                if not any(tool.name == tool_name for tool in tools):
                    missing_tools.append(tool_name)
            
            if missing_tools:
                print(f"   ⚠️  Herramientas faltantes: {missing_tools}")
            else:
                print("   ✅ Todas las herramientas críticas disponibles")
                
    except Exception as e:
        print(f"   ❌ Error de conexión MCP: {e}")
        return False
    
    # Verificar logs recientes
    print("\n3️⃣ Verificando logs recientes...")
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "logs", "--tail", "10", "simplybook-mcp"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            logs = result.stdout
            if "Failed to validate request" in logs:
                print("   ⚠️  Se detectaron errores de inicialización en los logs")
                print("   📋 Últimos logs:")
                for line in logs.strip().split('\n')[-5:]:
                    print(f"      {line}")
            else:
                print("   ✅ No se detectaron errores de inicialización")
        else:
            print("   ⚠️  No se pudieron obtener logs del contenedor")
            
    except Exception as e:
        print(f"   ⚠️  Error obteniendo logs: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Verificación completada")
    return True


async def monitor_server_health():
    """Monitorear la salud del servidor continuamente"""
    
    print("🔄 Iniciando monitoreo continuo del servidor...")
    print("Presiona Ctrl+C para detener")
    
    try:
        while True:
            await check_server_status()
            print(f"\n⏰ Próxima verificación en 60 segundos...")
            await asyncio.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoreo detenido por el usuario")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        asyncio.run(monitor_server_health())
    else:
        asyncio.run(check_server_status()) 