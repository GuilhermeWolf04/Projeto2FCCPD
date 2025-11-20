# Script pra parar os servicos

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Parando servicos do Docker Compose" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

docker-compose down

Write-Host ""
Write-Host "Servicos parados!" -ForegroundColor Green
Write-Host ""
Write-Host "Quer remover o volume do banco tambem? (dados serao perdidos)" -ForegroundColor Yellow
Write-Host "1 - Sim, remover tudo"
Write-Host "2 - Nao, manter os dados"
$opcao = Read-Host "Escolha"

if ($opcao -eq "1") {
    Write-Host ""
    Write-Host "Removendo volumes..." -ForegroundColor Yellow
    docker-compose down -v
    Write-Host "Tudo removido!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Volume mantido (dados do banco preservados)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Concluido!" -ForegroundColor Green
