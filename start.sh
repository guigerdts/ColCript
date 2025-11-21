#!/bin/bash

echo "🪙 Iniciando ColCript Web Interface..."
echo ""
echo "Servidor disponible en:"
echo "  - Local: http://localhost:5000"
echo "  - Red:   http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

cd ~/ColCript
python api/server.py
