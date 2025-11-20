from flask import Flask, jsonify, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

USUARIOS_SERVICE = os.getenv('USUARIOS_SERVICE', 'http://localhost:5001')
PEDIDOS_SERVICE = os.getenv('PEDIDOS_SERVICE', 'http://localhost:5002')

TIMEOUT = 5

@app.route('/')
def index():
    return jsonify({
        'servico': 'API Gateway',
        'versao': '1.0',
        'descricao': 'Ponto unico de entrada para os microsservicos',
        'servicos_disponiveis': {
            'usuarios': USUARIOS_SERVICE,
            'pedidos': PEDIDOS_SERVICE
        },
        'rotas_principais': {
            '/users': 'gerenciamento de usuarios',
            '/orders': 'gerenciamento de pedidos',
            '/health': 'status dos servicos',
            '/dashboard': 'visao geral do sistema'
        }
    })


@app.route('/users', methods=['GET'])
def listar_usuarios():
    """
    Busca todos os usuarios do microsservico
    """
    try:
        resp = requests.get(f'{USUARIOS_SERVICE}/usuarios', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            return jsonify({'erro': 'falha ao buscar usuarios', 'detalhes': resp.text}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de usuarios indisponivel', 'mensagem': str(e)}), 503

@app.route('/users/<int:user_id>', methods=['GET'])
def buscar_usuario(user_id):
    """
    Busca usuario especifico
    """
    try:
        resp = requests.get(f'{USUARIOS_SERVICE}/usuarios/{user_id}', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        elif resp.status_code == 404:
            return jsonify({'erro': 'usuario nao encontrado'}), 404
        else:
            return jsonify({'erro': 'erro ao buscar usuario'}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de usuarios indisponivel', 'mensagem': str(e)}), 503

@app.route('/users/state/<string:uf>', methods=['GET'])
def usuarios_por_estado(uf):
    """
    Busca usuarios de um estado especifico
    """
    try:
        resp = requests.get(f'{USUARIOS_SERVICE}/usuarios/estado/{uf}', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            return jsonify({'erro': 'falha ao filtrar usuarios'}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de usuarios indisponivel', 'mensagem': str(e)}), 503


@app.route('/orders', methods=['GET'])
def listar_pedidos():
    """
    Busca todos os pedidos do microsservico
    """
    try:
        resp = requests.get(f'{PEDIDOS_SERVICE}/pedidos', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            return jsonify({'erro': 'falha ao buscar pedidos', 'detalhes': resp.text}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de pedidos indisponivel', 'mensagem': str(e)}), 503

@app.route('/orders/<int:order_id>', methods=['GET'])
def buscar_pedido(order_id):
    """
    Busca pedido especifico
    """
    try:
        resp = requests.get(f'{PEDIDOS_SERVICE}/pedidos/{order_id}', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        elif resp.status_code == 404:
            return jsonify({'erro': 'pedido nao encontrado'}), 404
        else:
            return jsonify({'erro': 'erro ao buscar pedido'}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de pedidos indisponivel', 'mensagem': str(e)}), 503

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def pedidos_do_usuario(user_id):
    """
    Busca pedidos de um usuario especifico
    Combina dados de ambos os microsservicos
    """
    try:
        resp_user = requests.get(f'{USUARIOS_SERVICE}/usuarios/{user_id}', timeout=TIMEOUT)
        
        if resp_user.status_code == 404:
            return jsonify({'erro': 'usuario nao encontrado'}), 404
        
        resp_orders = requests.get(f'{PEDIDOS_SERVICE}/pedidos/usuario/{user_id}', timeout=TIMEOUT)
        
        if resp_user.status_code == 200 and resp_orders.status_code == 200:
            usuario = resp_user.json()
            pedidos_data = resp_orders.json()
            
            resultado = {
                'usuario': {
                    'id': usuario['id'],
                    'nome': usuario['nome'],
                    'email': usuario['email'],
                    'cidade': usuario['cidade'],
                    'status': usuario['status']
                },
                'historico_pedidos': {
                    'total_pedidos': pedidos_data['total_pedidos'],
                    'valor_total_gasto': pedidos_data.get('valor_total_gasto', 0),
                    'pedidos': pedidos_data['pedidos']
                }
            }
            
            return jsonify(resultado)
        else:
            return jsonify({'erro': 'falha ao combinar dados'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'um dos servicos esta indisponivel', 'mensagem': str(e)}), 503

@app.route('/orders/status/<string:status>', methods=['GET'])
def pedidos_por_status(status):
    """
    Filtra pedidos por status
    """
    try:
        resp = requests.get(f'{PEDIDOS_SERVICE}/pedidos/status/{status}', timeout=TIMEOUT)
        
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            return jsonify({'erro': 'falha ao filtrar pedidos'}), resp.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'servico de pedidos indisponivel', 'mensagem': str(e)}), 503


@app.route('/health', methods=['GET'])
def verificar_saude():
    """
    Verifica se todos os microsservicos estao respondendo
    """
    servicos_status = {
        'gateway': 'ok',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        resp = requests.get(f'{USUARIOS_SERVICE}/', timeout=2)
        servicos_status['usuarios'] = 'online' if resp.status_code == 200 else 'com_problemas'
    except:
        servicos_status['usuarios'] = 'offline'
    
    try:
        resp = requests.get(f'{PEDIDOS_SERVICE}/', timeout=2)
        servicos_status['pedidos'] = 'online' if resp.status_code == 200 else 'com_problemas'
    except:
        servicos_status['pedidos'] = 'offline'
    
    if servicos_status['usuarios'] == 'online' and servicos_status['pedidos'] == 'online':
        servicos_status['status_geral'] = 'todos_servicos_operacionais'
        codigo_http = 200
    elif servicos_status['usuarios'] == 'offline' and servicos_status['pedidos'] == 'offline':
        servicos_status['status_geral'] = 'todos_servicos_offline'
        codigo_http = 503
    else:
        servicos_status['status_geral'] = 'operacao_parcial'
        codigo_http = 207 
    
    return jsonify(servicos_status), codigo_http

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Combina estatisticas de ambos os servicos
    Visao geral do sistema
    """
    try:
        resp_users = requests.get(f'{USUARIOS_SERVICE}/usuarios/stats', timeout=TIMEOUT)
        
        resp_orders = requests.get(f'{PEDIDOS_SERVICE}/pedidos/stats', timeout=TIMEOUT)
        
        if resp_users.status_code == 200 and resp_orders.status_code == 200:
            stats_users = resp_users.json()
            stats_orders = resp_orders.json()
            
            dashboard_data = {
                'resumo_geral': {
                    'total_usuarios': stats_users['total_usuarios'],
                    'usuarios_ativos': stats_users['ativos'],
                    'total_pedidos': stats_orders['total_pedidos'],
                    'valor_total_vendas': stats_orders['valor_total_vendas'],
                    'ticket_medio': stats_orders['ticket_medio']
                },
                'detalhes_usuarios': {
                    'percentual_ativos': stats_users['percentual_ativos'],
                    'distribuicao_estados': stats_users['distribuicao_estados']
                },
                'detalhes_pedidos': {
                    'distribuicao_status': stats_orders['distribuicao_status'],
                    'produto_mais_vendido': stats_orders['produto_mais_vendido']
                },
                'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
            
            return jsonify(dashboard_data)
        else:
            return jsonify({'erro': 'falha ao gerar dashboard'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'erro': 'um ou mais servicos indisponiveis', 'mensagem': str(e)}), 503

if __name__ == '__main__':
    print("=" * 60)
    print("API GATEWAY iniciando...")
    print(f"Porta: 8000")
    print(f"Servico de Usuarios: {USUARIOS_SERVICE}")
    print(f"Servico de Pedidos: {PEDIDOS_SERVICE}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000, debug=False)
