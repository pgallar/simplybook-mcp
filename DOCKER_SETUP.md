# Configuración de Docker Compose para SimplyBook MCP

Esta guía te ayudará a configurar y ejecutar el servidor MCP de SimplyBook usando Docker Compose.

## Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Acceso a las credenciales de SimplyBook.me:
  - Company Login
  - User Login
  - Password

## Configuración Rápida

### 1. Configuración Automática

Ejecuta el script de configuración:

```bash
./setup-docker-claude.sh
```

Este script:
- Solicita tus credenciales de SimplyBook
- Crea el archivo `.env` con las variables de entorno
- Genera `claude-desktop-config-docker.json` para Claude Desktop

### 2. Iniciar el Servidor

```bash
docker compose up --build
```

### 3. Configurar Claude Desktop

1. Abre Claude Desktop
2. Ve a Settings > MCP Servers
3. Copia y pega el contenido de `claude-desktop-config-docker.json`
4. Reinicia Claude Desktop

## Configuración Manual

### 1. Variables de Entorno

Crea un archivo `.env` en el directorio raíz:

```bash
# Archivo .env
SIMPLYBOOK_COMPANY=tu_company_login
SIMPLYBOOK_LOGIN=tu_user_login
SIMPLYBOOK_PASSWORD=tu_password
```

### 2. Configuración de Claude Desktop

Crea `claude-desktop-config-docker.json`:

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

### 3. Ejecutar Docker Compose

```bash
docker compose up --build
```

## Estructura de Archivos

```
simplybook-mcp/
├── docker-compose.yml                  # Configuración de servicios
├── Dockerfile                          # Imagen de Docker
├── .env                                # Variables de entorno (creado por setup)
├── claude-desktop-config-docker.json  # Configuración de Claude Desktop
├── setup-docker-claude.sh             # Script de configuración
└── start-server.sh                    # Script de inicio
```

## Comandos Útiles

### Gestión de Contenedores

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

# Verificar estado
docker compose ps
```

### Verificación de Salud

```bash
# Verificar que el puerto está expuesto
curl http://localhost:8000/mcp/

# Verificar logs del contenedor
docker compose logs simplybook-mcp

# Verificar variables de entorno
docker compose exec simplybook-mcp env | grep SIMPLYBOOK
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

## Configuración de Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  simplybook-mcp:
    build: .
    container_name: simplybook-mcp
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
      - ./logs:/app/logs
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=INFO
      - SIMPLYBOOK_COMPANY=${SIMPLYBOOK_COMPANY}
      - SIMPLYBOOK_LOGIN=${SIMPLYBOOK_LOGIN}
      - SIMPLYBOOK_PASSWORD=${SIMPLYBOOK_PASSWORD}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/mcp/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "src/main.py"]
```

## Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `SIMPLYBOOK_COMPANY` | Company login de SimplyBook | Sí |
| `SIMPLYBOOK_LOGIN` | User login de SimplyBook | Sí |
| `SIMPLYBOOK_PASSWORD` | Password de SimplyBook | Sí |
| `ENVIRONMENT` | Entorno de ejecución | No (default: development) |
| `LOG_LEVEL` | Nivel de logging | No (default: INFO) |

## Diagnóstico de Problemas

### Error: "Unexpected token 'E', "ECHO est activado." is not valid JSON"

**Síntoma**: Claude Desktop muestra error al intentar conectarse al servidor MCP.

**Causa**: La configuración incluye `command`, `args` o `env` que ejecutan comandos del sistema en lugar de conectarse al servidor HTTP.

**Solución**: Usar la configuración con `npx mcp-remote`:
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

### Error: "simplybook-mcp exited with code 0"

**Síntoma**: El contenedor se inicia y luego se detiene inmediatamente.

**Causa**: Error en el código Python o configuración incorrecta.

**Solución**:
```bash
# Ver logs detallados
docker compose logs simplybook-mcp

# Verificar variables de entorno
docker compose exec simplybook-mcp env | grep SIMPLYBOOK
```

### Error: "curl: (22) The requested URL returned error: 404"

**Síntoma**: Health check falla con error 404.

**Causa**: El servidor no está respondiendo en el endpoint correcto.

**Solución**:
```bash
# Verificar que el servidor esté ejecutándose
docker compose ps

# Verificar logs del servidor
docker compose logs -f simplybook-mcp

# Verificar manualmente
curl http://localhost:8000/mcp/
```

### Error: "no configuration file provided: not found"

**Síntoma**: Docker Compose no encuentra el archivo de configuración.

**Causa**: Ejecutando desde el directorio incorrecto.

**Solución**:
```bash
# Verificar que estás en el directorio correcto
ls -la docker-compose.yml

# Navegar al directorio correcto
cd /ruta/a/simplybook-mcp
```

## Scripts de Utilidad

### start-server.sh

Script para iniciar el servidor con verificaciones:

```bash
#!/bin/bash

echo "=== Iniciando Servidor MCP de SimplyBook ==="

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "Ejecuta primero: ./setup-docker-claude.sh"
    exit 1
fi

# Verificar Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose"
    exit 1
fi

# Verificar variables de entorno
source .env
if [ -z "$SIMPLYBOOK_COMPANY" ] || [ -z "$SIMPLYBOOK_LOGIN" ] || [ -z "$SIMPLYBOOK_PASSWORD" ]; then
    echo "❌ Variables de entorno incompletas"
    exit 1
fi

echo "✅ Iniciando servidor..."
docker compose up --build
```

### setup-docker-claude.sh

Script de configuración automática:

```bash
#!/bin/bash

echo "Configurando Claude Desktop para SimplyBook MCP..."

# Solicitar credenciales
read -p "Ingresa tu Company Login: " COMPANY
read -p "Ingresa tu User Login: " LOGIN
read -s -p "Ingresa tu Password: " PASSWORD

# Crear archivos de configuración
cat > .env << EOF
SIMPLYBOOK_COMPANY=$COMPANY
SIMPLYBOOK_LOGIN=$LOGIN
SIMPLYBOOK_PASSWORD=$PASSWORD
EOF

cat > claude-desktop-config-docker.json << EOF
{
  "mcpServers": {
    "simplybook": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/"
      }
    }
  }
}
EOF

echo "Configuración completada!"
```

## Seguridad

### Variables de Entorno

- Las credenciales se almacenan en el archivo `.env`
- El archivo `.env` debe estar en `.gitignore`
- Nunca commits credenciales al repositorio

### Red

- El servidor solo expone el puerto 8000
- Las conexiones son locales (localhost)
- No se requiere configuración de firewall adicional

## Rendimiento

### Optimizaciones

- **Cache de Docker**: Las dependencias se cachean en capas separadas
- **Health Checks**: Monitoreo automático del estado del servidor
- **Restart Policy**: Reinicio automático en caso de fallo

### Monitoreo

```bash
# Ver uso de recursos
docker stats simplybook-mcp

# Ver logs en tiempo real
docker compose logs -f

# Verificar estado de salud
curl http://localhost:8000/mcp/
```

## Actualizaciones

### Actualizar el Servidor

```bash
# Detener servicios
docker compose down

# Reconstruir imagen
docker compose up --build

# O usar el script
./start-server.sh
```

### Actualizar Configuración

```bash
# Regenerar configuración
./setup-docker-claude.sh

# Reiniciar servicios
docker compose restart
``` 