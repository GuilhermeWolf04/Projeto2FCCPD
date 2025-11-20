# Para todos os servicos

Write-Host "Parando API Gateway e microsservicos..." -ForegroundColor Yellow

docker-compose down

Write-Host ""
Write-Host "Tudo parado!" -ForegroundColor Green
