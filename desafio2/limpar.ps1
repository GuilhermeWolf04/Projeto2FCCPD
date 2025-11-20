# Script pra limpar tudo do desafio 2

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Limpando Desafio 2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Parando e removendo containers..." -ForegroundColor Yellow
docker rm -f app-db container-db-1 container-db-2 2>$null
Write-Host "  -> Containers removidos" -ForegroundColor Green
Write-Host ""

Write-Host "Quer remover o VOLUME tambem? (dados serao perdidos)" -ForegroundColor Yellow
Write-Host "1 - Sim, remover tudo"
Write-Host "2 - Nao, manter o volume com os dados"
$opcao = Read-Host "Escolha"

if ($opcao -eq "1") {
    Write-Host "Removendo volume..." -ForegroundColor Yellow
    docker volume rm dados-desafio2 2>$null
    Write-Host "  -> Volume removido!" -ForegroundColor Green
} else {
    Write-Host "  -> Volume mantido (dados preservados)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Limpeza concluida!" -ForegroundColor Green
