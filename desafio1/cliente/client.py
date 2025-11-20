import requests
import time
from datetime import datetime

URL_SERVIDOR = "http://servidor-web:8080"
TEMPO_ESPERA = 5 

def chamar_servidor(rota="/"):
    try:
        url = f"{URL_SERVIDOR}{rota}"
        resp = requests.get(url, timeout=3)
        
        hora = datetime.now().strftime('%H:%M:%S')
        
        if resp.status_code == 200:
            info = resp.json()
            print(f"[{hora}] OK - Recebido:")
            print(f"  Mensagem: {info.get('msg')}")
            print(f"  Container: {info.get('container_id')}")
            print(f"  Acessos no servidor: {info.get('acessos')}")
            print("="*50)
        else:
            print(f"[{hora}] Erro HTTP {resp.status_code}")
            
    except requests.exceptions.ConnectionError:
        hora = datetime.now().strftime('%H:%M:%S')
        print(f"[{hora}] Erro de conexão - servidor fora do ar?")
    except requests.exceptions.Timeout:
        hora = datetime.now().strftime('%H:%M:%S')
        print(f"[{hora}] Timeout - servidor demorou muito pra responder")
    except Exception as e:
        hora = datetime.now().strftime('%H:%M:%S')
        print(f"[{hora}] Deu erro: {e}")

def rodar():
    print("*" * 50)
    print("Cliente rodando...")
    print(f"Vai chamar: {URL_SERVIDOR}")
    print(f"A cada {TEMPO_ESPERA}s")
    print("*" * 50)
    print()
    
    print("Esperando servidor subir...")
    time.sleep(3)
    
    num_request = 0
    
    while True:
        num_request += 1
        print(f"\n-- Request #{num_request} --")
        chamar_servidor()
        time.sleep(TEMPO_ESPERA)

if __name__ == '__main__':
    rodar()
