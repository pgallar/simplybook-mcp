#!/usr/bin/env python3
"""
Script para probar específicamente endpoints que podrían causar 
el error "Invalid request parameters" según la documentación de SimplyBook.me
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def test_invalid_parameters():
    """Probar endpoints con parámetros que podrían ser inválidos"""
    
    print("🔍 Probando endpoints con parámetros potencialmente inválidos")
    print("=" * 70)
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado al servidor MCP SSE")
            
            # Esperar inicialización
            await asyncio.sleep(5)
            
            # La autenticación ahora es interna y automática
            print("\n🔐 Autenticación interna automática")
            print("✅ Usando credenciales del archivo .env")
            
            # Esperar para que la autenticación interna se complete
            await asyncio.sleep(2)
            
            # Probar get_bookings con parámetros de fecha en formato incorrecto
            print("\n📅 Probando get_bookings con formato de fecha incorrecto...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": "30-07-2025",  # Formato incorrecto
                    "date_to": "30/07/2025"     # Formato incorrecto
                })
                print("✅ get_bookings con formato incorrecto ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con formato incorrecto")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_bookings con parámetros vacíos
            print("\n📅 Probando get_bookings con parámetros vacíos...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": "",
                    "date_to": ""
                })
                print("✅ get_bookings con parámetros vacíos ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con parámetros vacíos")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_bookings con parámetros nulos
            print("\n📅 Probando get_bookings con parámetros nulos...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": None,
                    "date_to": None
                })
                print("✅ get_bookings con parámetros nulos ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con parámetros nulos")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_available_slots con service_id inválido
            print("\n⏰ Probando get_available_slots con service_id inválido...")
            try:
                result = await client.call_tool("get_available_slots", {
                    "service_id": "999999",  # ID que no existe
                    "date": "2025-07-30"
                })
                print("✅ get_available_slots con service_id inválido ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con service_id inválido")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_available_slots con fecha inválida
            print("\n⏰ Probando get_available_slots con fecha inválida...")
            try:
                result = await client.call_tool("get_available_slots", {
                    "service_id": "2",
                    "date": "2025-13-45"  # Fecha inválida
                })
                print("✅ get_available_slots con fecha inválida ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con fecha inválida")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_calendar_data con fechas inválidas
            print("\n📅 Probando get_calendar_data con fechas inválidas...")
            try:
                result = await client.call_tool("get_calendar_data", {
                    "start_date": "2025-07-30",
                    "end_date": "2025-07-29"  # end_date antes que start_date
                })
                print("✅ get_calendar_data con fechas inválidas ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con fechas inválidas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_bookings con parámetros adicionales no documentados
            print("\n📅 Probando get_bookings con parámetros no documentados...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": "2025-07-30",
                    "date_to": "2025-07-30",
                    "invalid_param": "test",  # Parámetro no documentado
                    "another_invalid": 123
                })
                print("✅ get_bookings con parámetros no documentados ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con parámetros no documentados")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # Probar get_bookings con tipos de datos incorrectos
            print("\n📅 Probando get_bookings con tipos de datos incorrectos...")
            try:
                result = await client.call_tool("get_bookings", {
                    "date_from": 12345,  # Número en lugar de string
                    "date_to": ["2025", "07", "30"]  # Lista en lugar de string
                })
                print("✅ get_bookings con tipos incorrectos ejecutado")
                if isinstance(result.data, dict) and result.data.get("success"):
                    print("✅ Funcionó con tipos incorrectos")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    asyncio.run(test_invalid_parameters()) 