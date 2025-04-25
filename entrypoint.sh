#!/bin/sh

echo "Ejecutando script de inicializacion de base de datos..."

set -e

PYTHONPATH=/app python src/models/user_model.py

echo "Inicializacion de base de datos finalizada."

echo "Iniciando servidor de aplicacion..."
exec "$@"