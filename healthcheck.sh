#!/bin/bash
# Healthcheck personalizado para el servidor MCP SSE

# Configuración
HOST="localhost"
PORT="8001"
ENDPOINT="/sse/"
TIMEOUT=10
MAX_RETRIES=3

# Función para verificar si el servidor está respondiendo
check_server() {
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        # Intentar conectar al endpoint SSE
        response=$(curl -s -o /dev/null -w "%{http_code}" --max-time $TIMEOUT "http://$HOST:$PORT$ENDPOINT" 2>/dev/null)
        
        if [ "$response" = "200" ]; then
            echo "✅ Server is healthy (HTTP $response)"
            exit 0
        else
            echo "⚠️  Server check failed (HTTP $response), retry $((retry_count + 1))/$MAX_RETRIES"
            retry_count=$((retry_count + 1))
            sleep 2
        fi
    done
    
    echo "❌ Server health check failed after $MAX_RETRIES retries"
    exit 1
}

# Ejecutar el healthcheck
check_server 