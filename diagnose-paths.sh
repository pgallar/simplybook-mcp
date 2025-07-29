#!/bin/bash

echo "=== Diagnóstico de Rutas para Docker Compose ==="
echo ""

echo "1. Ruta actual en WSL:"
pwd
echo ""

echo "2. Verificando si docker-compose.yml existe:"
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml encontrado"
else
    echo "❌ docker-compose.yml NO encontrado"
fi
echo ""

echo "3. Verificando si Dockerfile existe:"
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile encontrado"
else
    echo "❌ Dockerfile NO encontrado"
fi
echo ""

echo "4. Ruta de Windows equivalente (aproximada):"
echo "C:\\Users\\pgall\\AppData\\Local\\Packages\\CanonicalGroupLimited.Ubuntu_79rhkp1fndgsc\\LocalState\\rootfs\\home\\pgallar\\Works\\simplybook-mcp"
echo ""

echo "5. Probando docker compose desde WSL:"
if command -v docker &> /dev/null; then
    echo "✅ Docker encontrado en WSL"
    echo "Probando 'docker compose config'..."
    docker compose config > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ docker compose config ejecutado exitosamente"
    else
        echo "❌ Error en docker compose config"
    fi
else
    echo "❌ Docker NO encontrado en WSL"
fi
echo ""

echo "6. Verificando variables de entorno:"
if [ -n "$SIMPLYBOOK_API_KEY" ]; then
    echo "✅ SIMPLYBOOK_API_KEY está configurada"
else
    echo "❌ SIMPLYBOOK_API_KEY NO está configurada"
fi
echo ""

echo "=== Fin del Diagnóstico ===" 