import sqlite3
from datetime import datetime
import sys
import time

DB_PATH = '/data/meu_banco.db'

def setup_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_teste():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    mensagens = [
        "Teste automatico 1",
        "Teste automatico 2", 
        "Dados para validar persistencia"
    ]
    
    for msg in mensagens:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        cursor.execute('INSERT INTO registros (mensagem, data_hora) VALUES (?, ?)', (msg, agora))
        print(f"Adicionado: {msg}")
        time.sleep(0.5)
    
    conn.commit()
    conn.close()
    print(f"\n{len(mensagens)} registros adicionados com sucesso!")

if __name__ == '__main__':
    print("=== TESTE AUTOMATICO - ADICIONAR DADOS ===\n")
    setup_banco()
    adicionar_teste()
