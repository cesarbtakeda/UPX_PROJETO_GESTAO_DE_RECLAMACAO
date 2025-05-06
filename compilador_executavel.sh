#!/bin/bash

# Nome do executável final (COM .exe)
OUTPUT_NAME="GerenciadorReclamacoes.exe"

# Comando de compilação corrigido
pyinstaller --onefile --noconsole \
    --add-data "interface.py:." \
    --add-data "reclamacoes.py:." \
    --add-data "pegar_urls.py:." \
    --add-data "graficos.py:." \
  
    --name "$OUTPUT_NAME" \
    ./interface.py  # Note o ./ antes do nome do arquivo

# Verificação
if [ -f "dist/$OUTPUT_NAME" ]; then
    echo "✅ Compilação bem-sucedida! Executável gerado em: dist/$OUTPUT_NAME"
else
    echo "❌ Falha na compilação! Verifique os erros acima."
fi
