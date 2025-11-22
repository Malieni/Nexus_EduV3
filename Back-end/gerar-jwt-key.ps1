# Script para gerar JWT Secret Key
# Execute este script no PowerShell para gerar uma chave segura

Write-Host "Gerando JWT Secret Key..." -ForegroundColor Green
Write-Host ""

# Gera uma string aleatória segura de 64 caracteres
$chars = (65..90) + (97..122) + (48..57)  # A-Z, a-z, 0-9
$key = -join ((Get-Random -InputObject $chars -Count 64) | ForEach-Object {[char]$_})

Write-Host "JWT_SECRET_KEY gerada:" -ForegroundColor Yellow
Write-Host $key -ForegroundColor Cyan
Write-Host ""
Write-Host "Copie o valor acima e cole no arquivo .env como JWT_SECRET_KEY" -ForegroundColor Green

