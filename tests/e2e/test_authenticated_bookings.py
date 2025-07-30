#!/usr/bin/env python3
"""
Prueba de agendamientos de mañana con autenticación explícita
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def test_authenticated_bookings():
    """Prueba consulta de agendamientos con autenticación explícita"""
    
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
            
            # Buscar herramientas de autenticación
            auth_tools = [tool for tool in tools if 'auth' in tool.name.lower() or 'authenticate' in tool.name.lower()]
            if auth_tools:
                print(f"🔐 Herramientas de autenticación encontradas: {len(auth_tools)}")
                for tool in auth_tools:
                    print(f"   - {tool.name}: {tool.description}")
            
            # Autenticar primero
            print("\n🔐 Autenticando con SimplyBook.me...")
            try:
                auth_result = await client.call_tool("authenticate", {
                    "company": "rominacostasestetica",
                    "login": "roalecos@gmail.com",
                    "password": "!Quitucho1712"
                })
                print("✅ Autenticación ejecutada")
                if isinstance(auth_result.data, dict) and auth_result.data.get("success"):
                    print("✅ Autenticación exitosa")
                    print(f"   Token guardado en: {auth_result.data.get('token_file', 'N/A')}")
                else:
                    print(f"❌ Error en autenticación: {auth_result.data}")
                    return
            except Exception as e:
                print(f"❌ Error en autenticación: {e}")
                return
            
            # Esperar un momento después de la autenticación
            print("⏳ Esperando después de autenticación...")
            await asyncio.sleep(2)
            
            # Validar token
            print("\n🔍 Validando token...")
            try:
                validation_result = await client.call_tool("validate_token", {
                    "company": "rominacostasestetica"
                })
                print("✅ Validación de token ejecutada")
                if isinstance(validation_result.data, dict) and validation_result.data.get("valid"):
                    print("✅ Token válido")
                else:
                    print(f"❌ Token inválido: {validation_result.data}")
            except Exception as e:
                print(f"❌ Error en validación de token: {e}")
            
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
                    if bookings:
                        print("📋 Detalles de las reservas:")
                        for i, booking in enumerate(bookings[:3] if isinstance(bookings, list) else [], 1):
                            print(f"   {i}. ID: {booking.get('id')} - Fecha: {booking.get('start_datetime', 'N/A')}")
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
                        for i, booking in enumerate(bookings[:3] if isinstance(bookings, list) else [], 1):
                            print(f"   {i}. ID: {booking.get('id')} - Fecha: {booking.get('start_datetime', 'N/A')}")
                    else:
                        print("📭 No hay reservas para mañana")
                else:
                    print(f"❌ Error en get_bookings: {result.data}")
            except Exception as e:
                print(f"❌ Error en get_bookings: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n💡 Asegúrate de que:")
        print("   1. El servidor MCP SSE esté ejecutándose en http://localhost:8001/sse/")
        print("   2. Las variables de entorno estén configuradas (SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN, SIMPLYBOOK_PASSWORD)")
        print("   3. El servidor se haya iniciado con: ./start-server-sse.sh")


if __name__ == "__main__":
    asyncio.run(test_authenticated_bookings()) 