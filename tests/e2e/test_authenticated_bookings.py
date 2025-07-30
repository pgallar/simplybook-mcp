#!/usr/bin/env python3
"""
Test de obtención de reservas con autenticación explícita
"""

import asyncio
import os
from datetime import datetime, timedelta
from fastmcp import Client


async def test_authenticated_bookings():
    """Probar obtención de reservas con autenticación explícita"""
    
    print("🔍 Probando obtención de reservas con autenticación explícita")
    print("=" * 60)
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado al servidor MCP SSE")
            
            # Esperar inicialización
            await asyncio.sleep(5)
            
            # Verificar que el servidor responde
            await client.ping()
            print("✅ Servidor SSE responde correctamente")
            
            # Obtener credenciales del .env
            company = os.getenv('SIMPLYBOOK_COMPANY')
            login = os.getenv('SIMPLYBOOK_LOGIN')
            password = os.getenv('SIMPLYBOOK_PASSWORD')
            
            if not all([company, login, password]):
                print("❌ Error: Faltan variables de entorno requeridas")
                print("   Asegúrate de tener configuradas:")
                print("   - SIMPLYBOOK_COMPANY")
                print("   - SIMPLYBOOK_LOGIN")
                print("   - SIMPLYBOOK_PASSWORD")
                return
            
            print("\n🔐 Autenticación interna automática")
            print("✅ Usando credenciales del archivo .env")
            await asyncio.sleep(2)
            
            # Obtener reservas
            print("\n📅 Obteniendo reservas...")
            try:
                result = await client.call_tool("get_bookings_list", {})
                if result.data.get("success"):
                    bookings = result.data.get("bookings", [])
                    print(f"✅ Reservas obtenidas: {len(bookings)}")
                    
                    # Mostrar detalles de las primeras 3 reservas
                    for i, booking in enumerate(bookings[:3], 1):
                        client_name = booking.get("client", {}).get("name", "N/A")
                        service_name = booking.get("service", {}).get("name", "N/A")
                        start_time = booking.get("start_datetime", "N/A")
                        print(f"   {i}. {client_name} - {service_name} - {start_time}")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    asyncio.run(test_authenticated_bookings()) 