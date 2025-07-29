# Configuración de Claude Desktop con SimplyBook MCP

Esta guía te ayudará a configurar Claude Desktop para usar el servidor MCP de SimplyBook.

## Requisitos Previos

1. **Claude Desktop** instalado en tu sistema
2. **API Key de SimplyBook.me**
3. **Python 3.11+** instalado
4. **Dependencias del proyecto** instaladas

## Configuración Automática (Recomendada)

### Paso 1: Ejecutar el script de configuración

```bash
# Navega al directorio del proyecto
cd /ruta/a/simplybook-mcp

# Ejecuta el script de configuración
./setup-claude-desktop.sh
```

El script te pedirá tu API Key de SimplyBook y creará automáticamente los archivos de configuración.

### Paso 2: Configurar Claude Desktop

1. Abre **Claude Desktop**
2. Ve a **Settings** (Configuración)
3. Busca la sección **MCP Servers**
4. Copia el contenido de uno de los archivos generados:
   - `claude-desktop-config.json` (para configuración stdio)
   - `claude-desktop-config-http.json` (para configuración HTTP)
5. Pega la configuración en el campo correspondiente
6. Reinicia Claude Desktop

## Configuración Manual

Si prefieres configurar manualmente, usa una de estas configuraciones:

### Configuración con stdio (Recomendada)

```json
{
  "mcpServers": {
    "simplybook": {
      "command": "python3",
      "args": ["src/main.py"],
      "env": {
        "SIMPLYBOOK_API_KEY": "tu_api_key_aqui",
        "PYTHONPATH": "/ruta/completa/a/simplybook-mcp/src"
      },
      "cwd": "/ruta/completa/a/simplybook-mcp"
    }
  }
}
```

### Configuración con HTTP

```json
{
  "mcpServers": {
    "simplybook": {
      "command": "python3",
      "args": ["src/main.py"],
      "env": {
        "SIMPLYBOOK_API_KEY": "tu_api_key_aqui",
        "PYTHONPATH": "/ruta/completa/a/simplybook-mcp/src"
      },
      "cwd": "/ruta/completa/a/simplybook-mcp",
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/"
      }
    }
  }
}
```

## Verificación

Una vez configurado, puedes verificar que todo funciona correctamente:

1. **Reinicia Claude Desktop**
2. **Abre una nueva conversación**
3. **Prueba un comando simple** como:
   ```
   @simplybook get_subscription_info
   ```

## Herramientas Disponibles

El servidor MCP proporciona las siguientes herramientas:

### Autenticación
- `authenticate(username, password)` - Autenticar usuario
- `second_factor_auth(token, code)` - Autenticación de segundo factor
- `get_sms_code(token)` - Obtener código SMS
- `refresh_token(refresh_token)` - Refrescar token
- `logout(token)` - Cerrar sesión

### Clientes
- `get_clients_list()` - Obtener lista de clientes
- `get_client(client_id)` - Obtener cliente específico
- `create_client(client_data)` - Crear cliente
- `edit_client(client_id, client_data)` - Editar cliente
- `delete_client(client_id)` - Eliminar cliente

### Servicios
- `get_services_list()` - Obtener lista de servicios
- `get_service(service_id)` - Obtener servicio específico
- `create_service(service_data)` - Crear servicio
- `update_service(service_id, service_data)` - Actualizar servicio
- `delete_service(service_id)` - Eliminar servicio

### Reservas
- `get_bookings_list()` - Obtener lista de reservas
- `create_booking(booking_data)` - Crear reserva
- `edit_booking(booking_id, booking_data)` - Editar reserva
- `get_booking_details(booking_id)` - Obtener detalles de reserva
- `cancel_booking(booking_id)` - Cancelar reserva
- `approve_booking(booking_id)` - Aprobar reserva

### Y muchas más...

## Solución de Problemas

### Error: "Command not found"
- Asegúrate de que Python 3 esté instalado y en el PATH
- Verifica que la ruta en `cwd` sea correcta

### Error: "Module not found"
- Verifica que `PYTHONPATH` apunte al directorio `src`
- Asegúrate de que todas las dependencias estén instaladas

### Error: "API Key not found"
- Verifica que la variable `SIMPLYBOOK_API_KEY` esté configurada correctamente
- Asegúrate de que el API Key sea válido

### Error: "Connection refused"
- Si usas configuración HTTP, asegúrate de que el puerto 8000 esté disponible
- Verifica que no haya otro proceso usando el mismo puerto

## Soporte

Si encuentras problemas, puedes:

1. Revisar los logs en `simplybook_mcp.log`
2. Verificar que todas las dependencias estén instaladas
3. Probar la configuración con el script automático
4. Abrir un issue en el repositorio del proyecto 