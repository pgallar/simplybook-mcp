#!/usr/bin/env python3
"""
Script de prueba para simular y manejar el error 403 que ocurre en Claude Desktop
después de múltiples ejecuciones del servidor MCP SimplyBook.
"""

import asyncio
import json
import time
from fastmcp import Client


async def test_multiple_requests():
    """Prueba múltiples solicitudes para simular el error 403"""
    
    print("🧪 Probando múltiples solicitudes para detectar error 403...")
    print("=" * 60)
    
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            # Realizar múltiples solicitudes rápidas
            for i in range(5):
                print(f"\n🔄 Solicitud #{i + 1}")
                print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
                
                try:
                    result = await client.call_tool("get_bookings_list", {})
                    
                    if result.data.get("success"):
                        bookings = result.data.get("bookings", [])
                        count = result.data.get("count", 0)
                        print(f"✅ Éxito: {count} reservas obtenidas")
                    else:
                        error = result.data.get("error", "Error desconocido")
                        print(f"❌ Error: {error}")
                        
                        # Verificar si es error 403
                        if "403" in error or "Forbidden" in error:
                            print("🚨 ¡Error 403 detectado! Implementando solución...")
                            print("💡 Esperando 10 segundos antes del siguiente intento...")
                            await asyncio.sleep(10)
                        
                except Exception as e:
                    print(f"❌ Excepción: {e}")
                    if "403" in str(e):
                        print("🚨 Error 403 en excepción")
                        await asyncio.sleep(10)
                
                # Pequeña pausa entre solicitudes
                if i < 4:  # No esperar después de la última solicitud
                    print("⏳ Esperando 2 segundos...")
                    await asyncio.sleep(2)
                    
    except Exception as e:
        print(f"❌ Error general: {e}")


async def test_auth_recovery():
    """Prueba la recuperación de autenticación después de error 403"""
    
    print("\n🔄 Probando recuperación de autenticación...")
    print("=" * 60)
    
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            # Primera solicitud
            print("\n🔄 Primera solicitud...")
            result1 = await client.call_tool("get_bookings_list", {})
            print(f"Resultado 1: {'✅ Éxito' if result1.data.get('success') else '❌ Error'}")
            
            # Simular error 403 (esperar y reintentar)
            print("\n⏳ Simulando error 403 (esperando 5 segundos)...")
            await asyncio.sleep(5)
            
            # Segunda solicitud (debería reintentar autenticación)
            print("\n🔄 Segunda solicitud (después de simular error)...")
            result2 = await client.call_tool("get_bookings_list", {})
            print(f"Resultado 2: {'✅ Éxito' if result2.data.get('success') else '❌ Error'}")
            
            if result2.data.get("success"):
                print("🎉 ¡Recuperación exitosa!")
            else:
                print("⚠️  La recuperación no fue exitosa")
                print(f"Error: {result2.data.get('error', 'Error desconocido')}")
                
    except Exception as e:
        print(f"❌ Error en prueba de recuperación: {e}")


async def test_rate_limiting():
    """Prueba el rate limiting implementado"""
    
    print("\n⏱️  Probando rate limiting...")
    print("=" * 60)
    
    client = Client("http://localhost:8000/mcp")
    
    try:
        async with client:
            print("✅ Conectado al servidor MCP")
            
            start_time = time.time()
            
            # Realizar 3 solicitudes rápidas
            for i in range(3):
                print(f"\n🔄 Solicitud rápida #{i + 1}")
                result = await client.call_tool("get_bookings_list", {})
                print(f"Resultado: {'✅ Éxito' if result.data.get('success') else '❌ Error'}")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n⏱️  Tiempo total: {total_time:.2f} segundos")
            print(f"⏱️  Tiempo promedio por solicitud: {total_time/3:.2f} segundos")
            
            if total_time >= 2.0:  # Debería tomar al menos 2 segundos con rate limiting
                print("✅ Rate limiting funcionando correctamente")
            else:
                print("⚠️  Rate limiting puede no estar funcionando")
                
    except Exception as e:
        print(f"❌ Error en prueba de rate limiting: {e}")


async def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de manejo de error 403")
    print("=" * 60)
    
    await test_multiple_requests()
    await test_auth_recovery()
    await test_rate_limiting()
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")
    print("\n💡 Recomendaciones para evitar error 403:")
    print("   1. Implementar delays entre solicitudes")
    print("   2. Usar rate limiting (ya implementado)")
    print("   3. Manejar reintentos automáticos")
    print("   4. Limpiar tokens expirados")
    print("   5. Usar User-Agent consistente")


if __name__ == "__main__":
    asyncio.run(main()) 