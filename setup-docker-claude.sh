#!/bin/bash

# Script para configurar Claude Desktop para SimplyBook MCP con Docker Compose

echo "Configurando Claude Desktop para SimplyBook MCP con Docker Compose..."
echo ""

# Solicitar credenciales
read -p "Ingresa tu Company Login: " COMPANY
read -p "Ingresa tu User Login: " LOGIN
read -s -p "Ingresa tu Password: " PASSWORD
echo ""

if [ -z "$COMPANY" ] || [ -z "$LOGIN" ] || [ -z "$PASSWORD" ]; then
    echo "Error: Todas las credenciales son requeridas"
    exit 1
fi

# Crear archivo .env
cat > .env << EOF
SIMPLYBOOK_COMPANY=$COMPANY
SIMPLYBOOK_LOGIN=$LOGIN
SIMPLYBOOK_PASSWORD=$PASSWORD
EOF

echo "Archivo .env creado con tus credenciales"

# Crear configuración para Claude Desktop (usando npx mcp-remote)
cat > claude-desktop-config-docker.json << EOF
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
EOF

echo "Configuración completada!"
echo ""
echo "Archivos creados:"
echo "- .env (con tus credenciales)"
echo "- claude-desktop-config-docker.json (configuración para Claude Desktop)"
echo ""
echo "Pasos para usar:"
echo ""
echo "1. Inicia el servidor MCP manualmente:"
echo "   docker compose up --build"
echo ""
echo "2. En Claude Desktop:"
echo "   - Ve a Settings > MCP Servers"
echo "   - Copia y pega el contenido de claude-desktop-config-docker.json"
echo "   - Reinicia Claude Desktop"
echo ""
echo "3. Prueba la conexión:"
echo "   @simplybook authenticate $COMPANY $LOGIN [password]"
echo "   @simplybook get_services_list"
echo ""
echo "Nota: El servidor MCP debe estar ejecutándose antes de usar Claude Desktop" 