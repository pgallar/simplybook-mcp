#!/usr/bin/env python3
"""
Script para probar la autenticación 2 veces seguidas con SimplyBook
"""

import asyncio
import json
import time
from fastmcp import Client


async def test_double_authentication():
    """Prueba la autenticación 2 veces seguidas"""
    
    print("🔐 Probando autenticación doble con SimplyBook")
    print("=" * 60)
    
    # Datos de autenticación
    auth_data = {
        "company": "rominacostasestetica",
        "login": "roalecos@gmail.com", 
        "password": "!Quitucho1712"
    }
    
    print(f"🏢 Company: {auth_data['company']}")
    print(f"👤 Login: {auth_data['login']}")
    print(f"🔑 Password: {'*' * len(auth_data['password'])}")
    print()
    
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            # Primera autenticación
            print("\n🔄 PRIMERA AUTENTICACIÓN")
            print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
            
            try:
                result1 = await client.call_tool("get_bookings_list", {})
                
                if result1.data.get("success"):
                    bookings = result1.data.get("bookings", [])
                    count = result1.data.get("count", 0)
                    print(f"✅ Éxito: {count} reservas obtenidas")
                    print(f"📊 Total de reservas en sistema: {len(bookings)}")
                else:
                    error = result1.data.get("error", "Error desconocido")
                    print(f"❌ Error: {error}")
                    
                    # Verificar si es error 403
                    if "403" in error or "Forbidden" in error:
                        print("🚨 Error 403 detectado en primera autenticación")
                    
            except Exception as e:
                print(f"❌ Excepción en primera autenticación: {e}")
            
            # Esperar 3 segundos entre autenticaciones
            print("\n⏳ Esperando 3 segundos entre autenticaciones...")
            await asyncio.sleep(3)
            
            # Segunda autenticación
            print("\n🔄 SEGUNDA AUTENTICACIÓN")
            print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
            
            try:
                result2 = await client.call_tool("get_bookings_list", {})
                
                if result2.data.get("success"):
                    bookings = result2.data.get("bookings", [])
                    count = result2.data.get("count", 0)
                    print(f"✅ Éxito: {count} reservas obtenidas")
                    print(f"📊 Total de reservas en sistema: {len(bookings)}")
                else:
                    error = result2.data.get("error", "Error desconocido")
                    print(f"❌ Error: {error}")
                    
                    # Verificar si es error 403
                    if "403" in error or "Forbidden" in error:
                        print("🚨 Error 403 detectado en segunda autenticación")
                    
            except Exception as e:
                print(f"❌ Excepción en segunda autenticación: {e}")
            
            # Comparar resultados
            print("\n📊 COMPARACIÓN DE RESULTADOS")
            print("=" * 40)
            
            success1 = result1.data.get("success") if 'result1' in locals() else False
            success2 = result2.data.get("success") if 'result2' in locals() else False
            
            print(f"Primera autenticación: {'✅ Éxito' if success1 else '❌ Fallo'}")
            print(f"Segunda autenticación: {'✅ Éxito' if success2 else '❌ Fallo'}")
            
            if success1 and success2:
                print("🎉 ¡Ambas autenticaciones exitosas!")
            elif success1 and not success2:
                print("⚠️  Primera exitosa, segunda falló (posible rate limiting)")
            elif not success1 and success2:
                print("⚠️  Primera falló, segunda exitosa (recuperación automática)")
            else:
                print("❌ Ambas autenticaciones fallaron")
                
    except Exception as e:
        print(f"❌ Error general: {e}")
        print(f"   Tipo de error: {type(e).__name__}")


async def test_rapid_authentication():
    """Prueba autenticación rápida sin delays"""
    
    print("\n⚡ Probando autenticación rápida (sin delays)")
    print("=" * 60)
    
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            # Múltiples solicitudes rápidas
            for i in range(3):
                print(f"\n🔄 Solicitud rápida #{i + 1}")
                print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
                
                try:
                    result = await client.call_tool("get_bookings_list", {})
                    
                    if result.data.get("success"):
                        count = result.data.get("count", 0)
                        print(f"✅ Éxito: {count} reservas")
                    else:
                        error = result.data.get("error", "Error desconocido")
                        print(f"❌ Error: {error}")
                        
                        if "403" in error:
                            print("🚨 Error 403 - Rate limiting activo")
                        
                except Exception as e:
                    print(f"❌ Excepción: {e}")
                
                # Sin delay entre solicitudes
                
    except Exception as e:
        print(f"❌ Error en prueba rápida: {e}")


async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de autenticación doble")
    print("=" * 60)
    
    await test_double_authentication()
    await test_rapid_authentication()
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")
    print("\n💡 Observaciones:")
    print("   - Si la segunda autenticación falla, es normal (rate limiting)")
    print("   - El sistema debería manejar reintentos automáticamente")
    print("   - Los delays ayudan a evitar errores 403")


if __name__ == "__main__":
    asyncio.run(main()) 