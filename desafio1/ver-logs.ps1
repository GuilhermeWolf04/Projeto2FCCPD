# Script para visualizar logs em tempo real dos containers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Logs dos Containers - Desafio 1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Escolha qual log deseja visualizar:" -ForegroundColor Yellow
Write-Host "1 - Servidor Web" -ForegroundColor White
Write-Host "2 - Cliente HTTP" -ForegroundColor White
Write-Host "3 - Ambos (lado a lado)" -ForegroundColor White
Write-Host ""

$opcao = Read-Host "Digite o número da opção"

switch ($opcao) {
    "1" {
        Write-Host "`nExibindo logs do Servidor Web (Ctrl+C para sair)..." -ForegroundColor Green
        docker logs -f servidor-web
    }
    "2" {
        Write-Host "`nExibindo logs do Cliente HTTP (Ctrl+C para sair)..." -ForegroundColor Green
        docker logs -f cliente-http
    }
    "3" {
        Write-Host "`nAbrindo logs em novas janelas..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker logs -f servidor-web"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "docker logs -f cliente-http"
    }
    default {
        Write-Host "Opção inválida!" -ForegroundColor Red
    }
}
