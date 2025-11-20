import sqlite3
import sys

DB_PATH = '/data/meu_banco.db'

def ler_dados():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, mensagem, data_hora FROM registros ORDER BY id')
        registros = cursor.fetchall()
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("LEITURA DOS DADOS PERSISTIDOS (Container de Leitura)")
        print("=" * 60)
        
        if registros:
            print(f"\nEncontrados {len(registros)} registro(s):\n")
            for r in registros:
                print(f"  [{r[0]}] {r[1]}")
                print(f"      Criado em: {r[2]}")
                print()
        else:
            print("\nNenhum dado encontrado no banco.")
        
        print("=" * 60)
        
    except sqlite3.OperationalError as e:
        print(f"Erro ao acessar o banco: {e}")
        print("O banco nao existe ou nao pode ser lido.")
        sys.exit(1)

if __name__ == '__main__':
    print("\n*** CONTAINER DE LEITURA (READ-ONLY) ***")
    print("Este container so le os dados, nao modifica nada.\n")
    ler_dados()
