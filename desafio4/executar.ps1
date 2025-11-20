Write-Host "=== DESAFIO 4: Microsservicos Independentes ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Parando containers antigos..." -ForegroundColor Yellow
docker stop ms-usuarios ms-relatorio 2>$null
docker rm ms-usuarios ms-relatorio 2>$null

Write-Host ""
Write-Host "Criando rede de comunicacao..." -ForegroundColor Green
docker network create rede-microservicos 2>$null

Write-Host ""
Write-Host "Subindo microsservico de USUARIOS..." -ForegroundColor Green
cd servico-usuarios
docker build -t ms-usuarios .
docker run -d `
    --name ms-usuarios `
    --network rede-microservicos `
    -p 5000:5000 `
    ms-usuarios

cd ..

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Subindo microsservico de RELATORIO..." -ForegroundColor Green
cd servico-relatorio
docker build -t ms-relatorio .
docker run -d `
    --name ms-relatorio `
    --network rede-microservicos `
    -e USUARIOS_URL=http://ms-usuarios:5000 `
    -p 5001:5001 `
    ms-relatorio

cd ..

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Status dos containers:" -ForegroundColor Cyan
docker ps --filter "name=ms-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host ""
Write-Host "=== Pronto! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Microsservicos rodando:" -ForegroundColor Yellow
Write-Host "  Usuarios:   http://localhost:5000"
Write-Host "  Relatorio:  http://localhost:5001"
Write-Host ""
Write-Host "Testes rapidos:" -ForegroundColor Cyan
Write-Host "  curl http://localhost:5000/usuarios         # lista usuarios"
Write-Host "  curl http://localhost:5001/relatorio        # relatorio simples"
Write-Host "  curl http://localhost:5001/relatorio/completo   # relatorio detalhado"
