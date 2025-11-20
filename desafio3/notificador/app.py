from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

notificacoes = []

@app.route('/')
def index():
    return jsonify({
        'servico': 'notificador',
        'funcao': 'recebe e registra notificacoes de eventos',
        'rotas': ['/notificar', '/historico', '/ultima']
    })

@app.route('/notificar', methods=['POST'])
def notificar():
    msg = request.json.get('mensagem', 'sem mensagem')
    
    notif = {
        'id': len(notificacoes) + 1,
        'mensagem': msg,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    
    notificacoes.append(notif)
    
    print(f"[NOTIFICACAO] {notif['timestamp']} - {msg}")
    
    return jsonify({
        'status': 'notificado',
        'id': notif['id']
    })

@app.route('/historico')
def historico():
    return jsonify({
        'total': len(notificacoes),
        'notificacoes': notificacoes[-15:]
    })

@app.route('/ultima')
def ultima():
    if notificacoes:
        return jsonify(notificacoes[-1])
    return jsonify({'mensagem': 'nenhuma notificacao ainda'})

if __name__ == '__main__':
    print("Servico NOTIFICADOR rodando na porta 5002")
    app.run(host='0.0.0.0', port=5002, debug=False)
