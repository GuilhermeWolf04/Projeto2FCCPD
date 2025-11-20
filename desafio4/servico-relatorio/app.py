from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

USUARIOS_URL = os.getenv('USUARIOS_URL', 'http://localhost:5000')

def calcular_tempo_cadastro(data_cadastro):
    try:
        data = datetime.strptime(data_cadastro, '%Y-%m-%d')
        hoje = datetime.now()
        diferenca = hoje - data
        
        anos = diferenca.days // 365
        meses = (diferenca.days % 365) // 30
        dias = (diferenca.days % 365) % 30
        
        if anos > 0:
            return f"{anos} ano(s) e {meses} mes(es)"
        elif meses > 0:
            return f"{meses} mes(es) e {dias} dia(s)"
        else:
            return f"{dias} dia(s)"
    except:
        return "data invalida"

@app.route('/')
def index():
    return jsonify({
        'servico': 'relatorio',
        'versao': '1.0',
        'descricao': 'Consome API de usuarios e gera relatorios',
        'rotas': ['/relatorio', '/relatorio/completo', '/status']
    })

@app.route('/relatorio')
def gerar_relatorio():
    try:
        resposta = requests.get(f'{USUARIOS_URL}/usuarios', timeout=5)
        
        if resposta.status_code != 200:
            return jsonify({'erro': 'falha ao buscar usuarios'}), 500
        
        dados = resposta.json()
        usuarios = dados.get('usuarios', [])
        
        relatorio = []
        for user in usuarios:
            status_texto = "ativo" if user['ativo'] else "inativo"
            tempo = calcular_tempo_cadastro(user['cadastrado_em'])
            
            relatorio.append({
                'nome': user['nome'],
                'situacao': f"{status_texto} desde {tempo}"
            })
        
        return jsonify({
            'total': len(relatorio),
            'relatorio': relatorio
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': f'nao consegui conectar no servico de usuarios: {str(e)}'}), 503

@app.route('/relatorio/completo')
def relatorio_completo():
    try:
        resp_usuarios = requests.get(f'{USUARIOS_URL}/usuarios', timeout=5)

        resp_stats = requests.get(f'{USUARIOS_URL}/stats', timeout=5)
        
        if resp_usuarios.status_code != 200 or resp_stats.status_code != 200:
            return jsonify({'erro': 'falha ao buscar dados'}), 500
        
        usuarios = resp_usuarios.json().get('usuarios', [])
        stats = resp_stats.json()
        
        usuarios_processados = []
        for user in usuarios:
            tempo = calcular_tempo_cadastro(user['cadastrado_em'])
            status_emoji = "✓" if user['ativo'] else "✗"
            
            usuarios_processados.append({
                'id': user['id'],
                'nome': user['nome'],
                'email': user['email'],
                'status': f"{status_emoji} {'ativo' if user['ativo'] else 'inativo'}",
                'tempo_cadastro': tempo,
                'data_cadastro': user['cadastrado_em']
            })
        
        return jsonify({
            'resumo': stats,
            'usuarios': usuarios_processados,
            'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': f'erro de comunicacao: {str(e)}'}), 503

@app.route('/status')
def verificar_status():
    try:
        resposta = requests.get(f'{USUARIOS_URL}/', timeout=3)
        
        if resposta.status_code == 200:
            return jsonify({
                'relatorio': 'ok',
                'servico_usuarios': 'online',
                'url_usuarios': USUARIOS_URL
            })
        else:
            return jsonify({
                'relatorio': 'ok',
                'servico_usuarios': 'com problemas',
                'codigo_http': resposta.status_code
            })
    except:
        return jsonify({
            'relatorio': 'ok',
            'servico_usuarios': 'offline',
            'url_usuarios': USUARIOS_URL
        }), 503

if __name__ == '__main__':
    print("Microsservico RELATORIO iniciando na porta 5001")
    print(f"Vai buscar usuarios em: {USUARIOS_URL}")
    app.run(host='0.0.0.0', port=5001, debug=False)
