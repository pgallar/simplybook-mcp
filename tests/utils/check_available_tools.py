#!/usr/bin/env python3
"""
Script para verificar las herramientas disponibles después de remover la autenticación pública
"""

import asyncio
from fastmcp import Client


async def check_available_tools():
    """Verificar las herramientas disponibles"""
    
    print("🔍 Verificando herramientas disponibles")
    print("=" * 50)
    
    try:
        client = Client("http://localhost:8001/sse")
        
        async with client:
            print("✅ Conectado al servidor MCP SSE")
            
            # Esperar inicialización
            await asyncio.sleep(5)
            
            # Verificar que el servidor responde
            await client.ping()
            print("✅ Servidor SSE responde correctamente")
            
            # Listar herramientas disponibles
            tools = await client.list_tools()
            print(f"📋 Total de herramientas disponibles: {len(tools)}")
            
            # Categorizar herramientas
            auth_tools = []
            booking_tools = []
            service_tools = []
            client_tools = []
            provider_tools = []
            other_tools = []
            
            for tool in tools:
                name = tool.name.lower()
                if 'auth' in name or 'token' in name or 'login' in name:
                    auth_tools.append(tool)
                elif 'book' in name:
                    booking_tools.append(tool)
                elif 'service' in name or 'event' in name:
                    service_tools.append(tool)
                elif 'client' in name:
                    client_tools.append(tool)
                elif 'provider' in name or 'unit' in name:
                    provider_tools.append(tool)
                else:
                    other_tools.append(tool)
            
            # Mostrar herramientas por categoría
            print(f"\n🔐 Herramientas de autenticación: {len(auth_tools)}")
            for tool in auth_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print(f"\n📅 Herramientas de reservas: {len(booking_tools)}")
            for tool in booking_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print(f"\n📋 Herramientas de servicios: {len(service_tools)}")
            for tool in service_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print(f"\n👤 Herramientas de clientes: {len(client_tools)}")
            for tool in client_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print(f"\n🏥 Herramientas de proveedores: {len(provider_tools)}")
            for tool in provider_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            print(f"\n🔧 Otras herramientas: {len(other_tools)}")
            for tool in other_tools:
                print(f"   - {tool.name}: {tool.description}")
            
            # Verificar si la herramienta authenticate está disponible
            authenticate_tool = next((tool for tool in tools if tool.name == "authenticate"), None)
            if authenticate_tool:
                print(f"\n⚠️  ADVERTENCIA: La herramienta 'authenticate' aún está disponible")
                print(f"   Esto significa que la autenticación pública no se removió correctamente")
            else:
                print(f"\n✅ ÉXITO: La herramienta 'authenticate' NO está disponible")
                print(f"   La autenticación pública se removió correctamente")
            
            # Probar una herramienta para verificar que funciona sin autenticación pública
            print(f"\n🧪 Probando herramienta sin autenticación pública...")
            try:
                result = await client.call_tool("get_services_list", {})
                if result.data.get("success"):
                    print("✅ get_services_list funciona correctamente")
                    services = result.data.get("services", [])
                    print(f"   📊 Servicios obtenidos: {len(services)}")
                else:
                    print(f"❌ Error en get_services_list: {result.data}")
            except Exception as e:
                print(f"❌ Excepción en get_services_list: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")


if __name__ == "__main__":
    asyncio.run(check_available_tools()) 