#!/bin/bash

# Script para configurar Claude Desktop con el servidor MCP de SimplyBook

echo "Configurando Claude Desktop para SimplyBook MCP..."

# Solicitar API Key
read -p "Ingresa tu API Key de SimplyBook: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "Error: El API Key es requerido"
    exit 1
fi

# Obtener la ruta actual del proyecto
PROJECT_PATH=$(pwd)

# Crear configuración con stdio
cat > claude-desktop-config.json << EOF
{
  "mcpServers": {
    "simplybook": {
      "command": "python3",
      "args": ["src/main.py"],
      "env": {
        "SIMPLYBOOK_API_KEY": "$API_KEY",
        "PYTHONPATH": "$PROJECT_PATH/src"
      },
      "cwd": "$PROJECT_PATH"
    }
  }
}
EOF

# Crear configuración con HTTP
cat > claude-desktop-config-http.json << EOF
{
  "mcpServers": {
    "simplybook": {
      "command": "python3",
      "args": ["src/main.py"],
      "env": {
        "SIMPLYBOOK_API_KEY": "$API_KEY",
        "PYTHONPATH": "$PROJECT_PATH/src"
      },
      "cwd": "$PROJECT_PATH",
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/"
      }
    }
  }
}
EOF

echo "Configuración completada!"
echo ""
echo "Archivos creados:"
echo "- claude-desktop-config.json (configuración stdio)"
echo "- claude-desktop-config-http.json (configuración HTTP)"
echo ""
echo "Para usar con Claude Desktop:"
echo "1. Copia el contenido de uno de los archivos de configuración"
echo "2. Ve a Claude Desktop > Settings > MCP Servers"
echo "3. Pega la configuración en el campo correspondiente"
echo "4. Reinicia Claude Desktop"
echo ""
echo "Nota: Reemplaza 'tu_api_key_aqui' con tu API Key real de SimplyBook" 