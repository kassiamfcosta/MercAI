@echo off
echo ============================================================
echo MercAI Backend - Iniciando Servidor
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [2/3] Verificando Python...
python --version

echo [3/3] Iniciando servidor...
echo.
echo Servidor iniciando em http://localhost:8000
echo Pressione Ctrl+C para parar
echo.
echo ============================================================
echo.

python test_server.py

pause
