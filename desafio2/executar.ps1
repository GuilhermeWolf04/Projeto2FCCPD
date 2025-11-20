# Script simples pra rodar o container com volume

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desafio 2 - Volumes e Persistencia" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Criando/verificando volume..." -ForegroundColor Yellow
docker volume create dados-desafio2 2>$null
Write-Host "  -> OK" -ForegroundColor Green
Write-Host ""

Write-Host "Buildando imagem..." -ForegroundColor Yellow
Set-Location app
docker build -t app-banco:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Imagem pronta!" -ForegroundColor Green
} else {
    Write-Host "  -> Erro no build" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host ""

docker rm -f app-db 2>$null

Write-Host "Iniciando container com volume..." -ForegroundColor Yellow
Write-Host ""

docker run -it `
    --name app-db `
    -v dados-desafio2:/data `
    app-banco:latest

Write-Host ""
Write-Host "Container finalizado!" -ForegroundColor Green
