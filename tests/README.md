# Tests para SimplyBook MCP Server

Este directorio contiene todos los tests unitarios y de integración para el servidor MCP de SimplyBook.

## Estructura de Tests

```
tests/
├── __init__.py                    # Inicializador del paquete
├── test_auth_client.py           # Tests del cliente de autenticación
├── test_services_client.py       # Tests del cliente de servicios
├── test_auth_routes.py           # Tests de las rutas de autenticación
├── test_services_routes.py       # Tests de las rutas de servicios
├── test_integration.py           # Tests de integración con API real
└── README.md                     # Esta documentación
```

## Tipos de Tests

### 1. Tests Unitarios
- **`test_auth_client.py`**: Prueba todas las funciones del cliente de autenticación
- **`test_services_client.py`**: Prueba todas las funciones del cliente de servicios
- **`test_auth_routes.py`**: Prueba las herramientas MCP de autenticación
- **`test_services_routes.py`**: Prueba las herramientas MCP de servicios

### 2. Tests de Integración
- **`test_integration.py`**: Prueba la conexión real con la API de SimplyBook.me

## Ejecutar Tests

### Tests Unitarios
```bash
# Ejecutar todos los tests unitarios
./run_tests.sh

# O ejecutar directamente con pytest
pytest tests/ -v --tb=short --asyncio-mode=auto
```

### Tests de Integración
```bash
# Ejecutar tests de integración (requiere credenciales reales)
./run_integration_tests.sh

# O ejecutar directamente
pytest tests/test_integration.py -v --tb=short --asyncio-mode=auto
```

### Tests Específicos
```bash
# Ejecutar solo tests de autenticación
pytest tests/test_auth_client.py -v

# Ejecutar solo tests de servicios
pytest tests/test_services_client.py -v

# Ejecutar un test específico
pytest tests/test_auth_client.py::TestAuthClient::test_authenticate_success -v
```

## Configuración

### Variables de Entorno para Tests de Integración
Los tests de integración requieren credenciales reales de SimplyBook.me:

```bash
SIMPLYBOOK_COMPANY=tu_company_login
SIMPLYBOOK_LOGIN=tu_user_login
SIMPLYBOOK_PASSWORD=tu_password
```

Estas variables se cargan automáticamente desde el archivo `.env` cuando ejecutas `./run_integration_tests.sh`.

## Problemas Identificados y Solucionados

### 1. Error 403 en Autenticación
**Problema**: `{"success":false,"message":"Error HTTP: 403"}`
**Causa**: URL o endpoint incorrecto para autenticación
**Solución**: Actualizado a usar `https://user-api-v2.simplybook.me/admin/auth`

### 2. Error 404 en get_bookings
**Problema**: `Client error '404 Not Found' for url '.../getBookings'`
**Causa**: Endpoint incorrecto
**Solución**: Cambiado a `/getBookingList`

### 3. Error en get_bookings_list
**Problema**: `'BookingsClient' object has no attribute 'get_bookings_list'`
**Causa**: Método faltante en BookingsClient
**Solución**: Agregado método `get_bookings_list()`

### 4. Error en get_calendar_data
**Problema**: `No se pudo autenticar`
**Causa**: Método faltante en BookingsClient
**Solución**: Agregado método `get_calendar_data()`

### 5. Error en validate_token
**Problema**: `Token inválido: 404`
**Causa**: Endpoint de validación incorrecto
**Solución**: Actualizado endpoint de validación

## Cobertura de Tests

Los tests cubren:

- ✅ Autenticación (éxito y fallo)
- ✅ Validación de tokens
- ✅ Gestión de tokens (guardar, cargar, eliminar)
- ✅ Obtención de servicios
- ✅ Obtención de performers
- ✅ Obtención de reservas
- ✅ Creación de reservas
- ✅ Cancelación de reservas
- ✅ Manejo de errores HTTP
- ✅ Manejo de excepciones

## Debugging

### Ver Logs Detallados
```bash
# Ejecutar con logs detallados
pytest tests/ -v -s --tb=long

# Ejecutar un test específico con logs
pytest tests/test_integration.py::TestIntegration::test_real_authentication -v -s
```

### Verificar Configuración
```bash
# Verificar que las credenciales estén configuradas
cat .env

# Verificar que pytest esté instalado
pytest --version
```

## Contribuir

Al agregar nuevas funcionalidades:

1. **Crear tests unitarios** para las nuevas funciones
2. **Crear tests de integración** si es necesario
3. **Actualizar esta documentación** con los nuevos tests
4. **Ejecutar todos los tests** antes de hacer commit

```bash
# Ejecutar todos los tests antes de commit
./run_tests.sh
./run_integration_tests.sh
``` 