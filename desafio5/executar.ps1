# Script pra subir toda a arquitetura com Gateway

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DESAFIO 5: API Gateway + Microsservicos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Parando containers antigos..." -ForegroundColor Yellow
docker-compose down 2>$null

Write-Host ""
Write-Host "Construindo e subindo os servicos..." -ForegroundColor Green
Write-Host "  - Gateway (porta 8000)" -ForegroundColor White
Write-Host "  - Servico de Usuarios (interno)" -ForegroundColor White
Write-Host "  - Servico de Pedidos (interno)" -ForegroundColor White
Write-Host ""

docker-compose up -d --build

Start-Sleep -Seconds 8

Write-Host ""
Write-Host "Status dos containers:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Sistema Online!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Acesso UNICO via Gateway: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Rotas principais:" -ForegroundColor Cyan
Write-Host "  GET  /                    - info do gateway"
Write-Host "  GET  /health              - status de todos os servicos"
Write-Host "  GET  /dashboard           - visao geral do sistema"
Write-Host ""
Write-Host "Usuarios:" -ForegroundColor Cyan
Write-Host "  GET  /users               - lista todos"
Write-Host "  GET  /users/<id>          - busca especifico"
Write-Host "  GET  /users/state/<uf>    - filtra por estado"
Write-Host ""
Write-Host "Pedidos:" -ForegroundColor Cyan
Write-Host "  GET  /orders              - lista todos"
Write-Host "  GET  /orders/<id>         - busca especifico"
Write-Host "  GET  /orders/user/<id>    - pedidos de um usuario (COMBINA dados!)"
Write-Host "  GET  /orders/status/<st>  - filtra por status"
Write-Host ""
Write-Host "Teste rapido:" -ForegroundColor Yellow
Write-Host '  curl http://localhost:8000/health'
Write-Host '  curl http://localhost:8000/dashboard'
Write-Host '  curl http://localhost:8000/orders/user/1'
