Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desafio 1 - Containers em Rede" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[Passo 1] Criando rede Docker 'rede-desafio1'..." -ForegroundColor Yellow
docker network create rede-desafio1 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  → Rede já existe ou foi criada com sucesso" -ForegroundColor Green
} else {
    Write-Host "  → Rede criada com sucesso!" -ForegroundColor Green
}
Write-Host ""

Write-Host "[Passo 2] Construindo imagem do servidor..." -ForegroundColor Yellow
Set-Location servidor
docker build -t servidor-web:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "  → Imagem do servidor construída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "  → Erro ao construir imagem do servidor" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host ""

Write-Host "[Passo 3] Construindo imagem do cliente..." -ForegroundColor Yellow
Set-Location cliente
docker build -t cliente-http:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "  → Imagem do cliente construída com sucesso!" -ForegroundColor Green
} else {
    Write-Host "  → Erro ao construir imagem do cliente" -ForegroundColor Red
    exit 1
}
Set-Location ..
Write-Host ""

Write-Host "[Passo 4] Iniciando container do servidor..." -ForegroundColor Yellow
docker run -d `
    --name servidor-web `
    --network rede-desafio1 `
    -p 8080:8080 `
    servidor-web:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "  → Servidor iniciado com sucesso!" -ForegroundColor Green
    Write-Host "  → Acessível em: http://localhost:8080" -ForegroundColor Cyan
} else {
    Write-Host "  → Erro ao iniciar servidor (possivelmente já está rodando)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "Aguardando servidor ficar pronto..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host ""

Write-Host "[Passo 5] Iniciando container do cliente..." -ForegroundColor Yellow
docker run -d `
    --name cliente-http `
    --network rede-desafio1 `
    cliente-http:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host "  → Cliente iniciado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "  → Erro ao iniciar cliente (possivelmente já está rodando)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Status dos Containers:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
docker ps --filter "network=rede-desafio1" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Próximos Passos:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Para visualizar os logs do servidor:" -ForegroundColor White
Write-Host "  docker logs -f servidor-web" -ForegroundColor Green
Write-Host ""
Write-Host "Para visualizar os logs do cliente:" -ForegroundColor White
Write-Host "  docker logs -f cliente-http" -ForegroundColor Green
Write-Host ""
Write-Host "Para parar os containers:" -ForegroundColor White
Write-Host "  .\parar.ps1" -ForegroundColor Green
Write-Host ""
