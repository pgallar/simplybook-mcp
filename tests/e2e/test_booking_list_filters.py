#!/usr/bin/env python3
"""
Script para probar la nueva funcionalidad get_booking_list con filtros avanzados
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def test_booking_list_filters():
    """Probar get_booking_list con diferentes filtros"""
    
    print("🔍 Probando get_booking_list con filtros avanzados")
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
            
            # La autenticación es interna y automática
            print("\n🔐 Autenticación interna automática")
            print("✅ Usando credenciales del archivo .env")
            await asyncio.sleep(2)
            
            # 1. Probar sin filtros (todos los parámetros None)
            print("\n📋 1. Probando sin filtros...")
            try:
                result = await client.call_tool("get_booking_list", {})
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    metadata = result.data.get("result", {}).get("metadata", {})
                    print(f"✅ Sin filtros: {len(bookings)} reservas")
                    print(f"   Página: {metadata.get('page', 'N/A')}")
                    print(f"   Total: {metadata.get('items_count', 'N/A')}")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 2. Probar con paginación
            print("\n📄 2. Probando con paginación...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "page": 1,
                    "on_page": 5
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    metadata = result.data.get("result", {}).get("metadata", {})
                    print(f"✅ Paginación: {len(bookings)} reservas en página {metadata.get('page', 'N/A')}")
                    print(f"   Elementos por página: {metadata.get('on_page', 'N/A')}")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 3. Probar solo reservas futuras
            print("\n🔮 3. Probando solo reservas futuras...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "upcoming_only": True
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Solo futuras: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 4. Probar por estado
            print("\n📊 4. Probando por estado...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "status": "confirmed"
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Estado 'confirmed': {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 5. Probar por servicios
            print("\n🛠️  5. Probando por servicios...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "services": ["2", "6"]  # IDs de servicios
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Por servicios [2, 6]: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 6. Probar por proveedores
            print("\n👥 6. Probando por proveedores...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "providers": ["2"]  # ID del proveedor
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Por proveedor [2]: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 7. Probar por cliente
            print("\n👤 7. Probando por cliente...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "client_id": "3"  # ID del cliente
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Por cliente [3]: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 8. Probar por fecha
            print("\n📅 8. Probando por fecha...")
            try:
                tomorrow = datetime.now() + timedelta(days=1)
                tomorrow_str = tomorrow.strftime("%Y-%m-%d")
                result = await client.call_tool("get_booking_list", {
                    "date": tomorrow_str
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Por fecha {tomorrow_str}: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 9. Probar búsqueda por texto
            print("\n🔍 9. Probando búsqueda por texto...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "search": "Pablo"  # Buscar por nombre del cliente
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Búsqueda 'Pablo': {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 10. Probar combinación de filtros
            print("\n🎯 10. Probando combinación de filtros...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "upcoming_only": True,
                    "status": "confirmed",
                    "page": 1,
                    "on_page": 3
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    metadata = result.data.get("result", {}).get("metadata", {})
                    print(f"✅ Combinación de filtros: {len(bookings)} reservas")
                    print(f"   Futuras + confirmadas + paginación")
                    print(f"   Página: {metadata.get('page', 'N/A')}")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
            # 11. Probar campos adicionales
            print("\n🔧 11. Probando campos adicionales...")
            try:
                result = await client.call_tool("get_booking_list", {
                    "additional_fields": {
                        "field1": "value1",
                        "field2": "value2"
                    }
                })
                if result.data.get("success"):
                    bookings = result.data.get("result", {}).get("data", [])
                    print(f"✅ Campos adicionales: {len(bookings)} reservas")
                else:
                    print(f"❌ Error: {result.data}")
            except Exception as e:
                print(f"❌ Excepción: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    asyncio.run(test_booking_list_filters()) 