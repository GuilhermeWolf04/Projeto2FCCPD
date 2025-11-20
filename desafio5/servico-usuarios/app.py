from flask import Flask, jsonify
from datetime import datetime
import random

app = Flask(__name__)

usuarios = [
    {
        'id': 1,
        'nome': 'Ana Carolina',
        'email': 'ana.carolina@exemplo.com',
        'cpf': '123.456.789-01',
        'telefone': '(11) 98765-4321',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cadastrado_em': '2022-05-10',
        'status': 'ativo'
    },
    {
        'id': 2,
        'nome': 'Bruno Mendes',
        'email': 'bruno.mendes@exemplo.com',
        'cpf': '234.567.890-12',
        'telefone': '(21) 99876-5432',
        'cidade': 'Rio de Janeiro',
        'estado': 'RJ',
        'cadastrado_em': '2023-01-20',
        'status': 'ativo'
    },
    {
        'id': 3,
        'nome': 'Carla Souza',
        'email': 'carla.souza@exemplo.com',
        'cpf': '345.678.901-23',
        'telefone': '(31) 97654-3210',
        'cidade': 'Belo Horizonte',
        'estado': 'MG',
        'cadastrado_em': '2021-11-15',
        'status': 'inativo'
    },
    {
        'id': 4,
        'nome': 'Daniel Oliveira',
        'email': 'daniel.oliveira@exemplo.com',
        'cpf': '456.789.012-34',
        'telefone': '(85) 96543-2109',
        'cidade': 'Fortaleza',
        'estado': 'CE',
        'cadastrado_em': '2023-07-03',
        'status': 'ativo'
    },
    {
        'id': 5,
        'nome': 'Eduarda Lima',
        'email': 'eduarda.lima@exemplo.com',
        'cpf': '567.890.123-45',
        'telefone': '(51) 95432-1098',
        'cidade': 'Porto Alegre',
        'estado': 'RS',
        'cadastrado_em': '2024-02-28',
        'status': 'ativo'
    },
    {
        'id': 6,
        'nome': 'Fernando Santos',
        'email': 'fernando.santos@exemplo.com',
        'cpf': '678.901.234-56',
        'telefone': '(71) 94321-0987',
        'cidade': 'Salvador',
        'estado': 'BA',
        'cadastrado_em': '2022-09-12',
        'status': 'ativo'
    }
]

@app.route('/')
def index():
    return jsonify({
        'servico': 'usuarios',
        'versao': '2.0',
        'total_cadastrados': len(usuarios),
        'endpoints': {
            '/usuarios': 'lista todos os usuarios',
            '/usuarios/<id>': 'busca usuario especifico',
            '/usuarios/estado/<uf>': 'usuarios por estado',
            '/usuarios/stats': 'estatisticas gerais'
        }
    })

@app.route('/usuarios')
def listar_todos():
    return jsonify({
        'total': len(usuarios),
        'usuarios': usuarios
    })

@app.route('/usuarios/<int:user_id>')
def buscar_por_id(user_id):
    usuario = next((u for u in usuarios if u['id'] == user_id), None)
    
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'erro': 'usuario nao encontrado', 'id_buscado': user_id}), 404

@app.route('/usuarios/estado/<string:uf>')
def buscar_por_estado(uf):
    usuarios_estado = [u for u in usuarios if u['estado'].upper() == uf.upper()]
    
    return jsonify({
        'estado': uf.upper(),
        'total': len(usuarios_estado),
        'usuarios': usuarios_estado
    })

@app.route('/usuarios/stats')
def estatisticas():
    ativos = sum(1 for u in usuarios if u['status'] == 'ativo')
    inativos = len(usuarios) - ativos
    
    por_estado = {}
    for u in usuarios:
        estado = u['estado']
        por_estado[estado] = por_estado.get(estado, 0) + 1
    
    return jsonify({
        'total_usuarios': len(usuarios),
        'ativos': ativos,
        'inativos': inativos,
        'percentual_ativos': round((ativos / len(usuarios)) * 100, 1),
        'distribuicao_estados': por_estado
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Servico de USUARIOS iniciando...")
    print(f"Total de usuarios cadastrados: {len(usuarios)}")
    print("Porta: 5001")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=False)
