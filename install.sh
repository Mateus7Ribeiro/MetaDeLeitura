#!/bin/bash
# Script para instalar o projeto Meta de Leitura no macOS/Linux

echo "========================================"
echo "Instalador - Meta de Leitura"
echo "========================================"
echo ""

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Erro ao criar ambiente virtual"
    exit 1
fi

echo ""
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo ""
echo "Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erro ao instalar dependencias"
    exit 1
fi

echo ""
echo "========================================"
echo "Instalacao concluida!"
echo "========================================"
echo ""
echo "Proximos passos:"
echo "1. Edite o arquivo .env com suas credenciais do MySQL"
echo "2. Crie o banco de dados: CREATE DATABASE meta_leitura;"
echo "3. Execute: python run.py"
echo ""
