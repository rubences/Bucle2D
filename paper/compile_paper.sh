#!/bin/bash
# Script para compilar el paper LaTeX
# Uso: ./compile_paper.sh

set -e

PAPER_DIR="/workspaces/Bucle2D/paper"
MAIN_TEX="main.tex"

echo "=========================================="
echo "Compilando Paper: Agentic-Racing-Vision"
echo "=========================================="
echo ""

cd "$PAPER_DIR"

# Verificar que existe el archivo principal
if [ ! -f "$MAIN_TEX" ]; then
    echo "❌ Error: No se encuentra $MAIN_TEX en $PAPER_DIR"
    exit 1
fi

echo "📄 Archivo encontrado: $MAIN_TEX"
echo ""

# Primera compilación
echo "🔧 Primera compilación de LaTeX..."
pdflatex -interaction=nonstopmode "$MAIN_TEX" > compile_log_1.txt 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Primera compilación exitosa"
else
    echo "⚠️  Primera compilación con advertencias (normal)"
fi
echo ""

# Compilar bibliografía
echo "📚 Procesando bibliografía..."
if bibtex main > bibtex_log.txt 2>&1; then
    echo "✅ Bibliografía procesada"
else
    echo "⚠️  BibTeX con advertencias (revisar referencias)"
fi
echo ""

# Segunda compilación (para resolver referencias)
echo "🔧 Segunda compilación de LaTeX..."
pdflatex -interaction=nonstopmode "$MAIN_TEX" > compile_log_2.txt 2>&1
echo "✅ Segunda compilación completada"
echo ""

# Tercera compilación (para resolver referencias cruzadas)
echo "🔧 Tercera compilación de LaTeX (referencias cruzadas)..."
pdflatex -interaction=nonstopmode "$MAIN_TEX" > compile_log_3.txt 2>&1
echo "✅ Tercera compilación completada"
echo ""

# Verificar que se generó el PDF
if [ -f "main.pdf" ]; then
    echo "=========================================="
    echo "✅ COMPILACIÓN EXITOSA"
    echo "=========================================="
    echo ""
    echo "📋 Archivo generado: $PAPER_DIR/main.pdf"
    echo "📊 Tamaño: $(du -h main.pdf | cut -f1)"
    echo "📄 Páginas: $(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}')"
    echo ""
    echo "🧹 Limpiando archivos temporales..."
    rm -f *.aux *.log *.out *.toc *.bbl *.blg compile_log_*.txt bibtex_log.txt
    echo "✅ Limpieza completada"
else
    echo "=========================================="
    echo "❌ ERROR EN LA COMPILACIÓN"
    echo "=========================================="
    echo ""
    echo "📋 Revisa los archivos de log:"
    echo "   - compile_log_1.txt"
    echo "   - compile_log_2.txt"
    echo "   - compile_log_3.txt"
    echo "   - bibtex_log.txt"
    exit 1
fi

echo ""
echo "Para ver el PDF:"
echo "  - VS Code: Click derecho en main.pdf → 'Open Preview'"
echo "  - Terminal: xdg-open main.pdf"
echo ""
