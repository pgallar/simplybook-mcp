#!/bin/bash

echo "=== Ejecutando Tests de Integración de SimplyBook MCP ==="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: No se encontró requirements.txt"
    echo "Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que las credenciales estén configuradas
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encontró archivo .env"
    echo "Ejecuta primero: ./setup-docker-claude.sh"
    exit 1
fi

# Cargar variables de entorno
source .env

if [ -z "$SIMPLYBOOK_COMPANY" ] || [ -z "$SIMPLYBOOK_LOGIN" ] || [ -z "$SIMPLYBOOK_PASSWORD" ]; then
    echo "❌ Error: Credenciales incompletas en .env"
    echo "Verifica que SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN y SIMPLYBOOK_PASSWORD estén configuradas"
    exit 1
fi

echo "✅ Credenciales configuradas"
echo ""

# Verificar que pytest esté instalado
if ! command -v pytest &> /dev/null; then
    echo "📦 Instalando dependencias de testing..."
    pip install -r requirements.txt
fi

echo "🧪 Ejecutando tests de integración..."
echo ""

# Ejecutar tests de integración
pytest tests/test_integration.py -v --tb=short --asyncio-mode=auto

echo ""
echo "=== Tests de Integración Completados ===" 