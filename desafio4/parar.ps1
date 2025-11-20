# Para e remove os microsservicos

Write-Host "Parando microsservicos..." -ForegroundColor Yellow

docker stop ms-usuarios ms-relatorio 2>$null
docker rm ms-usuarios ms-relatorio 2>$null

Write-Host ""
Write-Host "Removendo rede..." -ForegroundColor Yellow
docker network rm rede-microservicos 2>$null

Write-Host ""
Write-Host "Tudo parado!" -ForegroundColor Green
