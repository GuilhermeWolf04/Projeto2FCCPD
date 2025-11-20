from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

armazenamento = []

@app.route('/')
def index():
    return jsonify({
        'servico': 'armazenador',
        'funcao': 'guarda dados recebidos de outros servicos',
        'rotas': ['/guardar', '/listar', '/limpar']
    })

@app.route('/guardar', methods=['POST'])
def guardar():
    dados = request.json
    
    registro = {
        'timestamp': datetime.now().isoformat(),
        'dados': dados
    }
    
    armazenamento.append(registro)
    
    return jsonify({
        'status': 'guardado',
        'total_registros': len(armazenamento)
    })

@app.route('/listar')
def listar():
    return jsonify({
        'total': len(armazenamento),
        'registros': armazenamento[-10:] 
    })

@app.route('/limpar', methods=['DELETE'])
def limpar():
    qtd = len(armazenamento)
    armazenamento.clear()
    return jsonify({
        'status': 'limpo',
        'removidos': qtd
    })

if __name__ == '__main__':
    print("Servico ARMAZENADOR rodando na porta 5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
