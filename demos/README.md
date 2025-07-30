# Demos del Servidor MCP SimplyBook

Esta carpeta contiene scripts de demostración que muestran cómo usar las funcionalidades del servidor MCP de SimplyBook.

## 📁 Archivos de Demo

### `demo_booking_list_filters.py`
- **Propósito**: Demostrar la funcionalidad `get_booking_list` con filtros avanzados
- **Uso**: `python3 demo_booking_list_filters.py`
- **Funcionalidad**: 
  - Ejemplos prácticos de uso de todos los filtros disponibles
  - Muestra cómo combinar múltiples filtros
  - Incluye ejemplos de paginación
  - Demuestra búsqueda por texto y fecha

### `demo_logging_control.py`
- **Propósito**: Archivo placeholder para futuras demos de control de logging
- **Estado**: Vacío (placeholder para futuras funcionalidades)

## 🚀 Cómo Ejecutar

### Prerequisitos
1. Servidor MCP ejecutándose en Docker
2. Variables de entorno configuradas en `.env`
3. Python 3.11+ con dependencias instaladas

### Ejecución Básica
```bash
# Navegar a la carpeta de demos
cd demos

# Ejecutar demo de filtros avanzados
python3 demo_booking_list_filters.py
```

### Ejecución desde el Directorio Raíz
```bash
# Desde el directorio raíz del proyecto
python3 demos/demo_booking_list_filters.py
```

## 📊 Ejemplos Incluidos en el Demo

### 1. Reservas de Mañana Confirmadas
```python
result = await client.call_tool("get_booking_list", {
    "date": "2025-07-31",
    "status": "confirmed",
    "page": 1,
    "on_page": 10
})
```

### 2. Búsqueda de Cliente Específico
```python
result = await client.call_tool("get_booking_list", {
    "search": "Pablo Gabriel",
    "upcoming_only": True
})
```

### 3. Reservas por Servicio
```python
result = await client.call_tool("get_booking_list", {
    "services": ["2"],
    "status": "confirmed",
    "page": 1,
    "on_page": 5
})
```

### 4. Combinación Compleja de Filtros
```python
result = await client.call_tool("get_booking_list", {
    "upcoming_only": True,
    "status": "confirmed",
    "providers": ["2"],
    "page": 1,
    "on_page": 3
})
```

## 📚 Filtros Disponibles

El demo muestra todos los filtros disponibles:

- **Paginación**: `page`, `on_page`
- **Tiempo**: `upcoming_only`, `date`
- **Estado**: `status` (confirmed/confirmed_pending/pending/canceled)
- **Entidades**: `services`, `providers`, `client_id`
- **Búsqueda**: `search`, `additional_fields`

## 🔧 Troubleshooting

### Error de Conexión
```bash
# Verificar que el servidor esté ejecutándose
python3 ../tests/utils/check_server_status.py
```

### Error de Autenticación
```bash
# Verificar variables de entorno
cat ../.env

# Probar autenticación manual
python3 ../tests/e2e/test_authenticated_bookings.py
```

### Error de Filtros
```bash
# Verificar herramientas disponibles
python3 ../tests/utils/check_available_tools.py
```

## 📝 Notas Importantes

1. **Autenticación Interna**: Los demos usan autenticación interna automática
2. **Logging**: El logging de API se puede controlar via `ENABLE_API_LOGGING`
3. **SSE**: Los demos usan el endpoint SSE (`http://localhost:8001/sse`)
4. **Datos Reales**: Los demos usan datos reales de la API de SimplyBook

## 🔗 Enlaces Relacionados

- **Tests**: Ver carpeta `tests/` para tests completos
- **Configuración**: Ver `README.md` principal para configuración del servidor
- **API**: Ver documentación de SimplyBook.me para más detalles de filtros 