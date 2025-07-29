#!/bin/bash

# Script para iniciar el servidor MCP de SimplyBook

echo "=== Iniciando Servidor MCP de SimplyBook ==="
echo ""

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "Ejecuta primero: ./setup-docker-claude.sh"
    exit 1
fi

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose"
    echo "Inicia Docker Desktop y vuelve a intentar"
    exit 1
fi

# Verificar que las variables de entorno estén configuradas
source .env
if [ -z "$SIMPLYBOOK_COMPANY" ] || [ -z "$SIMPLYBOOK_LOGIN" ] || [ -z "$SIMPLYBOOK_PASSWORD" ]; then
    echo "❌ Variables de entorno incompletas en .env"
    echo "Verifica que SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN y SIMPLYBOOK_PASSWORD estén configuradas"
    exit 1
fi

echo "✅ Docker está ejecutándose"
echo "✅ Archivo .env encontrado"
echo "✅ Credenciales configuradas"
echo ""

# Detener contenedores existentes si los hay
echo "Deteniendo contenedores existentes..."
docker compose down > /dev/null 2>&1

# Iniciar el servidor
echo "Iniciando servidor MCP..."
echo ""

docker compose up --build

echo ""
echo "=== Servidor MCP detenido ===" 