# Script que demonstra o container de LEITURA (opcional do desafio)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Container de Leitura - Desafio 2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Buildando imagem do leitor..." -ForegroundColor Yellow
Set-Location app
docker build -f Dockerfile.leitor -t app-leitor:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Imagem do leitor pronta!" -ForegroundColor Green
} else {
    Write-Host "  -> Erro no build" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..
Write-Host ""

Write-Host "Executando container de LEITURA..." -ForegroundColor Yellow
Write-Host "Este container so le os dados, nao modifica nada." -ForegroundColor Cyan
Write-Host ""

docker run --rm `
    -v dados-desafio2:/data:ro `
    app-leitor:latest

Write-Host ""
Write-Host "Leitura concluida!" -ForegroundColor Green
Write-Host ""
Write-Host "Nota: o volume foi montado como READ-ONLY (:ro)" -ForegroundColor Cyan
