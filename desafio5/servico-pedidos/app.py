from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

pedidos = [
    {
        'id': 1001,
        'usuario_id': 1,
        'data_pedido': '2024-11-10',
        'valor_total': 245.90,
        'status': 'entregue',
        'itens': [
            {'produto': 'Livro Python', 'quantidade': 2, 'preco': 89.90},
            {'produto': 'Caneca Programador', 'quantidade': 1, 'preco': 35.00}
        ],
        'endereco_entrega': 'Rua das Flores, 123 - São Paulo/SP'
    },
    {
        'id': 1002,
        'usuario_id': 2,
        'data_pedido': '2024-11-12',
        'valor_total': 159.00,
        'status': 'em_transito',
        'itens': [
            {'produto': 'Mouse Gamer', 'quantidade': 1, 'preco': 159.00}
        ],
        'endereco_entrega': 'Av. Atlântica, 456 - Rio de Janeiro/RJ'
    },
    {
        'id': 1003,
        'usuario_id': 1,
        'data_pedido': '2024-11-15',
        'valor_total': 532.50,
        'status': 'processando',
        'itens': [
            {'produto': 'Teclado Mecânico', 'quantidade': 1, 'preco': 399.90},
            {'produto': 'Mousepad Grande', 'quantidade': 1, 'preco': 89.90},
            {'produto': 'Cabo USB-C', 'quantidade': 2, 'preco': 21.35}
        ],
        'endereco_entrega': 'Rua das Flores, 123 - São Paulo/SP'
    },
    {
        'id': 1004,
        'usuario_id': 4,
        'data_pedido': '2024-11-16',
        'valor_total': 89.90,
        'status': 'entregue',
        'itens': [
            {'produto': 'Livro JavaScript', 'quantidade': 1, 'preco': 89.90}
        ],
        'endereco_entrega': 'Rua do Sol, 789 - Fortaleza/CE'
    },
    {
        'id': 1005,
        'usuario_id': 5,
        'data_pedido': '2024-11-17',
        'valor_total': 1250.00,
        'status': 'em_transito',
        'itens': [
            {'produto': 'Monitor 24 polegadas', 'quantidade': 1, 'preco': 899.00},
            {'produto': 'Suporte Monitor', 'quantidade': 1, 'preco': 120.00},
            {'produto': 'Cabo HDMI', 'quantidade': 2, 'preco': 115.50}
        ],
        'endereco_entrega': 'Av. Ipiranga, 321 - Porto Alegre/RS'
    },
    {
        'id': 1006,
        'usuario_id': 6,
        'data_pedido': '2024-11-18',
        'valor_total': 45.00,
        'status': 'cancelado',
        'itens': [
            {'produto': 'Caneca Programador', 'quantidade': 1, 'preco': 35.00}
        ],
        'endereco_entrega': 'Rua da Praia, 555 - Salvador/BA'
    },
    {
        'id': 1007,
        'usuario_id': 2,
        'data_pedido': '2024-11-19',
        'valor_total': 679.80,
        'status': 'processando',
        'itens': [
            {'produto': 'Webcam HD', 'quantidade': 1, 'preco': 299.90},
            {'produto': 'Microfone USB', 'quantidade': 1, 'preco': 379.90}
        ],
        'endereco_entrega': 'Av. Atlântica, 456 - Rio de Janeiro/RJ'
    }
]

@app.route('/')
def index():
    return jsonify({
        'servico': 'pedidos',
        'versao': '2.0',
        'total_pedidos': len(pedidos),
        'endpoints': {
            '/pedidos': 'lista todos os pedidos',
            '/pedidos/<id>': 'busca pedido especifico',
            '/pedidos/usuario/<user_id>': 'pedidos de um usuario',
            '/pedidos/status/<status>': 'pedidos por status',
            '/pedidos/stats': 'estatisticas de vendas'
        }
    })

@app.route('/pedidos')
def listar_todos():
    return jsonify({
        'total': len(pedidos),
        'pedidos': pedidos
    })

@app.route('/pedidos/<int:pedido_id>')
def buscar_por_id(pedido_id):
    pedido = next((p for p in pedidos if p['id'] == pedido_id), None)
    
    if pedido:
        return jsonify(pedido)
    else:
        return jsonify({'erro': 'pedido nao encontrado', 'id_buscado': pedido_id}), 404

@app.route('/pedidos/usuario/<int:user_id>')
def buscar_por_usuario(user_id):
    pedidos_usuario = [p for p in pedidos if p['usuario_id'] == user_id]
    
    if pedidos_usuario:
        # calcula total gasto
        total_gasto = sum(p['valor_total'] for p in pedidos_usuario)
        
        return jsonify({
            'usuario_id': user_id,
            'total_pedidos': len(pedidos_usuario),
            'valor_total_gasto': round(total_gasto, 2),
            'pedidos': pedidos_usuario
        })
    else:
        return jsonify({
            'usuario_id': user_id,
            'total_pedidos': 0,
            'pedidos': []
        })

@app.route('/pedidos/status/<string:status>')
def buscar_por_status(status):
    pedidos_filtrados = [p for p in pedidos if p['status'] == status]
    
    return jsonify({
        'status': status,
        'total': len(pedidos_filtrados),
        'pedidos': pedidos_filtrados
    })

@app.route('/pedidos/stats')
def estatisticas():
    total_vendas = sum(p['valor_total'] for p in pedidos)
    ticket_medio = total_vendas / len(pedidos) if pedidos else 0
    
    # conta por status
    por_status = {}
    for p in pedidos:
        status = p['status']
        por_status[status] = por_status.get(status, 0) + 1
    
    contador_produtos = {}
    for p in pedidos:
        for item in p['itens']:
            prod = item['produto']
            contador_produtos[prod] = contador_produtos.get(prod, 0) + item['quantidade']
    
    produto_top = max(contador_produtos.items(), key=lambda x: x[1]) if contador_produtos else ('nenhum', 0)
    
    return jsonify({
        'total_pedidos': len(pedidos),
        'valor_total_vendas': round(total_vendas, 2),
        'ticket_medio': round(ticket_medio, 2),
        'distribuicao_status': por_status,
        'produto_mais_vendido': {
            'nome': produto_top[0],
            'quantidade': produto_top[1]
        }
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Servico de PEDIDOS iniciando...")
    print(f"Total de pedidos cadastrados: {len(pedidos)}")
    print("Porta: 5002")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5002, debug=False)
