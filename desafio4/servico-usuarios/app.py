from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

usuarios_cadastrados = [
    {
        'id': 1,
        'nome': 'João Silva',
        'email': 'joao.silva@email.com',
        'ativo': True,
        'cadastrado_em': '2023-01-15'
    },
    {
        'id': 2,
        'nome': 'Maria Santos',
        'email': 'maria.santos@email.com',
        'ativo': True,
        'cadastrado_em': '2023-03-22'
    },
    {
        'id': 3,
        'nome': 'Carlos Oliveira',
        'email': 'carlos.oliveira@email.com',
        'ativo': False,
        'cadastrado_em': '2022-11-08'
    },
    {
        'id': 4,
        'nome': 'Ana Paula',
        'email': 'ana.paula@email.com',
        'ativo': True,
        'cadastrado_em': '2024-02-10'
    },
    {
        'id': 5,
        'nome': 'Pedro Costa',
        'email': 'pedro.costa@email.com',
        'ativo': True,
        'cadastrado_em': '2023-07-30'
    }
]

@app.route('/')
def index():
    return jsonify({
        'servico': 'usuarios',
        'versao': '1.0',
        'descricao': 'API de gerenciamento de usuarios',
        'rotas': ['/usuarios', '/usuarios/<id>', '/stats']
    })

@app.route('/usuarios')
def listar_usuarios():
    return jsonify({
        'total': len(usuarios_cadastrados),
        'usuarios': usuarios_cadastrados
    })

@app.route('/usuarios/<int:user_id>')
def buscar_usuario(user_id):
    usuario = next((u for u in usuarios_cadastrados if u['id'] == user_id), None)
    
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'erro': 'usuario nao encontrado'}), 404

@app.route('/stats')
def estatisticas():
    ativos = sum(1 for u in usuarios_cadastrados if u['ativo'])
    inativos = len(usuarios_cadastrados) - ativos
    
    return jsonify({
        'total_usuarios': len(usuarios_cadastrados),
        'usuarios_ativos': ativos,
        'usuarios_inativos': inativos,
        'percentual_ativos': round((ativos / len(usuarios_cadastrados)) * 100, 2)
    })

if __name__ == '__main__':
    print("Microsservico USUARIOS iniciando na porta 5000")
    print(f"Total de usuarios cadastrados: {len(usuarios_cadastrados)}")
    app.run(host='0.0.0.0', port=5000, debug=False)
