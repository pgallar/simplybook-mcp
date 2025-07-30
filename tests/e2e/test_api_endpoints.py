#!/usr/bin/env python3
"""
Script para probar todos los endpoints de la API SimplyBook.me
y detectar errores de "Invalid request parameters"
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def test_all_endpoints():
    """Probar todos los endpoints de la API"""
    
    print("🔗 Conectando al servidor MCP SSE...")
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado exitosamente")
            
            # Esperar inicialización
            print("⏳ Esperando inicialización del servidor...")
            await asyncio.sleep(5)
            
            # Verificar que el servidor responde
            await client.ping()
            print("✅ Servidor SSE responde correctamente")
            
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"📋 Herramientas disponibles: {len(tools)}")
            
            # La autenticación ahora es interna y automática
            print("\n🔐 Autenticación interna automática")
            print("✅ Usando credenciales del archivo .env")
            
            # Esperar para que la autenticación interna se complete
            await asyncio.sleep(2)
            
            # Probar get_services_list
            print("\n📋 Probando get_services_list...")
            try:
                result = await client.call_tool("get_services_list", {})
                print("✅ get_services_list ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    services = result.data.get("services", [])
                    print(f"📊 Servicios obtenidos: {len(services)}")
                else:
                    print(f"❌ Error en get_services_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_services_list: {e}")
            
            # Probar get_performers_list
            print("\n👥 Probando get_performers_list...")
            try:
                result = await client.call_tool("get_performers_list", {})
                print("✅ get_performers_list ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    performers = result.data.get("performers", [])
                    print(f"📊 Performers obtenidos: {len(performers)}")
                else:
                    print(f"❌ Error en get_performers_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_performers_list: {e}")
            
            # Probar get_bookings_list
            print("\n📅 Probando get_bookings_list...")
            try:
                result = await client.call_tool("get_bookings_list", {})
                print("✅ get_bookings_list ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    print(f"📊 Reservas obtenidas: {len(bookings)}")
                else:
                    print(f"❌ Error en get_bookings_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_bookings_list: {e}")
            
            # Probar get_bookings con parámetros de fecha
            print("\n📅 Probando get_bookings con parámetros de fecha...")
            try:
                tomorrow = datetime.now() + timedelta(days=1)
                tomorrow_str = tomorrow.strftime("%Y-%m-%d")
                
                result = await client.call_tool("get_bookings", {
                    "date_from": tomorrow_str,
                    "date_to": tomorrow_str
                })
                print("✅ get_bookings con parámetros ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    print(f"📊 Reservas para mañana: {len(bookings)}")
                else:
                    print(f"❌ Error en get_bookings con parámetros: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_bookings con parámetros: {e}")
            
            # Probar get_clients_list
            print("\n👤 Probando get_clients_list...")
            try:
                result = await client.call_tool("get_clients_list", {})
                print("✅ get_clients_list ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    clients = result.data.get("clients", [])
                    print(f"📊 Clientes obtenidos: {len(clients)}")
                else:
                    print(f"❌ Error en get_clients_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_clients_list: {e}")
            
            # Probar get_providers_list
            print("\n🏥 Probando get_providers_list...")
            try:
                result = await client.call_tool("get_providers_list", {})
                print("✅ get_providers_list ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    providers = result.data.get("providers", [])
                    print(f"📊 Proveedores obtenidos: {len(providers)}")
                else:
                    print(f"❌ Error en get_providers_list: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_providers_list: {e}")
            
            # Probar get_available_slots con parámetros
            print("\n⏰ Probando get_available_slots...")
            try:
                result = await client.call_tool("get_available_slots", {
                    "service_id": "2",
                    "date": "2025-07-30"
                })
                print("✅ get_available_slots ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    slots = result.data.get("slots", [])
                    print(f"📊 Slots disponibles: {len(slots)}")
                else:
                    print(f"❌ Error en get_available_slots: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_available_slots: {e}")
            
            # Probar get_calendar_data con parámetros
            print("\n📅 Probando get_calendar_data...")
            try:
                result = await client.call_tool("get_calendar_data", {
                    "start_date": "2025-07-30",
                    "end_date": "2025-07-30"
                })
                print("✅ get_calendar_data ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    calendar_data = result.data.get("calendar_data", [])
                    print(f"📊 Datos del calendario: {len(calendar_data) if isinstance(calendar_data, list) else 'N/A'}")
                else:
                    print(f"❌ Error en get_calendar_data: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_calendar_data: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        print(f"   Tipo de error: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(test_all_endpoints()) 