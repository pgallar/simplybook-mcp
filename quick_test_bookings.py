#!/usr/bin/env python3
"""
Prueba rápida para obtener el listado de bookings del servidor MCP SimplyBook
Compatible con FastMCP 2.10.6 - Versión SSE
"""

import asyncio
import json
from fastmcp import Client


async def quick_test():
    """Prueba rápida del listado de bookings"""
    
    print("🔗 Conectando al servidor MCP SSE...")
    
    try:
        # Usar la URL del servidor SSE
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado exitosamente")
            
            # Verificar que el servidor responde
            await client.ping()
            print("✅ Servidor SSE responde correctamente")
            
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"📋 Herramientas disponibles: {len(tools)}")
            
            # Buscar la herramienta de bookings
            booking_tools = [tool for tool in tools if 'booking' in tool.name.lower()]
            if booking_tools:
                print(f"🎯 Herramientas de bookings encontradas: {len(booking_tools)}")
                for tool in booking_tools:
                    print(f"   - {tool.name}: {tool.description}")
            
            # Ejecutar directamente get_bookings_list
            print("\n🔄 Obteniendo listado de bookings...")
            result = await client.call_tool("get_bookings_list", {})
            
            # Mostrar resultado
            print("\n📊 RESULTADO:")
            print(json.dumps(result.data, indent=2, ensure_ascii=False))
            
            # Verificar el resultado
            if isinstance(result.data, dict):
                if result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    count = result.data.get("count", 0)
                    print(f"\n✅ Éxito: Se obtuvieron {count} reservas")
                else:
                    print(f"\n❌ Error: {result.data.get('error', 'Error desconocido')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n💡 Asegúrate de que:")
        print("   1. El servidor MCP SSE esté ejecutándose en http://localhost:8001/sse/")
        print("   2. Las variables de entorno estén configuradas (SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN, SIMPLYBOOK_PASSWORD)")
        print("   3. El servidor se haya iniciado con: ./start-server-sse.sh")


if __name__ == "__main__":
    asyncio.run(quick_test()) 