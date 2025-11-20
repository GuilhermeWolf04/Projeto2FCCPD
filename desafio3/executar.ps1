# Script pra subir os 3 servicos do Desafio 3

Write-Host "=== DESAFIO 3: Docker Compose ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Parando containers antigos..." -ForegroundColor Yellow
docker-compose down 2>$null

Write-Host ""
Write-Host "Subindo os 3 servicos (processador + armazenador + notificador)..." -ForegroundColor Green
docker-compose up -d --build

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Status dos containers:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "=== Pronto! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Servicos rodando:" -ForegroundColor Yellow
Write-Host "  Processador:   http://localhost:5000"
Write-Host "  Armazenador:   http://localhost:5001"
Write-Host "  Notificador:   http://localhost:5002"
Write-Host ""
Write-Host "Teste:" -ForegroundColor Cyan
Write-Host '  curl -X POST http://localhost:5000/processar -H "Content-Type: application/json" -d "{\"dado\":\"teste do sistema\"}"'
