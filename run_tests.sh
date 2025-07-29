#!/bin/bash

echo "=== Ejecutando Tests Unitarios de SimplyBook MCP ==="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: No se encontró requirements.txt"
    echo "Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que pytest esté instalado
if ! command -v pytest &> /dev/null; then
    echo "📦 Instalando dependencias de testing..."
    pip install -r requirements.txt
fi

echo "🧪 Ejecutando tests unitarios..."
echo ""

# Ejecutar tests con cobertura
pytest tests/ -v --tb=short --asyncio-mode=auto

echo ""
echo "=== Tests Completados ===" 