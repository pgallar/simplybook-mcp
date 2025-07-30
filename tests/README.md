# Tests del Servidor MCP SimplyBook

Esta carpeta contiene todos los tests organizados por categorías para el servidor MCP de SimplyBook.

## 📁 Estructura de Tests

```
tests/
├── unit/           # Tests unitarios
├── integration/    # Tests de integración
├── e2e/           # Tests end-to-end
├── utils/         # Scripts de utilidad y verificación
└── README.md      # Este archivo
```

## 🧪 Tests Unitarios (`unit/`)

Tests que verifican componentes individuales del sistema de forma aislada.

### Archivos:
- `test_auth_client.py` - Tests del cliente de autenticación
- `test_auth_routes.py` - Tests de las rutas de autenticación
- `test_services_client.py` - Tests del cliente de servicios
- `test_services_routes.py` - Tests de las rutas de servicios

### Ejecución:
```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/

# Ejecutar tests específicos
pytest tests/unit/test_auth_client.py
pytest tests/unit/test_services_routes.py
```

## 🔗 Tests de Integración (`integration/`)

Tests que verifican la interacción entre múltiples componentes.

### Archivos:
- `test_integration.py` - Tests de integración general

### Ejecución:
```bash
# Ejecutar tests de integración
pytest tests/integration/
```

## 🌐 Tests End-to-End (`e2e/`)

Tests que verifican el flujo completo del sistema, incluyendo la API externa de SimplyBook.

### Archivos:
- `test_api_endpoints.py` - Tests de todos los endpoints de la API
- `test_booking_list_filters.py` - Tests de filtros avanzados de reservas
- `test_authenticated_bookings.py` - Tests de autenticación y reservas
- `test_tomorrow_bookings.py` - Tests de reservas de mañana
- `test_sse_client.py` - Tests del cliente SSE
- `test_double_auth.py` - Tests de autenticación múltiple
- `test_403_error.py` - Tests de manejo de errores 403
- `test_bookings_client.py` - Tests del cliente de bookings
- `test_invalid_parameters.py` - Tests de parámetros inválidos
- `test_logging_control.py` - Tests de control de logging

### Ejecución:
```bash
# Ejecutar todos los tests e2e
pytest tests/e2e/

# Ejecutar tests específicos
python3 tests/e2e/test_api_endpoints.py
python3 tests/e2e/test_booking_list_filters.py
```

## 🛠️ Scripts de Utilidad (`utils/`)

Scripts para verificar el estado del sistema y debugging.

### Archivos:
- `check_available_tools.py` - Verificar herramientas disponibles en el servidor MCP
- `check_api_logs.py` - Analizar logs de la API
- `check_server_status.py` - Verificar estado del servidor
- `quick_test_bookings.py` - Test rápido de reservas

### Ejecución:
```bash
# Verificar estado del servidor
python3 tests/utils/check_server_status.py

# Ver herramientas disponibles
python3 tests/utils/check_available_tools.py

# Analizar logs
python3 tests/utils/check_api_logs.py

# Test rápido
python3 tests/utils/quick_test_bookings.py
```

## 🚀 Ejecución Completa

### Prerequisitos
1. Servidor MCP ejecutándose en Docker
2. Variables de entorno configuradas en `.env`
3. Python 3.11+ con dependencias instaladas

### Ejecutar Todos los Tests
```bash
# Tests unitarios
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests e2e (requieren servidor ejecutándose)
python3 tests/e2e/test_api_endpoints.py
python3 tests/e2e/test_booking_list_filters.py

# Verificar estado
python3 tests/utils/check_server_status.py
```

### Scripts de Automatización
```bash
# Ejecutar tests unitarios e integración
./run_tests.sh

# Ejecutar tests de integración completos
./run_integration_tests.sh
```

## 📊 Categorías de Tests

### 🔐 Autenticación
- `tests/unit/test_auth_client.py`
- `tests/unit/test_auth_routes.py`
- `tests/e2e/test_authenticated_bookings.py`
- `tests/e2e/test_double_auth.py`
- `tests/e2e/test_403_error.py`

### 📅 Reservas
- `tests/e2e/test_booking_list_filters.py`
- `tests/e2e/test_bookings_client.py`
- `tests/e2e/test_tomorrow_bookings.py`
- `tests/utils/quick_test_bookings.py`

### 🔧 API y Endpoints
- `tests/e2e/test_api_endpoints.py`
- `tests/e2e/test_invalid_parameters.py`
- `tests/e2e/test_sse_client.py`

### 📝 Logging y Monitoreo
- `tests/e2e/test_logging_control.py`
- `tests/utils/check_api_logs.py`
- `tests/utils/check_server_status.py`

### 🛠️ Servicios
- `tests/unit/test_services_client.py`
- `tests/unit/test_services_routes.py`

### 🔗 Integración
- `tests/integration/test_integration.py`

## 📝 Notas Importantes

1. **Tests Unitarios**: No requieren servidor ejecutándose
2. **Tests E2E**: Requieren servidor MCP ejecutándose en Docker
3. **Autenticación**: Los tests e2e usan autenticación interna automática
4. **Logging**: El logging de API se puede controlar via `ENABLE_API_LOGGING`
5. **SSE**: Los tests usan el endpoint SSE (`http://localhost:8001/sse`)

## 🔧 Troubleshooting

### Error de Conexión en Tests E2E
```bash
# Verificar que el servidor esté ejecutándose
python3 tests/utils/check_server_status.py

# Reiniciar el servidor si es necesario
docker compose down && docker compose up --build -d
```

### Error de Autenticación
```bash
# Verificar variables de entorno
cat .env

# Probar autenticación manual
python3 tests/e2e/test_authenticated_bookings.py
```

### Error en Tests Unitarios
```bash
# Verificar dependencias
pip install -r requirements.txt

# Ejecutar con verbose
pytest tests/unit/ -v
```

## 📚 Documentación Relacionada

- **Demos**: Ver carpeta `demos/` para ejemplos de uso
- **Configuración**: Ver `README.md` principal para configuración del servidor
- **Docker**: Ver `DOCKER_SETUP.md` para configuración de Docker 