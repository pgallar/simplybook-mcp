# FastMCP SimplyBook Server

Este proyecto es un servidor FastMCP que se comunica con la API REST de SimplyBook.me. Proporciona una forma estructurada de interactuar con la API de SimplyBook, permitiendo una fácil integración y gestión de reservas y servicios.

## Configuración

### Variables de Entorno

El servidor requiere las siguientes variables de entorno según la [documentación de SimplyBook.me](https://simplybook.me/en/api/developer-api/tab/rest_api):

- `SIMPLYBOOK_COMPANY`: Tu company login
- `SIMPLYBOOK_LOGIN`: Tu user login
- `SIMPLYBOOK_PASSWORD`: Tu password

## Opciones de Ejecución

### Opción 1: Docker Compose (Recomendada)

#### Configuración Automática

1. **Ejecuta el script de configuración:**
   ```bash
   ./setup-docker-claude.sh
   ```

2. **Inicia el servidor MCP:**
   ```bash
   docker compose up --build
   ```

3. **Configura Claude Desktop:**
   - Copia el contenido de `claude-desktop-config-docker.json`
   - Ve a Claude Desktop > Settings > MCP Servers
   - Pega la configuración y reinicia

#### Configuración Manual

1. **Crea archivo .env:**
   ```bash
   echo "SIMPLYBOOK_COMPANY=tu_company_login" > .env
   echo "SIMPLYBOOK_LOGIN=tu_user_login" >> .env
   echo "SIMPLYBOOK_PASSWORD=tu_password" >> .env
   ```

2. **Inicia Docker Compose:**
   ```bash
   docker compose up --build
   ```

3. **Configura Claude Desktop con:**
   ```json
   {
     "mcpServers": {
       "simplybook": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "http://localhost:8000/mcp/"
         ]
       }
     }
   }
   ```

### Opción 2: Ejecución Local

1. **Clona el repositorio:**
   ```
   git clone <repository-url>
   cd simplybook-mcp
   ```

2. **Configura las variables de entorno:**
   ```bash
   export SIMPLYBOOK_COMPANY=tu_company_login
   export SIMPLYBOOK_LOGIN=tu_user_login
   export SIMPLYBOOK_PASSWORD=tu_password
   ```

3. **Instala las dependencias:**
   ```
   pip install -r requirements.txt
   ```

4. **Ejecuta el servidor:**
   ```
   python src/main.py
   ```

## Estructura del Proyecto

```
simplybook-mcp/
├── src/                                # Código fuente
│   ├── main.py                         # Punto de entrada del servidor FastMCP
│   └── simplybook/                     # Módulos de SimplyBook
├── tests/                              # Tests organizados por categorías
│   ├── unit/                           # Tests unitarios
│   ├── integration/                    # Tests de integración
│   ├── e2e/                           # Tests end-to-end
│   ├── utils/                         # Scripts de utilidad y verificación
│   └── README.md                      # Documentación de tests
├── demos/                              # Scripts de demostración
│   ├── demo_booking_list_filters.py   # Demo de filtros avanzados
│   └── README.md                      # Documentación de demos
├── logs/                               # Logs del sistema
├── docker-compose.yml                  # Configuración de Docker Compose
├── Dockerfile                          # Imagen de Docker
├── requirements.txt                    # Dependencias del proyecto
├── claude-desktop-config-docker.json  # Configuración para Claude Desktop
├── setup-docker-claude.sh             # Script de configuración automática
└── README.md                           # Documentación del proyecto
```

## Uso

Una vez que el servidor esté ejecutándose, puedes acceder a los endpoints definidos para interactuar con la API de SimplyBook. El sistema implementa la autenticación según la [documentación oficial de SimplyBook.me](https://simplybook.me/en/api/developer-api/tab/rest_api).

### Comandos de Prueba

```
@simplybook get_services_list
@simplybook get_performers_list
@simplybook get_bookings
@simplybook get_booking_list
```

### Tests y Demos

El proyecto incluye tests organizados por categorías y scripts de demostración:

#### Tests Organizados (`tests/`)
```bash
# Tests unitarios (no requieren servidor)
pytest tests/unit/

# Tests de integración
pytest tests/integration/

# Tests end-to-end (requieren servidor)
python3 tests/e2e/test_api_endpoints.py
python3 tests/e2e/test_booking_list_filters.py

# Scripts de utilidad
python3 tests/utils/check_server_status.py
python3 tests/utils/check_available_tools.py
python3 tests/utils/quick_test_bookings.py
```

#### Demos (`demos/`)
```bash
# Demo de filtros avanzados
python3 demos/demo_booking_list_filters.py
```

Para más información:
- **Tests**: Consulta [tests/README.md](tests/README.md)
- **Demos**: Consulta [demos/README.md](demos/README.md)

## Documentación Adicional

- **Docker Compose**: [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Claude Desktop**: [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md)
- **API SimplyBook.me**: [https://simplybook.me/en/api/developer-api/tab/rest_api](https://simplybook.me/en/api/developer-api/tab/rest_api)

## Comandos Útiles

### Docker Compose
```bash
# Iniciar servicios
docker compose up

# Iniciar en segundo plano
docker compose up -d

# Detener servicios
docker compose down

# Ver logs
docker compose logs -f

# Reconstruir imagen
docker compose up --build
```

### Verificación
```bash
# Verificar que el contenedor está ejecutándose
docker compose ps

# Verificar que el puerto está expuesto
curl http://localhost:8000/mcp/
```

## Configuración de Claude Desktop

### Configuración con npx mcp-remote (Recomendada)
```json
{
  "mcpServers": {
    "simplybook": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp/"
      ]
    }
  }
}
```

## Flujo de Ejecución

1. **Usuario** ejecuta `docker compose up --build` manualmente
2. **Docker Compose** construye la imagen y inicia el contenedor
3. **El contenedor** recibe las credenciales a través de variables de entorno
4. **El servidor MCP** autentica con SimplyBook.me y obtiene un token
5. **El token se almacena** en un archivo temporal local
6. **Todas las llamadas a la API** usan los headers `X-Company-Login` y `X-Token`
7. **Claude Desktop** se conecta al servidor MCP usando `npx mcp-remote`

## Workflow de Desarrollo

### Iniciar el Servidor
```bash
# Navegar al directorio del proyecto
cd /ruta/a/simplybook-mcp

# Configurar credenciales (si no están configuradas)
./setup-docker-claude.sh

# Iniciar el servidor
docker compose up --build
```

### Conectar Claude Desktop
1. Abrir Claude Desktop
2. Ir a Settings > MCP Servers
3. Pegar la configuración de `claude-desktop-config-docker.json`
4. Reiniciar Claude Desktop
5. Probar con `@simplybook authenticate tu_company tu_login tu_password`

### Detener el Servidor
```bash
# Detener Docker Compose
docker compose down
```

## Autenticación

El sistema implementa la autenticación según la [documentación oficial de SimplyBook.me](https://simplybook.me/en/api/developer-api/tab/rest_api):

1. **Autenticación inicial**: Se llama al endpoint `POST https://user-api-v2.simplybook.me/admin/auth` con `company`, `login` y `password`
2. **Token temporal**: El token obtenido se almacena en un archivo temporal local
3. **Headers de API**: Todas las llamadas posteriores usan:
   - `X-Company-Login`: Company login
   - `X-Token`: Token obtenido de la autenticación

## Contribuir

¡Las contribuciones son bienvenidas! Por favor abre un issue o envía un pull request para cualquier mejora o corrección de errores.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.