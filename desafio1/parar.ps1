# Script para parar e limpar os containers do Desafio 1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Parando Containers - Desafio 1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Parando containers..." -ForegroundColor Yellow
docker stop servidor-web cliente-http 2>$null
Write-Host "  → Containers parados" -ForegroundColor Green
Write-Host ""

Write-Host "Removendo containers..." -ForegroundColor Yellow
docker rm servidor-web cliente-http 2>$null
Write-Host "  → Containers removidos" -ForegroundColor Green
Write-Host ""

Write-Host "Removendo rede..." -ForegroundColor Yellow
docker network rm rede-desafio1 2>$null
Write-Host "  → Rede removida" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Limpeza concluída!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
