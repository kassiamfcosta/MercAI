# Script PowerShell para iniciar o servidor MercAI
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "MercAI Backend - Iniciando Servidor" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Mudar para o diretório do script
Set-Location $PSScriptRoot

# Ativar ambiente virtual
Write-Host "[1/3] Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Verificar Python
Write-Host "[2/3] Verificando Python..." -ForegroundColor Yellow
python --version

# Iniciar servidor
Write-Host "[3/3] Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Servidor iniciando em http://localhost:8000" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python test_server.py
