#!/usr/bin/env python3
"""
Script de prueba para testear la conexión SSE del servidor MCP SimplyBook
"""

import asyncio
import json
import time
from fastmcp import Client


async def test_sse_connection():
    """Prueba la conexión SSE al servidor MCP"""
    
    print("🔌 Probando conexión SSE al servidor MCP")
    print("=" * 60)
    
    # URL del servidor SSE
    sse_url = "http://localhost:8001/mcp"
    
    print(f"🌐 Conectando a: {sse_url}")
    print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
    
    try:
        client = Client(sse_url)
        
        async with client:
            print("✅ Conectado exitosamente al servidor SSE")
            
            # Verificar que el servidor responde
            await client.ping()
            print("✅ Servidor SSE responde correctamente")
            
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"📋 Herramientas disponibles: {len(tools)}")
            
            # Buscar herramientas de bookings
            booking_tools = [tool for tool in tools if 'booking' in tool.name.lower()]
            if booking_tools:
                print(f"🎯 Herramientas de bookings encontradas: {len(booking_tools)}")
                for tool in booking_tools:
                    print(f"   - {tool.name}: {tool.description}")
            
            # Probar la herramienta get_bookings_list
            print("\n🔄 Probando get_bookings_list via SSE...")
            result = await client.call_tool("get_bookings_list", {})
            
            if result.data.get("success"):
                bookings = result.data.get("bookings", [])
                count = result.data.get("count", 0)
                print(f"✅ Éxito SSE: {count} reservas obtenidas")
                print(f"📊 Total de reservas: {len(bookings)}")
                
                if bookings:
                    print("\n📋 Primeras reservas:")
                    for i, booking in enumerate(bookings[:3]):
                        client_name = booking.get('client', {}).get('name', 'N/A')
                        service_name = booking.get('service', {}).get('name', 'N/A')
                        print(f"   {i+1}. {client_name} - {service_name}")
            else:
                error = result.data.get("error", "Error desconocido")
                print(f"❌ Error SSE: {error}")
                
    except Exception as e:
        print(f"❌ Error conectando a SSE: {e}")
        print(f"   Tipo de error: {type(e).__name__}")


async def test_sse_performance():
    """Prueba el rendimiento del servidor SSE"""
    
    print("\n⚡ Probando rendimiento del servidor SSE")
    print("=" * 60)
    
    sse_url = "http://localhost:8001/mcp"
    
    # Realizar múltiples solicitudes para medir rendimiento
    times = []
    successes = 0
    total_requests = 5
    
    for i in range(total_requests):
        print(f"\n🔄 Solicitud #{i + 1}")
        try:
            start_time = time.time()
            client = Client(sse_url)
            
            async with client:
                await client.ping()
                result = await client.call_tool("get_bookings_list", {})
                end_time = time.time()
                
                request_time = end_time - start_time
                times.append(request_time)
                
                if result.data.get("success"):
                    successes += 1
                    print(f"✅ Éxito: {request_time:.2f}s")
                else:
                    print(f"❌ Error: {request_time:.2f}s")
                    
        except Exception as e:
            print(f"❌ Excepción: {e}")
            times.append(None)
    
    # Calcular estadísticas
    print(f"\n📊 Estadísticas de rendimiento:")
    print("=" * 40)
    
    valid_times = [t for t in times if t is not None]
    if valid_times:
        avg_time = sum(valid_times) / len(valid_times)
        min_time = min(valid_times)
        max_time = max(valid_times)
        
        print(f"📈 Tiempo promedio: {avg_time:.2f}s")
        print(f"📈 Tiempo mínimo: {min_time:.2f}s")
        print(f"📈 Tiempo máximo: {max_time:.2f}s")
        print(f"📈 Solicitudes exitosas: {successes}/{total_requests}")
    else:
        print("❌ No se pudieron medir tiempos")


async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del servidor SSE")
    print("=" * 60)
    
    await test_sse_connection()
    await test_sse_performance()
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")
    print("\n💡 Configuración SSE:")
    print("   - URL: http://localhost:8001/mcp")
    print("   - Transport: SSE")
    print("   - Config: claude-desktop-config-sse.json")


if __name__ == "__main__":
    asyncio.run(main()) 