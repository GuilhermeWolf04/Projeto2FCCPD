import sqlite3
from datetime import datetime
import os

DB_PATH = '/data/meu_banco.db'

def iniciar_banco():
    print(f"Conectando no banco em {DB_PATH}")
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
    print("Banco inicializado!")

def adicionar_registro(msg):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cursor.execute('INSERT INTO registros (mensagem, data_hora) VALUES (?, ?)', (msg, agora))
    
    conn.commit()
    conn.close()
    print(f"Registro adicionado: '{msg}' em {agora}")

def listar_registros():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, mensagem, data_hora FROM registros ORDER BY id')
    registros = cursor.fetchall()
    
    conn.close()
    
    if registros:
        print("\n=== REGISTROS NO BANCO ===")
        for r in registros:
            print(f"ID {r[0]}: {r[1]} - {r[2]}")
        print(f"Total: {len(registros)} registro(s)")
        print("=" * 50)
    else:
        print("Nenhum registro encontrado ainda.")
    
    return len(registros)

def menu():
    iniciar_banco()
    
    print("\n*** SISTEMA DE REGISTROS ***")
    print("1 - Adicionar registro")
    print("2 - Ver todos os registros")
    print("3 - Sair")
    
    while True:
        print("\nEscolha uma opcao:")
        opcao = input("> ").strip()
        
        if opcao == '1':
            msg = input("Digite a mensagem: ").strip()
            if msg:
                adicionar_registro(msg)
            else:
                print("Mensagem vazia!")
        
        elif opcao == '2':
            listar_registros()
        
        elif opcao == '3':
            print("Saindo...")
            break
        
        else:
            print("Opcao invalida!")

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        print(f"*** BANCO EXISTENTE ENCONTRADO! ***")
        print("Os dados foram persistidos com sucesso no volume!")
    else:
        print("Criando novo banco de dados...")
    
    menu()
