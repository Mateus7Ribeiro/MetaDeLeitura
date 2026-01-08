@echo off
REM Script para instalar o projeto Mesa Literária no Windows

echo ========================================
echo Instalador - Mesa Literária
echo ========================================
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo Erro ao criar ambiente virtual
    exit /b 1
)

echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar dependencias
    exit /b 1
)

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas credenciais do MySQL
echo 2. Crie o banco de dados: CREATE DATABASE meta_leitura;
echo 3. Execute: python run.py
echo.
pause
