# Script pra ver os logs dos servicos

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Logs dos Servicos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Escolha qual servico:" -ForegroundColor Yellow
Write-Host "1 - Web (frontend)"
Write-Host "2 - API (backend)"
Write-Host "3 - Cache (Redis)"
Write-Host "4 - Banco (PostgreSQL)"
Write-Host "5 - Todos"
Write-Host ""

$opcao = Read-Host "Opcao"

switch ($opcao) {
    "1" {
        Write-Host "`nLogs do Web (Ctrl+C para sair)..." -ForegroundColor Green
        docker-compose logs -f web
    }
    "2" {
        Write-Host "`nLogs da API (Ctrl+C para sair)..." -ForegroundColor Green
        docker-compose logs -f api
    }
    "3" {
        Write-Host "`nLogs do Redis (Ctrl+C para sair)..." -ForegroundColor Green
        docker-compose logs -f cache
    }
    "4" {
        Write-Host "`nLogs do PostgreSQL (Ctrl+C para sair)..." -ForegroundColor Green
        docker-compose logs -f banco
    }
    "5" {
        Write-Host "`nLogs de todos os servicos (Ctrl+C para sair)..." -ForegroundColor Green
        docker-compose logs -f
    }
    default {
        Write-Host "Opcao invalida!" -ForegroundColor Red
    }
}
