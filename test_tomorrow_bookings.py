#!/usr/bin/env python3
"""
Prueba específica para consultar agendamientos de mañana
Con manejo de inicialización del servidor MCP
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def test_tomorrow_bookings():
    """Prueba consulta de agendamientos de mañana"""
    
    print("🔗 Conectando al servidor MCP SSE...")
    
    try:
        # Usar la URL del servidor SSE
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado exitosamente")
            
            # Esperar a que el servidor esté completamente inicializado
            print("⏳ Esperando inicialización del servidor...")
            await asyncio.sleep(3)  # Esperar 3 segundos para inicialización completa
            
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
            
            # Calcular fecha de mañana
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            print(f"\n📅 Consultando agendamientos para mañana: {tomorrow_str}")
            
            # Probar get_bookings_list (todas las reservas)
            print("\n🔄 Obteniendo todas las reservas...")
            try:
                result = await client.call_tool("get_bookings_list", {})
                print("✅ get_bookings_list ejecutado correctamente")
                if isinstance(result.data, dict) and result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    print(f"📊 Total de reservas: {len(bookings)}")
                else:
                    print(f"❌ Error en get_bookings_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_bookings_list: {e}")
            
            # Probar get_bookings con filtro de fecha (desde services)
            print(f"\n🔄 Obteniendo reservas para mañana ({tomorrow_str})...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": tomorrow_str,
                    "date_to": tomorrow_str
                })
                print("✅ get_bookings ejecutado correctamente")
                if isinstance(result.data, dict) and result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    print(f"📊 Reservas para mañana: {len(bookings)}")
                    if bookings:
                        print("📋 Detalles de las reservas:")
                        # Mostrar solo las primeras 5 reservas de forma segura
                        for i, booking in enumerate(bookings[:5] if isinstance(bookings, list) else [], 1):
                            print(f"   {i}. ID: {booking.get('id')} - Fecha: {booking.get('start_datetime', 'N/A')}")
                    else:
                        print("📭 No hay reservas para mañana")
                else:
                    print(f"❌ Error en get_bookings: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_bookings: {e}")
            
            # Probar get_calendar_data con rango de fechas
            print(f"\n🔄 Obteniendo datos del calendario para mañana...")
            try:
                result = await client.call_tool("get_calendar_data", {
                    "start_date": tomorrow_str,
                    "end_date": tomorrow_str
                })
                print("✅ get_calendar_data ejecutado correctamente")
                if isinstance(result.data, dict) and result.data.get("success"):
                    calendar_data = result.data.get("calendar_data", [])
                    print(f"📊 Datos del calendario: {len(calendar_data) if isinstance(calendar_data, list) else 'N/A'}")
                else:
                    print(f"❌ Error en get_calendar_data: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_calendar_data: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n💡 Asegúrate de que:")
        print("   1. El servidor MCP SSE esté ejecutándose en http://localhost:8001/sse/")
        print("   2. Las variables de entorno estén configuradas (SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN, SIMPLYBOOK_PASSWORD)")
        print("   3. El servidor se haya iniciado con: ./start-server-sse.sh")


if __name__ == "__main__":
    asyncio.run(test_tomorrow_bookings()) 