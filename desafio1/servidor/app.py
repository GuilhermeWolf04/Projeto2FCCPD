from flask import Flask, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

# contador pra saber quantas vezes foi acessado
qtd_acessos = 0

@app.route('/')
def pagina_principal():
    global qtd_acessos
    qtd_acessos += 1
    
    nome_host = socket.gethostname()
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    dados = {
        'msg': 'Servidor online e funcionando',
        'container_id': nome_host,
        'horario': agora,
        'acessos': qtd_acessos
    }
    
    print(f"[{agora}] Acesso #{qtd_acessos}")
    
    return jsonify(dados), 200

@app.route('/status')
def verificar_status():
    # endpoint pra checar se ta tudo ok
    return jsonify({
        'ok': True,
        'nome': 'servidor-web'
    }), 200

@app.route('/info')
def informacoes():
    # mostra algumas infos do servidor
    return jsonify({
        'total_acessos': qtd_acessos,
        'rodando_desde': datetime.now().strftime('%d/%m/%Y às %H:%M:%S')
    }), 200

if __name__ == '__main__':
    print("Iniciando servidor web na porta 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False)
