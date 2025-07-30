#!/usr/bin/env python3
"""
Demostración práctica de get_booking_list con filtros avanzados
"""

import asyncio
import json
from datetime import datetime, timedelta
from fastmcp import Client


async def demo_booking_list_filters():
    """Demostración práctica de filtros"""
    
    print("🎯 DEMOSTRACIÓN: get_booking_list con filtros avanzados")
    print("=" * 70)
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado al servidor MCP SSE")
            await asyncio.sleep(5)
            
            # La autenticación es interna y automática
            print("🔐 Autenticación interna automática")
            await asyncio.sleep(2)
            
            # Ejemplo 1: Obtener reservas de mañana confirmadas
            print("\n📅 EJEMPLO 1: Reservas de mañana confirmadas")
            print("-" * 50)
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            
            result = await client.call_tool("get_booking_list", {
                "date": tomorrow_str,
                "status": "confirmed",
                "page": 1,
                "on_page": 10
            })
            
            if result.data.get("success"):
                bookings = result.data.get("result", {}).get("data", [])
                metadata = result.data.get("result", {}).get("metadata", {})
                print(f"✅ Encontradas {len(bookings)} reservas confirmadas para {tomorrow_str}")
                print(f"   Página {metadata.get('page', 'N/A')} de {metadata.get('pages_count', 'N/A')}")
                
                # Mostrar detalles de las primeras 3 reservas
                for i, booking in enumerate(bookings[:3], 1):
                    client_name = booking.get("client", {}).get("name", "N/A")
                    service_name = booking.get("service", {}).get("name", "N/A")
                    start_time = booking.get("start_datetime", "N/A")
                    print(f"   {i}. {client_name} - {service_name} - {start_time}")
            else:
                print(f"❌ Error: {result.data}")
            
            # Ejemplo 2: Buscar reservas de un cliente específico
            print("\n👤 EJEMPLO 2: Buscar reservas de un cliente")
            print("-" * 50)
            
            result = await client.call_tool("get_booking_list", {
                "search": "Pablo Gabriel",
                "upcoming_only": True
            })
            
            if result.data.get("success"):
                bookings = result.data.get("result", {}).get("data", [])
                print(f"✅ Encontradas {len(bookings)} reservas futuras para 'Pablo Gabriel'")
                
                for i, booking in enumerate(bookings[:3], 1):
                    service_name = booking.get("service", {}).get("name", "N/A")
                    start_time = booking.get("start_datetime", "N/A")
                    status = booking.get("status", "N/A")
                    print(f"   {i}. {service_name} - {start_time} - {status}")
            else:
                print(f"❌ Error: {result.data}")
            
            # Ejemplo 3: Reservas por servicio específico
            print("\n🛠️  EJEMPLO 3: Reservas por servicio específico")
            print("-" * 50)
            
            result = await client.call_tool("get_booking_list", {
                "services": ["2"],  # Limpieza facial
                "status": "confirmed",
                "page": 1,
                "on_page": 5
            })
            
            if result.data.get("success"):
                bookings = result.data.get("result", {}).get("data", [])
                print(f"✅ Encontradas {len(bookings)} reservas confirmadas para servicio ID 2")
                
                for i, booking in enumerate(bookings[:3], 1):
                    client_name = booking.get("client", {}).get("name", "N/A")
                    start_time = booking.get("start_datetime", "N/A")
                    print(f"   {i}. {client_name} - {start_time}")
            else:
                print(f"❌ Error: {result.data}")
            
            # Ejemplo 4: Reservas canceladas
            print("\n❌ EJEMPLO 4: Reservas canceladas")
            print("-" * 50)
            
            result = await client.call_tool("get_booking_list", {
                "status": "canceled",
                "page": 1,
                "on_page": 5
            })
            
            if result.data.get("success"):
                bookings = result.data.get("result", {}).get("data", [])
                print(f"✅ Encontradas {len(bookings)} reservas canceladas")
                
                for i, booking in enumerate(bookings[:3], 1):
                    client_name = booking.get("client", {}).get("name", "N/A")
                    service_name = booking.get("service", {}).get("name", "N/A")
                    start_time = booking.get("start_datetime", "N/A")
                    print(f"   {i}. {client_name} - {service_name} - {start_time}")
            else:
                print(f"❌ Error: {result.data}")
            
            # Ejemplo 5: Combinación compleja de filtros
            print("\n🎯 EJEMPLO 5: Combinación compleja de filtros")
            print("-" * 50)
            
            result = await client.call_tool("get_booking_list", {
                "upcoming_only": True,
                "status": "confirmed",
                "providers": ["2"],
                "page": 1,
                "on_page": 3
            })
            
            if result.data.get("success"):
                bookings = result.data.get("result", {}).get("data", [])
                metadata = result.data.get("result", {}).get("metadata", {})
                print(f"✅ Encontradas {len(bookings)} reservas futuras confirmadas del proveedor 2")
                print(f"   Página {metadata.get('page', 'N/A')} de {metadata.get('pages_count', 'N/A')}")
                
                for i, booking in enumerate(bookings, 1):
                    client_name = booking.get("client", {}).get("name", "N/A")
                    service_name = booking.get("service", {}).get("name", "N/A")
                    start_time = booking.get("start_datetime", "N/A")
                    print(f"   {i}. {client_name} - {service_name} - {start_time}")
            else:
                print(f"❌ Error: {result.data}")
            
            # Mostrar información sobre los filtros disponibles
            print("\n📚 FILTROS DISPONIBLES:")
            print("-" * 50)
            print("🔹 page: Número de página para paginación")
            print("🔹 on_page: Elementos por página")
            print("🔹 upcoming_only: Solo reservas futuras (true/false)")
            print("🔹 status: Estado (confirmed/confirmed_pending/pending/canceled)")
            print("🔹 services: Lista de IDs de servicios")
            print("🔹 providers: Lista de IDs de proveedores")
            print("🔹 client_id: ID del cliente")
            print("🔹 date: Fecha específica (YYYY-MM-DD)")
            print("🔹 search: Búsqueda por texto (código, datos del cliente)")
            print("🔹 additional_fields: Campos adicionales (dict)")
            
            print("\n💡 EJEMPLOS DE USO:")
            print("-" * 50)
            print("🔸 Reservas de hoy: date='2025-07-30'")
            print("🔸 Solo futuras: upcoming_only=true")
            print("🔸 Confirmadas: status='confirmed'")
            print("🔸 Por servicio: services=['2', '6']")
            print("🔸 Por proveedor: providers=['2']")
            print("🔸 Por cliente: client_id='3'")
            print("🔸 Búsqueda: search='Pablo'")
            print("🔸 Paginación: page=1, on_page=10")
            
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    asyncio.run(demo_booking_list_filters()) 