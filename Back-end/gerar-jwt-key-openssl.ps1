# Script equivalente ao: openssl rand -hex 32
# Gera uma string hexadecimal aleatória de 64 caracteres (32 bytes em hex)

Write-Host "Gerando JWT_SECRET_KEY (equivalente a: openssl rand -hex 32)..." -ForegroundColor Green
Write-Host ""

# Gera bytes aleatórios e converte para hexadecimal
$bytes = New-Object byte[] 32
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$rng.GetBytes($bytes)
$hexString = ($bytes | ForEach-Object { $_.ToString("x2") }) -join ""

Write-Host "JWT_SECRET_KEY gerada (formato hexadecimal):" -ForegroundColor Yellow
Write-Host $hexString -ForegroundColor Cyan
Write-Host ""
Write-Host "Copie o valor acima e cole no arquivo .env como JWT_SECRET_KEY" -ForegroundColor Green
Write-Host ""
Write-Host "Exemplo de como deve ficar no .env:" -ForegroundColor Yellow
Write-Host "JWT_SECRET_KEY=$hexString" -ForegroundColor Gray

