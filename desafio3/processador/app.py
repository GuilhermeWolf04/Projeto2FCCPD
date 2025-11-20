from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# pega os enderecos dos outros servicos
ARMAZENADOR_URL = os.getenv('ARMAZENADOR_URL', 'http://armazenador:5001')
NOTIFICADOR_URL = os.getenv('NOTIFICADOR_URL', 'http://notificador:5002')

# simula alguns dados processados
dados_processados = []

@app.route('/')
def index():
    return jsonify({
        'servico': 'processador',
        'funcao': 'recebe requisicoes e processa dados',
        'rotas': ['/processar', '/dados', '/status']
    })

@app.route('/processar', methods=['POST'])
def processar():
    # pega o dado enviado
    dado = request.json.get('dado', 'sem dados')
    
    # simula processamento (transforma em maiuscula, conta caracteres, etc)
    resultado = {
        'original': dado,
        'processado': dado.upper(),
        'tamanho': len(dado),
        'palavras': len(dado.split())
    }
    
    dados_processados.append(resultado)
    
    # manda pro armazenador guardar
    try:
        resp_arma = requests.post(
            f'{ARMAZENADOR_URL}/guardar',
            json={'tipo': 'processamento', 'conteudo': resultado},
            timeout=3
        )
        resultado['armazenado'] = resp_arma.status_code == 200
    except:
        resultado['armazenado'] = False
    
    # manda pro notificador avisar
    try:
        resp_notif = requests.post(
            f'{NOTIFICADOR_URL}/notificar',
            json={'mensagem': f'Processado: {dado[:20]}...'},
            timeout=3
        )
        resultado['notificado'] = resp_notif.status_code == 200
    except:
        resultado['notificado'] = False
    
    return jsonify(resultado)

@app.route('/dados')
def listar_dados():
    return jsonify({
        'total': len(dados_processados),
        'ultimos': dados_processados[-5:]
    })

@app.route('/status')
def status():
    # tenta pingar os outros servicos
    status_servicos = {'processador': 'ok'}
    
    try:
        r = requests.get(f'{ARMAZENADOR_URL}/', timeout=2)
        status_servicos['armazenador'] = 'ok' if r.status_code == 200 else 'erro'
    except:
        status_servicos['armazenador'] = 'offline'
    
    try:
        r = requests.get(f'{NOTIFICADOR_URL}/', timeout=2)
        status_servicos['notificador'] = 'ok' if r.status_code == 200 else 'erro'
    except:
        status_servicos['notificador'] = 'offline'
    
    return jsonify(status_servicos)

if __name__ == '__main__':
    print("Servico PROCESSADOR rodando na porta 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
