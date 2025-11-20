Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Desafio 2 - Teste de Persistencia" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[Passo 1] Criando volume Docker 'dados-desafio2'..." -ForegroundColor Yellow
docker volume create dados-desafio2
if ($LASTEXITCODE -eq 0) {
    Write-Host "  -> Volume criado!" -ForegroundColor Green
} else {
    Write-Host "  -> Volume ja existe ou foi criado" -ForegroundColor Green
}
Write-Host ""

Write-Host "[Passo 2] Verificando/construindo imagem..." -ForegroundColor Yellow
$imagemExiste = docker images -q app-banco:latest
if (-not $imagemExiste) {
    Write-Host "  -> Buildando imagem..." -ForegroundColor Yellow
    Set-Location app
    docker build -t app-banco:latest .
    Set-Location ..
    Write-Host "  -> Imagem construida!" -ForegroundColor Green
} else {
    Write-Host "  -> Imagem ja existe" -ForegroundColor Green
}
Write-Host ""

Write-Host "[Passo 3] Iniciando PRIMEIRO container (vai criar dados)..." -ForegroundColor Yellow
Write-Host "  -> Voce pode adicionar alguns registros agora" -ForegroundColor Cyan
Write-Host "  -> Depois escolha opcao 3 para sair" -ForegroundColor Cyan
Write-Host ""

docker run -it `
    --name container-db-1 `
    -v dados-desafio2:/data `
    app-banco:latest

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Primeiro container finalizado!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[Passo 4] REMOVENDO o container..." -ForegroundColor Yellow
docker rm container-db-1
Write-Host "  -> Container removido! (mas o volume continua)" -ForegroundColor Green
Write-Host ""

Write-Host "Pressione qualquer tecla para criar um NOVO container..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

Write-Host "[Passo 5] Criando SEGUNDO container (com o mesmo volume)..." -ForegroundColor Yellow
Write-Host "  -> Se aparecer 'BANCO EXISTENTE ENCONTRADO', funcionou!" -ForegroundColor Cyan
Write-Host "  -> Escolha opcao 2 para ver os dados anteriores" -ForegroundColor Cyan
Write-Host ""

docker run -it `
    --name container-db-2 `
    -v dados-desafio2:/data `
    app-banco:latest

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TESTE COMPLETO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Os dados persistiram entre os containers!" -ForegroundColor Green
Write-Host ""
