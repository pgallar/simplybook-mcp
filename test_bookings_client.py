#!/usr/bin/env python3
"""
Test script para probar la obtención del listado de bookings del servidor MCP SimplyBook
usando el cliente FastMCP.

Este script asume que el servidor MCP ya está ejecutándose en http://localhost:8000
"""

import asyncio
import json
from fastmcp import Client


async def test_get_bookings_list():
    """Prueba la obtención del listado de bookings"""
    
    # Crear cliente conectado al servidor MCP
    client = Client("http://localhost:8000")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            # Verificar que el servidor está disponible
            await client.ping()
            print("✅ Servidor responde correctamente")
            
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"📋 Herramientas disponibles: {len(tools)}")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # Buscar específicamente la herramienta de bookings
            booking_tools = [tool for tool in tools if 'booking' in tool.name.lower()]
            if booking_tools:
                print(f"\n🎯 Herramientas de bookings encontradas: {len(booking_tools)}")
                for tool in booking_tools:
                    print(f"   - {tool.name}: {tool.description}")
            
            # Ejecutar la herramienta get_bookings_list
            print("\n🔄 Ejecutando get_bookings_list...")
            result = await client.call_tool("get_bookings_list", {})
            
            print("📊 Resultado obtenido:")
            print(json.dumps(result.data, indent=2, ensure_ascii=False))
            
            # Verificar la estructura de la respuesta
            if isinstance(result.data, dict):
                if result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    count = result.data.get("count", 0)
                    print(f"\n✅ Éxito: Se obtuvieron {count} reservas")
                    
                    if bookings:
                        print("\n📋 Primeras reservas:")
                        for i, booking in enumerate(bookings[:3]):  # Mostrar solo las primeras 3
                            print(f"   Reserva {i+1}: {booking.get('id', 'N/A')} - {booking.get('client_name', 'N/A')}")
                    else:
                        print("ℹ️  No hay reservas disponibles")
                else:
                    print(f"❌ Error: {result.data.get('error', 'Error desconocido')}")
            else:
                print(f"⚠️  Respuesta inesperada: {type(result.data)}")
                
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        
        # Verificar si el servidor está ejecutándose
        print("\n🔍 Verificando si el servidor está ejecutándose...")
        print("   Asegúrate de que el servidor MCP esté ejecutándose en http://localhost:8000")
        print("   Puedes iniciarlo con: python src/main.py")


async def test_booking_tools():
    """Prueba todas las herramientas relacionadas con bookings"""
    
    client = Client("http://localhost:8000")
    
    try:
        async with client:
            print("\n🧪 Probando todas las herramientas de bookings...")
            
            tools = await client.list_tools()
            booking_tools = [tool for tool in tools if 'booking' in tool.name.lower()]
            
            for tool in booking_tools:
                print(f"\n🔧 Probando: {tool.name}")
                print(f"   Descripción: {tool.description}")
                
                try:
                    # Para get_bookings_list no necesitamos parámetros
                    if tool.name == "get_bookings_list":
                        result = await client.call_tool(tool.name, {})
                    else:
                        # Para otras herramientas, solo mostramos que están disponibles
                        print(f"   ⚠️  Herramienta disponible pero requiere parámetros específicos")
                        continue
                    
                    if result.data.get("success"):
                        print(f"   ✅ Éxito")
                    else:
                        print(f"   ❌ Error: {result.data.get('error', 'Error desconocido')}")
                        
                except Exception as e:
                    print(f"   ❌ Error ejecutando {tool.name}: {str(e)}")
                    
    except Exception as e:
        print(f"❌ Error general: {str(e)}")


async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del cliente MCP para bookings")
    print("=" * 60)
    
    await test_get_bookings_list()
    await test_booking_tools()
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")


if __name__ == "__main__":
    asyncio.run(main()) 